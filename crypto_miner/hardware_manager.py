import platform
import subprocess
import shutil
import re

class SystemInfo:
    def __init__(self):
        self.os_info = platform.system() + " " + platform.release()
        self.cpu_info = "Unknown CPU"
        self.cpu_count_physical = 0
        self.cpu_count_logical = 0
        self.gpu_info = "Unknown GPU"
        self._detect_hardware()

    def _detect_hardware(self):
        """Detects CPU and GPU information based on the OS."""
        self._detect_cpu()
        self._detect_gpu()

    def _detect_cpu(self):
        """Detects CPU model and core counts."""
        self.cpu_info = platform.processor()
        # Fallback if platform.processor is empty or generic
        if not self.cpu_info:
            self.cpu_info = platform.machine()

        if platform.system() == "Windows":
            try:
                # Get CPU Name
                command = "wmic cpu get Name"
                output = subprocess.check_output(command, shell=True).decode().strip()
                lines = output.split('\n')
                if len(lines) > 1:
                    self.cpu_info = lines[1].strip()

                # Get Cores
                command_cores = "wmic cpu get NumberOfCores,NumberOfLogicalProcessors"
                output_cores = subprocess.check_output(command_cores, shell=True).decode().strip()
                # Expected output:
                # NumberOfCores  NumberOfLogicalProcessors
                # 6              12
                lines = output_cores.split('\n')
                if len(lines) > 1:
                    parts = lines[1].split()
                    if len(parts) >= 2:
                        self.cpu_count_physical = int(parts[0])
                        self.cpu_count_logical = int(parts[1])
            except Exception as e:
                # Fallback to standard lib if wmic fails
                import multiprocessing
                self.cpu_count_logical = multiprocessing.cpu_count()
                self.cpu_count_physical = self.cpu_count_logical # Best guess
        else:
            # Linux/Unix detection (for verification in sandbox or user fallback)
            try:
                # Try lscpu
                if shutil.which("lscpu"):
                    output = subprocess.check_output("lscpu", shell=True).decode()
                    for line in output.split('\n'):
                        if "Model name:" in line:
                            self.cpu_info = line.split(":", 1)[1].strip()
                        if "Core(s) per socket:" in line:
                            cores_per_socket = int(line.split(":", 1)[1].strip())
                            # Simplified: assuming 1 socket for most desktop setups or verify "Socket(s):"
                            # But let's just use multiprocessing for logical
                            self.cpu_count_physical = cores_per_socket # Rough estimate if 1 socket
                        if "Socket(s):" in line:
                            sockets = int(line.split(":", 1)[1].strip())
                            if self.cpu_count_physical > 0:
                                self.cpu_count_physical *= sockets

                if self.cpu_info == "Unknown CPU":
                     # /proc/cpuinfo fallback
                     with open("/proc/cpuinfo", "r") as f:
                         for line in f:
                             if "model name" in line:
                                 self.cpu_info = line.split(":", 1)[1].strip()
                                 break
            except:
                pass

            import multiprocessing
            self.cpu_count_logical = multiprocessing.cpu_count()
            if self.cpu_count_physical == 0:
                self.cpu_count_physical = self.cpu_count_logical # Fallback

    def _detect_gpu(self):
        """Detects GPU using nvidia-smi or OS specific commands."""
        # 1. Try nvidia-smi (Cross-platform if driver installed)
        if shutil.which("nvidia-smi"):
            try:
                # Get name
                output = subprocess.check_output("nvidia-smi --query-gpu=name --format=csv,noheader", shell=True).decode().strip()
                # Handle multiple GPUs (just take first or list all)
                gpus = output.split('\n')
                self.gpu_info = ", ".join([g.strip() for g in gpus])
                return
            except:
                pass

        # 2. OS Specific Fallbacks
        if platform.system() == "Windows":
            try:
                command = "wmic path win32_videocontroller get name"
                output = subprocess.check_output(command, shell=True).decode().strip()
                lines = output.split('\n')
                if len(lines) > 1:
                    # Filter out empty lines
                    gpus = [line.strip() for line in lines[1:] if line.strip()]
                    self.gpu_info = ", ".join(gpus)
            except:
                pass
        else:
            # Linux Fallback
            try:
                if shutil.which("lspci"):
                    output = subprocess.check_output("lspci | grep -i vga", shell=True).decode().strip()
                    if output:
                        # Extract basic info
                        self.gpu_info = output
            except:
                pass

    def get_summary(self):
        return {
            "OS": self.os_info,
            "CPU": self.cpu_info,
            "Physical Cores": self.cpu_count_physical,
            "Logical Cores": self.cpu_count_logical,
            "GPU": self.gpu_info
        }

if __name__ == "__main__":
    # Test
    sys = SystemInfo()
    print(sys.get_summary())
