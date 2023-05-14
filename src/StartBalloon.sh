
# direwolf start, output to console and file, start uplink script
direwolf -c ~/direwolf/flight_mode.conf | tee ~/FLIGHT_DATA_S23/flight_output.txt & python3 ~/Overseer/src/uplink.py