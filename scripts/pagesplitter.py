#!/bin/python

# Import from parent directory: https://www.geeksforgeeks.org/python-import-from-parent-directory/
import sys

# Add scripts directory in parent directory to path
sys.path.append("../utils")

from lecture_specific import alag_pdf

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pagesplitter.py input.pdf [output.pdf]")
        sys.exit(1)

    # If output file is same as input file, it will be modified in place
    if len(sys.argv) == 2:
        alag_pdf(sys.argv[1], sys.argv[1])
    else:
        alag_pdf(sys.argv[1], sys.argv[2])

