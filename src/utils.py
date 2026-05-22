import subprocess
import os


def clear_screen():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)


def print_banner():
    print("""
╔══════════════════════════════════════╗
║          R P G   E N G I N E         ║
║         Python Final Project         ║
╚══════════════════════════════════════╝""")


def print_divider():
    print("-" * 40)
