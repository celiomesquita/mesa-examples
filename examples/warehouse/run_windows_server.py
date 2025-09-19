#!/usr/bin/env python3
"""
Server script optimized for WSL -> Windows browser access.
"""

import subprocess
import sys

if __name__ == "__main__":
    print("Starting warehouse simulation server for Windows browser access...")

    # Get WSL IP
    try:
        result = subprocess.run(['ip', 'addr', 'show', 'eth0'],
                              capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'inet ' in line and '127.0.0.1' not in line:
                wsl_ip = line.split()[1].split('/')[0]
                break
        else:
            wsl_ip = "172.27.140.32"  # fallback
    except:
        wsl_ip = "172.27.140.32"  # fallback

    print(f"WSL IP detected: {wsl_ip}")
    print(f"Open your Windows browser to: http://{wsl_ip}:8765")
    print("Press Ctrl+C to stop the server")
    print("-" * 60)

    try:
        # Run solara with all interfaces bound
        subprocess.run([
            sys.executable, '-m', 'solara', 'run', 'app.py',
            '--host', '0.0.0.0',
            '--port', '8765',
            '--no-open',
            '--log-level', 'info'
        ], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Try: python simple_viz.py (matplotlib version)")
        print("2. Check Windows Firewall settings")
        print("3. Try a different port: --port 8080")