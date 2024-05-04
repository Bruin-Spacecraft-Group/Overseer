import os
import psutil
from typing import Literal
from datetime import datetime
from gpiozero import CPUTemperature


class CPUMetrics:
    """
    Basic CPU metrics for a Raspberry Pi:
    - temperature
    - clock speed/ticks
    - RAM total, used and free
    - disk total, used and free
    - top 5 processes using the most RAM

    Initialization takes 2 optional parameters:
    - `units`: one of "B", "KB", "MB" or "GB", to specify the units of the data; default "MB"
    - `dp`: an integer used to round the data to the specified decimal places; default 2
    - `topn`: an integer representing the top `topn` processes using the most memory

    Exposed via the `get_metrics` function.
    """
    UNITS = {
        "B": 1,
        "KB": 10 ** 3,
        "MB": 10 ** 6,
        "GB": 10 ** 9
    }

    def __init__(self, units: Literal["B", "KB", "MB", "GB"] = "MB", dp: int = 2, topn: int = 5) -> None:
        SIZE = CPUMetrics.UNITS.get(units, CPUMetrics.UNITS["MB"])

        # Get CPU temperature
        try:
            self.cpu_temp = CPUTemperature().temperature
        except:
            self.cpu_temp = "NA"

        # Get clock speed
        self.cpu_freq = psutil.cpu_freq().current

        # Get RAM data (in megabytes)
        # Sample `ram_usage` list:
        # ['total', 'used', 'free', 'shared', 'buff/cache', 'available', 'Mem:',
        # '7989', '1945', '1486', '335', '4557', '5401', 'Swap:', '2147', '0', '2147',
        # 'Total:', '10136', '1945', '3633']
        ram_usage = os.popen('free -t -b').read().strip().split()
        ram_usage = ram_usage[ram_usage.index("Mem:", ) + 1: ram_usage.index("Swap:")]
        self.ram_data = {
            "total": round(float(ram_usage[0]) / SIZE, dp),
            "used": round(float(ram_usage[1]) / SIZE, dp),
            "free": round(float(ram_usage[-1]) / SIZE, dp)
        }

        # Get disk usage
        disk_usage = psutil.disk_usage("/")
        self.disk_data = {
            "total": round(disk_usage.total / SIZE, dp),
            "used": round(disk_usage.used / SIZE, dp),
            "free": round(disk_usage.free / SIZE, dp)
        }

        # Get top 5 processes
        processes = [x for x in psutil.process_iter()]
        # Sort processes by memory usage
        processes = sorted(processes, key=lambda x: x.memory_info().rss, reverse=True)
        self.top_processes = []
        for process in processes[:topn]:
            self.top_processes.append({
                "pid": process.ppid(),
                "name": process.name(),
                "status": process.status(),
                "started_at": datetime.fromtimestamp(process.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
                "memory_usage": round(process.memory_info().rss / SIZE, dp)
            })

    def get_metrics(self) -> dict:
        """
        Return the metrics as a dictionary.
        Sample:
        ```python3
        {'cpu_temp': 'NA',
        'cpu_ticks': 2295.624,
        'disk': {'free': 1005947.83, 'total': 1081101.18, 'used': 20160.99},
        'ram': {'free': 5568.19, 'total': 7989.25, 'used': 2099.09},
        'top_processes': [
            {'memory_usage': 813.25,
            'name': 'process_name',
            'pid': 1024,
            'started_at': '2024-05-04 11:29:38',
            'status': 'sleeping'},
            ... (4 more processes)
        ]}
        ```
        """
        return {
            "cpu_temp": self.cpu_temp,
            "cpu_ticks": self.cpu_freq,
            "ram": self.ram_data,
            "disk": self.disk_data,
            "top_processes": self.top_processes
        }


# Unit testing (with pprint if available)
if __name__ == "__main__":
    try:
        from pprint import pprint
        printer = pprint
    except ImportError:
        printer = print

    cpu_metrics = CPUMetrics()
    printer(cpu_metrics.get_metrics())
