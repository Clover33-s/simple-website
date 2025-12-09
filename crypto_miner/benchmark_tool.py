import time
import hashlib
import multiprocessing
import threading
import platform
import subprocess
import os
try:
    from hardware_manager import SystemInfo
except ImportError:
    from .hardware_manager import SystemInfo

class SystemMonitor:
    def __init__(self):
        self.monitor_data = []
        self.monitoring_active = False
        self.thread = None

    def start(self):
        self.monitoring_active = True
        self.monitor_data = []
        self.thread = threading.Thread(target=self._monitor_loop)
        self.thread.start()

    def stop(self):
        self.monitoring_active = False
        if self.thread:
            self.thread.join()

    def _monitor_loop(self):
        while self.monitoring_active:
            stats = {
                "timestamp": time.time(),
                "cpu_percent": 0.0,
                "gpu_load": "N/A"
            }

            # Windows CPU Load
            if platform.system() == "Windows":
                try:
                    output = subprocess.check_output("wmic cpu get LoadPercentage", shell=True).decode().strip()
                    lines = output.split('\n')
                    if len(lines) > 1:
                        stats["cpu_percent"] = float(lines[1].strip())
                except:
                    pass

                # GPU Load (nvidia-smi)
                try:
                    output = subprocess.check_output("nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits", shell=True).decode().strip()
                    stats["gpu_load"] = f"{output}%"
                except:
                    pass

            self.monitor_data.append(stats)
            time.sleep(1)

    def get_data(self):
        return self.monitor_data

    def generate_log_section(self, f):
        f.write("System Monitor Log (Sampled during operation):\n")
        if not self.monitor_data:
            f.write("No monitoring data available (Monitoring implementation relies on Windows commands).\n")
        else:
            for entry in self.monitor_data:
                ts = time.strftime('%H:%M:%S', time.localtime(entry['timestamp']))
                f.write(f"[{ts}] CPU Load: {entry['cpu_percent']}% | GPU Load: {entry['gpu_load']}\n")


class Benchmark:
    def __init__(self):
        self.results = {}
        self.monitor = SystemMonitor()

    @staticmethod
    def _hash_worker(duration, stop_event, result_list):
        """Hashes continuously for a set duration."""
        count = 0
        sha256 = hashlib.sha256
        data = b"benchmark_data"
        while not stop_event.is_set():
            sha256(data).hexdigest()
            count += 1
        result_list.append(count)

    def run_single_core_test(self, duration=5):
        """Runs a benchmark on a single core."""
        stop_event = multiprocessing.Event()
        manager = multiprocessing.Manager()
        result_list = manager.list()

        # Start monitoring
        self.monitor.start()

        # Start Worker
        p = multiprocessing.Process(target=Benchmark._hash_worker, args=(duration, stop_event, result_list))
        p.start()

        time.sleep(duration)
        stop_event.set()
        p.join()

        # Stop monitoring
        self.monitor.stop()

        total_hashes = sum(result_list)
        hashrate = total_hashes / duration
        self.results['single_core'] = hashrate
        return hashrate

    def run_multi_core_test(self, duration=5):
        """Runs a benchmark on all available cores."""
        num_cores = multiprocessing.cpu_count()
        stop_event = multiprocessing.Event()
        manager = multiprocessing.Manager()
        result_list = manager.list()

        self.monitor.start()

        processes = []
        for _ in range(num_cores):
            p = multiprocessing.Process(target=Benchmark._hash_worker, args=(duration, stop_event, result_list))
            processes.append(p)
            p.start()

        time.sleep(duration)
        stop_event.set()

        for p in processes:
            p.join()

        self.monitor.stop()

        total_hashes = sum(result_list)
        hashrate = total_hashes / duration
        self.results['multi_core'] = hashrate
        return hashrate

    def generate_report(self, filename="benchmark_report.txt"):
        """Generates a comprehensive report file."""
        sys_info = SystemInfo().get_summary()

        single = self.results.get('single_core', 0)
        multi = self.results.get('multi_core', 0)
        efficiency = 0
        multiplier = 0
        if single > 0:
            efficiency = ((multi - single) / single) * 100
            multiplier = multi / single

        with open(filename, "w") as f:
            f.write("Crypto Mining Simulator - Benchmark Report\n")
            f.write("==========================================\n\n")

            f.write("Hardware Information:\n")
            f.write(f"OS: {sys_info['OS']}\n")
            f.write(f"CPU: {sys_info['CPU']}\n")
            f.write(f"Cores: {sys_info['Physical Cores']} Physical, {sys_info['Logical Cores']} Logical\n")
            f.write(f"GPU: {sys_info['GPU']}\n\n")

            f.write("Benchmark Results:\n")
            f.write(f"Single-Core Hashrate: {single:,.2f} H/s\n")
            f.write(f"Multi-Core Hashrate:  {multi:,.2f} H/s\n")
            if single > 0:
                f.write(f"Multi-Core Speedup:   {multiplier:.2f}x\n")
                f.write(f"Efficiency Gain:      {efficiency:.2f}%\n\n")

            f.write("Calculation Explanation:\n")
            f.write("1. Single-Core Hashrate = Total Hashes / Duration\n")
            f.write("2. Multi-Core Hashrate  = Sum of all Core Hashes / Duration\n")
            f.write("3. Speedup              = Multi-Core / Single-Core\n\n")

            self.monitor.generate_log_section(f)

        return filename
