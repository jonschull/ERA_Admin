import subprocess
import sys
import time
import os
import fcntl

# The command to run the main analysis script
COMMAND_TO_RUN = [sys.executable, "-u", "batch_analyze_calls.py"]
# If no output is received for this many seconds, restart the script
INACTIVITY_TIMEOUT = 300  # 5 minutes

def run_and_monitor():
    """Runs the batch analysis script as a subprocess and monitors it for inactivity."""
    while True:
        print("\n" + "="*60)
        print(f"Starting batch_analyze_calls.py at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)

        process = subprocess.Popen(
            COMMAND_TO_RUN,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line-buffered
            universal_newlines=True
        )

        # Set up non-blocking reads for stdout
        fd = process.stdout.fileno()
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        last_output_time = time.time()

        while True:
            try:
                # Non-blocking read
                try:
                    line = process.stdout.readline()
                    if line:
                        print(line, end='')
                        last_output_time = time.time()
                except (IOError, TypeError):
                    # This can happen if the read is attempted when no data is available
                    pass

                # Check if process has finished
                if process.poll() is not None:
                    break
                
                # Check for timeout
                if time.time() - last_output_time > INACTIVITY_TIMEOUT:
                    print("\n" + "!"*60)
                    print(f"WATCHDOG: No output for {INACTIVITY_TIMEOUT} seconds. Restarting script...")
                    print("!"*60)
                    process.kill()
                    break # Break inner loop to restart the process

                time.sleep(0.1) # A small sleep to prevent busy-waiting
            
            except Exception as e:
                print(f"WATCHDOG: An unexpected error occurred: {e}")
                process.kill()
                break

        # Check exit code
        exit_code = process.poll()
        if exit_code == 0:
            print("\n" + "*"*60)
            print("WATCHDOG: Script finished successfully.")
            print(""*60)
            break # Exit the outer while loop
        elif exit_code is None: # This means we broke due to timeout
            print("WATCHDOG: Preparing to restart after timeout...")
            time.sleep(5) # Brief pause before restarting
        else:
            print("\n" + "!"*60)
            print(f"WATCHDOG: Script exited with an error (code {exit_code}). Restarting...")
            print("!"*60)
            time.sleep(5)

if __name__ == "__main__":
    run_and_monitor()
