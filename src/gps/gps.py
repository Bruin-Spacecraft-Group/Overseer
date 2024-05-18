class Ublox():
    def __init__(self, cb=None):
        self.cb = cb

        self.isInFlightMode = False
        self.comm_thread = None

        self.lastFixTime = time.time()
        self.lastCommTime = time.time()
        self.lastAltTime = 0
        self.prev_alt = 0.0
        self.GPSDAT = {"status": "init", "navmode": "unknown",
                       "lat_raw":"0.00", "lat": "0.00", "lon_raw":"0.00", "lon": "0.00", "alt": "0",
                       "fixTime": "000000", "FixType": "?", "SatCount": 0,
                       "accentRate": 0, 'groundSpeed':"?", 'groundCourse':"?"}
        self.sim_alt = 30000 / 2.0
        self.sim_v = math.pi / (2 * 60 * 60)
        self.sim_t = 0.0

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme

    def bit(self):
        for retry in range(5):
          try:
            bus = smbus.SMBus(1)
            bus.read_byte(device)
            return False
          except NameError:
              return True
          except Exception as x:
            time.sleep(1)
        return True

    def gps_reset(self):
        if self.comm_thread is not None:
            self.comm_thread.stop()
        with open('assets/config.json') as fin:
            config = json.load(fin)
        self.logger.warning("GPS Reset!")
        GPIO.setup(config['pins']['GPS_RST'], GPIO.OUT)
        GPIO.output(config['pins']['GPS_RST'], GPIO.LOW)
        time.sleep(1)
        GPIO.output(config['pins']['GPS_RST'], GPIO.HIGH)
        self.isInFlightMode = False
        self.comm_thread = communicationThread(self.nmea_handler, self.ublox_handler, self.error_handler)
        self.comm_thread.start()

    def start(self):
        self.gps_reset()
        print("i2c bit:", "error" if self.bit() else "ok")


    def stop(self):
        self.comm_thread.stop()

    def get_data(self):
        return self.GPSDAT

    def set_status(self, new_status):
        if self.GPSDAT['status'] != new_status:
          self.logger.info("gps status changed from %s to %s" % (self.GPSDAT['status'], new_status))
        self.GPSDAT['status']=new_status

    def housekeeping(self):
        if not self.comm_thread.isOk:
            self.set_status( no_i2c )
            return
        if not self.isInFlightMode:
            self.logger.info("set flight mode !")
            self.comm_thread.send_bytes(setNavCmnd)
            time.sleep(5)
        elapsed = time.time() - self.lastFixTime
        if elapsed > 2 * 60:
            self.GPSDAT['SatCount'] = -1
            self.set_status( im_lost )
            self.update_files()
            self.lastFixTime = time.time()
            # check for hardware failure
            if time.time() - self.lastCommTime > 5 * 60:
                self.set_status( no_comm )
            if self.bit():
                self.set_status( no_i2c )
                self.gps_reset()

    def update_files(self, filename="gps"):
        try:
            self.sim_t += self.sim_v
#            self.logger.info( "sim %f %f %f" % (self.sim_v, self.sim_t, self.sim_alt*(1-math.cos(self.sim_t))))

            self.GPSDAT['fixTimeStr'] = self.GPSDAT['fixTime'][0:2] + ':' + self.GPSDAT['fixTime'][2:4] + ':' + self.GPSDAT['fixTime'][4:6]

            # Change latitue and longitude to decimal degrees format
            longitude = self.GPSDAT["lon_raw"] 
            latitude = self.GPSDAT["lat_raw"]
            # calculate
            degrees_lon = float(longitude[:3])
            fraction_lon = float(longitude[3:]) / 60
            degrees_lat = float(latitude[:2])
            fraction_lat = float(latitude[2:]) / 60
            DD_longitude = degrees_lon + fraction_lon  # longitude (decimal degrees)
            DD_latitude = degrees_lat + fraction_lat  # latitude (decimal degrees)
            self.GPSDAT['lat'] = DD_latitude
            self.GPSDAT['lon'] = DD_longitude
            if 'alt_raw' in self.GPSDAT:
                self.GPSDAT['alt'] = float(self.GPSDAT['alt_raw']) # + self.sim_alt * (1-math.cos(self.sim_t))
        except Exception as x:
            self.logger.exception(x)
            self.logger.error("bad assets while calc files")
            return

        if printFix:
          self.logger.info("-----------------")
          self.logger.info("Lat %.4f" % self.GPSDAT['lat'])
          self.logger.info("Lon %.4f" % self.GPSDAT['lon'])
          self.logger.info("Alt %s" % self.GPSDAT["alt"])
          self.logger.info("Fix Time %s" % self.GPSDAT['fixTimeStr'])
          self.logger.info("Status %s" % self.GPSDAT["status"])
          self.logger.info("Nav Mode %s" % self.GPSDAT["navmode"])
          self.logger.info("Fix Mode %s" % self.GPSDAT["FixType"])
          self.logger.info("satellites %s" % self.GPSDAT["SatCount"])
          self.logger.info("ascent rate %s" % self.GPSDAT["accentRate"])
          self.logger.info("ground course %s" % self.GPSDAT['groundCourse'])
          self.logger.info("ground speed %s" % self.GPSDAT['groundSpeed'])
          self.logger.info("")
        self.lastFixTime = time.time()

    def tokenize(self, tokens, titles):
        rv = {}
        for i, k in enumerate(titles):
          try:
            if i>=len(tokens) :
                break
            rv[k] = tokens[i]
          except Exception as x:
            self.logger.error(i,k)
            self.logger.error(",".join(tokens))
            self.logger.exception(x)
        return rv

    def parse_gnrmc(self, tokens):
        RMCDAT = self.tokenize(tokens,
                               ['strType', 'fixTime', 'status', 'lat_raw', 'latDir',
                                'lon_raw', 'lonDir', 'groundSpeed', 'groundCourse',
                                'date', 'mode'])
        if RMCDAT["lat_raw"] == "":
            return False
        for i, k in enumerate(['fixTime', 'lat_raw', 'latDir', 'lon_raw', 'lonDir', 'groundSpeed', 'groundCourse', 'date']):
            self.GPSDAT[k] = RMCDAT[k]
        return True

    def parse_gngll(self, tokens):
        GGADAT = self.tokenize(tokens,
                               ['strType', 
                                'lat_raw', 'latDir', 'lon_raw', 'lonDir',
                                'fixTime', 'status', 'modeInd'
                               ])
        if GGADAT["lat_raw"] == "":
            return False
        for i, k in enumerate(['fixTime', 'lat_raw', 'latDir', 'lon_raw', 'lonDir']):
            self.GPSDAT[k] = GGADAT[k]
        return True

    def parse_gngga(self, tokens):
        GGADAT = self.tokenize(tokens,
                               ['strType', 'fixTime',
                                'lat_raw', 'latDir', 'lon_raw', 'lonDir',
                                'fixQual', 'numSat', 'horDil',
                                'alt_raw', 'altUnit', 'galt', 'galtUnit',
                                'DPGS_updt', 'DPGS_ID'])
        if GGADAT["lat_raw"] == "":
            return False
        for i, k in enumerate(['fixTime', 'lat_raw', 'latDir', 'lon_raw', 'lonDir', 'alt_raw']):
            self.GPSDAT[k] = GGADAT[k]
        return True

    def parse_gngsa(self, tokens):
        self.GPSDAT["FixType"] = tokens[1] + tokens[2]
        count = 0
        for id in tokens[3:14]:
            if id != "":
                count += 1
        self.GPSDAT["SatCount"] = count
        return True

    def nmea_handler(self, line):
        if verbose:
            self.logger.debug("nmea:"+line)
        self.lastCommTime = time.time()
        tokens = line.split(',')
        cmnd = tokens[0][1:]
        if cmnd in ["GNTXT", "GLGSV", "GPGSV"]:
            pass
        elif cmnd == "GNRMC":
            if verbose:
              self.logger.debug(("fix:  %s" % line))
            if self.parse_gnrmc(tokens):
                self.set_status( im_good )
            self.update_files()
        elif cmnd in ["GNGLL","GPGLL"]:
            if verbose:
                self.logger.debug("fix:  %s" % line)
            if self.parse_gngll(tokens):
                self.set_status(im_good)
        elif cmnd == "GNGGA":
            if verbose:
                self.logger.debug(("fix:  %s" % line))
            if self.parse_gngga(tokens):
                self.set_status(im_good)
            try:
                try:
                  alt = float(self.GPSDAT["alt_raw"])
                except:
                  self.logger.error("bad alt %s replacing with %s" %(self.GPSDAT['alt_alt'], self.prev_alt))
                  alt = self.prev_alt
                  self.GPSDAT['alt_raw'] = self.prev_alt
                if abs(alt-self.prev_alt) > 10000:
                  alt = self.prev_alt
                now = time.time()
                delta_time = now - self.lastAltTime
                if self.lastAltTime == 0:
                    self.lastAltTime = now
                    self.prev_alt = alt
                    self.GPSDAT['accentRate'] = 0
                elif delta_time > 10:
                    delta_alt = float(self.GPSDAT["alt"]) - float(self.prev_alt)
                    accent = delta_alt / delta_time
                    if verbose:
                        self.logger.debug(("%s m / %s sec = %s" % (delta_alt, delta_time, accent)))
                    self.GPSDAT["accentRate"] = 0.7 * self.GPSDAT["accentRate"] + 0.3 * accent
                    self.lastAltTime = now
                    self.update_files()
            except:
                pass
        elif cmnd == "GNGSA":
            if verbose:
                self.logger.debug(("stts: %s" % line))
            self.parse_gngsa(tokens)
        else:
            if verbose:
                self.logger.debug(("nmea unparsed: %s" % line))

    def ublox_handler(self, buffer):
        ack = [181, 98, 5, 1, 2, 0, 6, 36, 50, 91]
        if buffer == ack:
            self.logger.debug("got ACK !")
            self.GPSDAT["navmode"] = "flight"
            self.isInFlightMode = True
            self.update_files()
        else:
            if verbose:
                self.logger.info(("ublox: %s" % buffer))

    def error_handler(self, status):
        pass