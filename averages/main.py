"""
Extracts average values in the components.

Author: Dmytro Kuksenko
Date: Sept 6, 2022
"""

import re
import time
import numpy as np
import matplotlib.pyplot as plt
import json

from failure import mises_stress
from averages import (
    get_header,
    match_lines,
    calculate_averages,
    min_max_value,
    print_averages,
)


if __name__ == "__main__":

    start = time.time()

    with open("averages/config.json") as file:
        config = json.load(file)
    
    
    with open(config['file name']) as f:
        file = f.readlines()
    
    
    header = re.compile(" (.+)for .*set\\s(\\S+) and time  (.+)")

    data = match_lines(header, file)

    averages = {}

    for key, val in data.items():
        averages[key] = calculate_averages(val, key)
        if key in ["stresses"]:
            mises = mises_stress(val[:, 2:])
            min_max_value(key, val)

    print_averages(averages)

    end = time.time()
    duration = end - start

    print(f"\nThe execution time is {duration:1f} (s)")
