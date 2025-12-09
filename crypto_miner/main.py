import sys
import time
# Changed to standard imports to support direct execution like `python main.py`
try:
    from hardware_manager import SystemInfo
    from miner_engine import MulticoreMiner
    from benchmark_tool import Benchmark, SystemMonitor
    from utils import clear_screen, print_header, print_table_row, wait_for_enter
except ImportError:
    # Fallback if run as package
    from .hardware_manager import SystemInfo
    from .miner_engine import MulticoreMiner
    from .benchmark_tool import Benchmark, SystemMonitor
    from .utils import clear_screen, print_header, print_table_row, wait_for_enter

def main_menu():
    while True:
        clear_screen()
        print_header("Crypto Mining Simulator & Benchmark Tool")
        print("\n1. View System Hardware")
        print("2. Run Benchmark (CPU & GPU Detection)")
        print("3. Start Mining Simulation")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == '1':
            show_hardware()
        elif choice == '2':
            run_benchmark()
        elif choice == '3':
            start_mining()
        elif choice == '4':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")
            time.sleep(1)

def show_hardware():
    clear_screen()
    print_header("System Hardware Information")

    print("\nDetecting hardware... Please wait.")
    sys_info = SystemInfo().get_summary()

    print("\n")
    print_table_row("Component", "Details")
    print("-" * 60)
    print_table_row("OS", sys_info['OS'])
    print_table_row("CPU", sys_info['CPU'])
    print_table_row("Physical Cores", str(sys_info['Physical Cores']))
    print_table_row("Logical Cores", str(sys_info['Logical Cores']))
    print_table_row("GPU", sys_info['GPU'])

    wait_for_enter()

def run_benchmark():
    clear_screen()
    print_header("Performance Benchmark")

    print("\nThis test will measure your system's hashing power.")
    print("It will check Single-Core and Multi-Core performance.")
    print("System stats will be monitored in the background.")
    input("\nPress Enter to start benchmark...")

    bench = Benchmark()

    print("\nRunning Single-Core Test (5s)...")
    sc_score = bench.run_single_core_test(duration=5)
    print(f"Result: {sc_score:,.2f} H/s")

    print("\nRunning Multi-Core Test (5s)...")
    mc_score = bench.run_multi_core_test(duration=5)
    print(f"Result: {mc_score:,.2f} H/s")

    print("\nGenerating detailed report...")
    filename = bench.generate_report()
    print(f"Report saved to: {filename}")

    wait_for_enter()

def start_mining():
    clear_screen()
    print_header("Mining Simulation")

    print("\nConfigure your mining block:")
    block_data = input("Enter block data (default: 'sim_block_1'): ").strip()
    if not block_data:
        block_data = "sim_block_1"

    try:
        difficulty = int(input("Enter difficulty (number of leading zeros, e.g. 4-7): "))
    except ValueError:
        print("Invalid input, defaulting to 4.")
        difficulty = 4

    print(f"\nMining block '{block_data}' with difficulty {difficulty}...")
    print("Initializing workers and system monitor...")

    # Start Monitor
    monitor = SystemMonitor()
    monitor.start()

    miner = MulticoreMiner()
    nonce, block_hash, duration = miner.mine(block_data, difficulty)

    # Stop Monitor
    monitor.stop()

    print("\n" + "="*60)
    if nonce is not None:
        print("BLOCK FOUND!")
        print(f"Nonce:      {nonce}")
        print(f"Hash:       {block_hash}")
        print(f"Time Taken: {duration:.4f} seconds")
        print(f"Approx H/s: {(nonce/duration):,.2f}") # Simplified calc
    else:
        print("Mining ended without finding a block (search space exhausted).")
    print("="*60)

    # Save Mining Report
    report_file = "mining_report.txt"
    print(f"\nSaving mining stats to {report_file}...")
    with open(report_file, "w") as f:
        f.write("Crypto Mining Simulation Report\n")
        f.write("===============================\n\n")
        f.write(f"Block Data: {block_data}\n")
        f.write(f"Difficulty: {difficulty}\n")
        if nonce is not None:
             f.write(f"Result:     SUCCESS\n")
             f.write(f"Nonce:      {nonce}\n")
             f.write(f"Hash:       {block_hash}\n")
             f.write(f"Time Taken: {duration:.4f} s\n")
        else:
             f.write(f"Result:     FAILED (Not found in range)\n")

        f.write("\n")
        monitor.generate_log_section(f)

    wait_for_enter()

if __name__ == "__main__":
    # Ensure multiprocessing works correctly on Windows
    import multiprocessing
    multiprocessing.freeze_support()
    main_menu()
