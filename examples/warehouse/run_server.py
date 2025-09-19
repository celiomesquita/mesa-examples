#!/usr/bin/env python3
"""
Alternative way to run the warehouse simulation server.
This bypasses potential WSL networking issues with the Solara CLI.
"""

import subprocess
import sys
import os

if __name__ == "__main__":
    print("Starting warehouse simulation server...")
    print("This will start the server on http://0.0.0.0:8765")
    print("Access it via http://localhost:8765 or http://127.0.0.1:8765")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)

    try:
        # Run solara with explicit host binding
        subprocess.run([
            sys.executable, '-m', 'solara', 'run', 'app.py',
            '--host', '0.0.0.0',
            '--port', '8765',
            '--no-open'
        ], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Server failed to start: {e}")
        print("Try running: solara run app.py --host 0.0.0.0 --port 8765 --no-open")
    except Exception as e:
        print(f"Unexpected error: {e}")