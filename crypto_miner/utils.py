import os
import platform

def clear_screen():
    """Clears the console screen based on the operating system."""
    system_os = platform.system()
    if system_os == "Windows":
        os.system("cls")
    else:
        # Linux and macOS
        os.system("clear")

def print_header(text, width=60):
    """Prints a formatted header."""
    print("=" * width)
    print(f"{text.center(width)}")
    print("=" * width)

def print_table_row(col1, col2, width=60):
    """Prints a formatted row with two columns."""
    col_width = width // 2
    print(f"{col1:<{col_width}}{col2:>{col_width-1}}")

def wait_for_enter():
    """Pauses execution until the user presses Enter."""
    input("\nPress Enter to continue...")
