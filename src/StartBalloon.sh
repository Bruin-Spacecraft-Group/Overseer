
# direwolf start, output to console and file, start uplink script
direwolf -c flight_mode.conf | tee flight_output.txt & python3 uplink.py