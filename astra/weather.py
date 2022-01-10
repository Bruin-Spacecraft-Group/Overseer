# coding=utf-8

"""
This module contains classes for modelling the weather and atmosphere.

The environment classes providing the simulator module with all the atmospheric
data throughout a simulation:
    forecastEnvironment : GFS-based atmospheric model
    
University of Southampton
Niccolo' Zapponi, nz1g10@soton.ac.uk, 22/04/2013
"""

from datetime import timedelta
import logging
from six.moves import builtins
import numpy
from . import global_tools as tools
from . import GFS

# SETUP ERROR LOGGING AND DEBUGGING
logger = logging.getLogger(__name__)

# Pass through the @profile decorator if line profiler (kernprof) is not in use
try:
    builtins.profile
except AttributeError:
    def profile(func):
        return func


class environment(object):
    """
    Defines a common interface for the Simulator module.

    This is a meta class that should not be instantiated directly, and is
    provided mainly for code reuse and a uniform API for the simulator class,
    regardless of the environment data used.
    
    Parameters
    ----------
    launchSiteLat : float
        latitude of the launch site [deg]
    launchSiteLon : float
        longitude of the launch site [deg]
    launchSiteElev : float
        elevation of the launch site above Mean Sea Level [m]
    dateAndTime : :obj:`datetime.datetime`
        Date and time of launch
    inflationTemperature : float
        the ambient temperature during the balloon inflation [degC]
    UTC_offset : float
        the offset in hours between the current time zone and UTC
        (for example, Florida in winter has a UTC_offset = -5)

    Attributes
    ----------
    launchSiteLat : float
        latitude of the launch site [deg]
    launchSiteLon : float
        longitude of the launch site [deg]
    launchSiteElev : float
        elevation of the launch site above Mean Sea Level [m]
    dateAndTime : :obj:`datetime.datetime`
        Date and time of launch
    UTC_offset : float
        The offset in hours between the current time zone and UTC. NOTE: If
        zero, UTC offset is AUTOMATICALLY retrieved using the launch site GPS
        location

    Notes
    -----
    The primary base class methods that should be overridden are the 'getter'
    functions for Temperature, Pressure, WindDirection, WindSpeed, Density,
    Viscosity

    See Also
    --------
    astra.global_tools.getUTCOffset
    """

    def __init__(self,
                 launchSiteLat,
                 launchSiteLon,
                 launchSiteElev,
                 dateAndTime,
                 inflationTemperature=0.0,
                 UTC_offset=0.0,
                 debugging=False,
                 load_on_init=False):

        # COMMON INTERFACE

        # Variables
        # Set all kwargs as attributes - could move this to Base class
        self.inflationTemperature = inflationTemperature
        self.launchSiteLat = launchSiteLat
        self.launchSiteLon = launchSiteLon
        self.launchSiteElev = launchSiteElev
        self.dateAndTime = dateAndTime
        self.UTC_offset = UTC_offset
        self.debugging = debugging

        self._UTC_time = None

        # Monte Carlo parameters
        self.getMCWindDirection = []
        self.getMCWindSpeed = []

        self._weatherLoaded = False

        if debugging:
            log_lev = logging.DEBUG
        else:
            log_lev = logging.WARNING

        logger.setLevel(log_lev)

    def getTemperature(self, lat, lon, alt, time):
        """Request the temperature for an input location and time.

        Returns
        -------
        temperature : float
            temperature in degrees Celsius
        """
        raise NotImplementedError(
            "getTemperature method must be implemented by class {}".format(
                type(self).__name__))

    def getPressure(self, lat, lon, alt, time):
        """request the pressure for the point at the given location at the
        given time.
        Returns a float, pressure in [millibar]"""
        raise NotImplementedError(
            "getPressure method must be implemented by class {}".format(
                type(self).__name__))

    def getDensity(self, lat, lon, alt, time):
        """request the density for the point at the given location at the
        given time.
        Returns a float, density in [kg/m3]"""
        raise NotImplementedError(
            "getDensity method must be implemented by class {}".format(
            type(self).__name__))

    def getViscosity(self, lat, lon, alt, time):
        """getViscosity(): request the viscosity for the point
        at the given location at the given time.
        Returns a float, viscosity in [Pa s]"""
        raise NotImplementedError(
            "getViscosity method must be implemented by class {}".format(
            type(self).__name__))

    def getWindSpeed(self, *args):
        """request the wind speed for the point at the given location at the
        given time.
        Returns a float, speed in [knots]"""
        raise NotImplementedError(
            "getWindSpeed method must be implemented by class {}".format(
                type(self).__name__))

    def getWindDirection(self, *args):
        """getWindDirection(lat,lon,alt,time): request the wind direction for
        the point at the given location at the given time.
        Returns a float, direction in [degrees] clockwise from north"""
        raise NotImplementedError(
            "getWindDirection method must be implemented by class {}".format(
                type(self).__name__))


class forecastEnvironment(environment):
    """
    Class responsible for downloading weather forecast data from the Global
    Forecast System (GFS) and generating a forecast-based atmospheric model.

    Parameters
    ----------
    launchSiteLat : float
        latitude of the launch site [deg]
    launchSiteLon : float
        longitude of the launch site [deg]
    launchSiteElev : float
        elevation of the launch site above Mean Sea Level [m]
    dateAndTime : :obj:`datetime.datetime`
        The launch time
    UTC_offset : float
        the offset in hours between the current time zone and UTC (for example,
        Florida in winter has a UTC_offset = -5)
    inflationTemperature : float
        the ambient temperature during the balloon inflation [degC]
    [forceNonHD] : bool (default False)
        if TRUE, the weather forecast download will be forced to a lower
        resolution (i.e. 1deg x 1deg)
    [forecastDuration] : float (default 4)
        The number of hours from dateAndTime for which to download weather data
    [use_async] : bool (default True)
        Use an asynchronous request for downloads. This should speed up the
        download, but may incur larger memory overhead for large forecastDuration.
    [requestSimultaneous] : bool (default True)
        If True, populate a dictionary of responses from the web download
        requests, then process the data. If False, each response will be
        removed once the data has been processed: This has better memory
        overhead for large ForecastDuration, but is slower, and does not work
        with asynchronous requesting (use_async)
    [debug] : bool, optional (default False)
        If TRUE, all the information available will be logged
    [log_to_file]: bool, optional (default False)
         If true, all error and debug logs will be stored in an error.log file
    [progressHandler] : function, or None (default None)
        Progress for each downloaded parameter (in %) will be passed to this
        function, if provided.
    [load_on_init] : bool, optional (default False)
        If True, the forecast will be downloaded when the environment object is
        created. This is set to False by default, as the :obj:`flight` object
        should preferably be used to load the forecast (input validation and
        preflight checks should be done before expensive data download) 

    Notes
    -----
    * The simulator automatically switches to non-HD forecast if the amount of
    data requested is too high.

    :Example:
    
        >>> from datetime import datetime, timedelta
        >>> import weather

        >>> my_forecast_atmosphere = weather.forecastEnvironment()
        >>> my_forecast_atmosphere.launchSiteLat = 50.2245
        >>> my_forecast_atmosphere.launchSiteLon = -5.3069
        >>> my_forecast_atmosphere.launchSiteElev = 60
        >>> my_forecast_atmosphere.dateAndTime = datetime.now() + timedelta(days=1)
        >>> my_forecast_atmosphere.UTC_offset = 3
        >>> my_forecast_atmosphere.loadForecast()

    """

    def __init__(self,
                 launchSiteLat,
                 launchSiteLon,
                 launchSiteElev,
                 dateAndTime,
                 UTC_offset=0,
                 inflationTemperature=0.0,
                 forceNonHD=True,
                 forecastDuration=4,
                 use_async=True,
                 requestSimultaneous=True,
                 debugging=False,
                 progressHandler=None,
                 load_on_init=False):
        """
        Initialize the forecastEnvironment object
        """
        # Initialize extra forecast-specific variables
        self.forceNonHD = forceNonHD
        self.forecastDuration = forecastDuration
        self.use_async = use_async
        self.requestSimultaneous = requestSimultaneous

        self._GFSmodule = None

        # This should be the last thing that is called on init, since the base
        # (environment) class init calls self.load (if load_on_init is True)
        super(forecastEnvironment, self).__init__(
            inflationTemperature=inflationTemperature,
            launchSiteLat=launchSiteLat,
            launchSiteLon=launchSiteLon,
            launchSiteElev=launchSiteElev,
            dateAndTime=dateAndTime,
            UTC_offset=UTC_offset,
            debugging=debugging,
            load_on_init=load_on_init)

    @profile
    def load(self, progressHandler=None):
        """
        Create a link to the Global Forecast System and download the required
        atmospheric data.

        Once the data has been downloaded, altitude data is generated and
        interpolated. The processed data is then prepared to be used with
        standard environment methods.

        Parameters
        ----------
        progressHandler : function
            Returns progress 

        Returns
        -------
        status : TRUE if successful.
        """

        # Data validation
        if self._weatherLoaded:
            logger.warning(
                'The weather was already loaded. All data will be overwritten.')

        if self.launchSiteLat == 0.0:
            logger.debug(
                'The launch site latitude is set to 0!')
        if self.launchSiteLon == 0.0:
            logger.debug(
                'The launch site longitude is set to 0!')
        if self.dateAndTime is None:
            raise ValueError(
                'The flight date and time has not been set and is required!')

        if self.UTC_offset == 0:
            self.UTC_offset = tools.getUTCOffset(
                self.launchSiteLat,self.launchSiteLon,self.dateAndTime)
            logger.debug('Fetched time zone data about the launch site: UTC offset is %f hours' % self.UTC_offset)

        self._UTC_time = self.dateAndTime - timedelta(seconds=self.UTC_offset * 3600)
        logger.debug('Using UTC time %s' % self._UTC_time.strftime('%d/%m/%y %H:%M'))

        # log the current parameters
        logger.info('Preparing to download weather data for parameters:')
        logger.debug("    Launch site Latitude: {}".format(self.launchSiteLat))
        logger.debug("    Launch site Longitude: {}".format(self.launchSiteLon))
        logger.debug("    Launch time: {}".format(self._UTC_time))

        # Setup the GFS link
        self._GFSmodule = GFS.GFS_Handler(self.launchSiteLat,
                                          self.launchSiteLon,
                                          self._UTC_time,
                                          use_async=self.use_async,
                                          requestSimultaneous=self.requestSimultaneous,
                                          HD=(not self.forceNonHD),
                                          forecastDuration=
                                            self.forecastDuration,
                                          debugging=self.debugging)

        # Connect to the GFS and download data
        if self._GFSmodule.downloadForecast(progressHandler):
            logger.debug('GFS data successfully downloaded.')
        else:
            logger.error('Error while downloading GFS data.')
            return


        # Setup the standard environment data access functions


        # Linearly interpolate all data downloaded from the GFS
        pressureInterpolation, temperatureInterpolation,\
            windDirectionInterpolation, windSpeedInterpolation = \
                self._GFSmodule.interpolateData('press',
                                                'temp',
                                                'windrct',
                                                'windspd')

        self.getPressure = lambda lat, lon, alt, time: float(
            pressureInterpolation(lat, lon, alt, self._GFSmodule.getGFStime(
                time - timedelta(seconds=self.UTC_offset * 3600)))
            )
        self.getTemperature = lambda lat, lon, alt, time: float(
            temperatureInterpolation(lat, lon, alt, self._GFSmodule.getGFStime(
                time - timedelta(seconds=self.UTC_offset * 3600)))
            )
        self.getWindDirection = lambda lat, lon, alt, time: float(
            windDirectionInterpolation(lat, lon, alt, self._GFSmodule.getGFStime(
                time - timedelta(seconds=self.UTC_offset * 3600))))
        self.getWindSpeed = lambda lat, lon, alt, time: float(
            windSpeedInterpolation(lat, lon, alt, self._GFSmodule.getGFStime(
                time - timedelta(seconds=self.UTC_offset * 3600))))

        # Extra definitions for derived quantities (density and viscosity)
        AirMolecMass = 0.02896
        GasConstant = 8.31447
        standardTempRankine = tools.c2kel(15) * (9. / 5)
        Mu0 = 0.01827 # Mu 0 (15 deg) [cP]
        C = 120 # Sutherland's Constant

        self.getDensity = lambda lat, lon, alt, time: \
            self.getPressure(lat, lon, alt, time) * 100 * AirMolecMass / (GasConstant * 
                tools.c2kel(self.getTemperature(lat, lon, alt, time))
            )

        def viscosity(lat, lon, alt, time):
            tempRankine = tools.c2kel(self.getTemperature(lat, lon, alt, time)) * (9. / 5)
            TTO = (tempRankine / standardTempRankine) ** 1.5 # T/TO [Rankine/Rankine]
            TR = ((0.555 * standardTempRankine) + C) / ((0.555 * tempRankine) + C)
            vcP = Mu0 * TTO * TR
            return vcP / 1000.

        self.getViscosity = viscosity

        self._weatherLoaded = True


    def perturbWind(self, numberOfFlights):
        
        """
        Perform a wind perturbation for the purpose of Monte Carlo simulations.

        Note: this method should only be called AFTER loadForecast() has been
        performed.
        """

        if not self._weatherLoaded:
            logger.error('Error: the weather has not been loaded yet! Wind cannot be perturbed.')
            return

        self.getMCWindDirection = []
        self.getMCWindSpeed = []

        def perturbedWindDirection(lat, lon, alt, time):
            return self.getWindDirection(lat, lon, alt, time)

        def perturbedWindSpeed(lat, lon, alt, time):
            return self.getWindSpeed(lat, lon, alt, time)

        for _ in numpy.arange(numberOfFlights):
            self.getMCWindDirection.append(perturbedWindDirection)
            self.getMCWindSpeed.append(perturbedWindSpeed)