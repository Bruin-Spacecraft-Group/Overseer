import json
import subprocess
import time

class GPS:
    def __init__(self):
        self.data_file = "gps_data.json"

    def fetch_data(self):
        with open(self.data_file, "w") as f:
            subprocess.run(["gpspipe", "-w", "-n", "5"], stdout=f)

    def parse_data(self):
        json_out = {}
        with open(self.data_file, "r") as f:
            for line in f:
                json_loaded = json.loads(line)
                if json_loaded["class"] == "TPV" and json_loaded["mode"] > 1:
                    json_out = json_loaded
                    break
        return json_out

    def get_gps_data(self):
        self.fetch_data()
        return self.parse_data()

def main():
    gps = GPS()

    try:
        while True:
            data = gps.get_gps_data()
            print(json.dumps(data, indent=4))
            time.sleep(1)  # Delay for readability
    except KeyboardInterrupt:
        print("Program interrupted by the user.")
    finally:
        del gps

if __name__ == "__main__":
    main()
