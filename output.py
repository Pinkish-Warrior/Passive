# Handles writing results to sequentially named files inside the output/ folder.
# First run writes to output/result.txt, subsequent runs to result2.txt, result3.txt, etc.

import os

OUTPUT_DIR = "output"


def save_result(content: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename = os.path.join(OUTPUT_DIR, "result.txt")
    n = 2
    # Increment the suffix until we find a filename that doesn't exist yet
    while os.path.exists(filename):
        filename = os.path.join(OUTPUT_DIR, f"result{n}.txt")
        n += 1

    with open(filename, "w") as f:
        f.write(content + "\n")

    return filename
