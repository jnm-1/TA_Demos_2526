"""
Dummy slow task — used by the modal timer showcase.
This script simulates work that takes a few seconds (like SP baking).
It writes a result file when done.

Usage (called by the showcase addon via subprocess):
    python dummy_slow_task.py <output_file_path>
"""

import sys
import time


def main():
    if len(sys.argv) < 2:
        print("Usage: python dummy_slow_task.py <output_file_path>")
        sys.exit(1)

    output_path = sys.argv[1]
    print("Starting slow task...")

    # Simulate work (3 seconds)
    for i in range(1, 4):
        print(f"Working... step {i}/3")
        time.sleep(1)

    # Write a result file so the caller knows we're done
    with open(output_path, "w") as f:
        f.write("DONE\n")
        f.write(f"Completed at: {time.strftime('%H:%M:%S')}\n")

    print(f"Task complete! Result written to {output_path}")


if __name__ == "__main__":
    main()
