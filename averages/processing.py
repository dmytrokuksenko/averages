"""
A collection of supplemental functions for processing the DAT file. 

Author: Dmytro Kuksenko
Date: Sept 19, 2022
"""

import re
import numpy as np


def get_header(header, line):

    names = header.match(line)
    var = names.group(1).replace(" ", "")
    var_name = var.split("(")[0]
    components = re.findall(r"\(.*?\)", var)
    num_components = len(components[0].split(","))
    set_name = names.group(2)
    increment = float(names.group(3))
    print(f"Set: {set_name}, Variable: {var_name}, Time Increment: {increment}")

    return var_name, num_components, set_name, increment


def string_to_digits(str):

    for i in range(len(str)):
        if str[i].isdigit():
            reduced = str[i:]
            break
    temp = reduced.replace("\n", "").split(" ")

    digits = [float(x) for x in temp if x]

    return digits


def calculate_averages(data, name):

    print(f"\nThe components of {name}...")

    if name in  ["stresses", "strains"]:
        averages = [
            np.sum(data[:, i] / len(data[:, i])) for i in range(2, data.shape[1])
        ]

    elif name == "volume":
        averages = [np.sum(data[:, 1])]

    else:
        averages = [
            np.sum(data[:, i] / len(data[:, i])) for i in range(1, data.shape[1])
        ]

    return np.array(averages)


def min_max_values(data, name):

    temp = np.array(data)
    max_vals = np.amax(temp, where=[True] * temp.shape[1], initial=-1, axis=0)
    print(np.average(max_vals))
    print(f"The maximum values around each columns for {name} are:")
    for i, max_val in enumerate(max_vals):
        print(i, max_val)


def print_averages(data):

    for key, val in data.items():
        if key == "stresses":
            print("\n")
            for i, item in enumerate(val):
                print(f"Average sigma {i+1,i+1} equals {item:.2f}")
        elif key == "strains":
            print("\n")
            for i, item in enumerate(val):
                print(f"Average epsilon {i+1,i+1} equals {item:.8f}")
        elif key == "volume":
            print("\n")
            print(f"\nThe volume of the set is {val[0]}")
        else:
            print("\nNo calculated averages have been detected!")


def match_lines(header, file):

    start_flag = 0
    empty_line = 0
    lines = []
    data = {}

    for line in file:

        if re.match(header, line):
            var_name, _, _, _ = get_header(header, line)
            start_flag = 1
        else:
            if start_flag == 1:
                if len("".join(line.split())) == 0:
                    empty_line += 1
                    if empty_line >= 2:
                        empty_line, start_flag = 0, 0
                        data[var_name] = np.array(lines)
                        lines.clear()
                else:
                    lines.append(string_to_digits(line))

    if lines:
        data[var_name] = np.array(lines)

    return data


def min_max_value(key, val):
    print(f"\nCalculating max\min {key}")
    for i in range(2, val.shape[1]):
        print(f"\nMax: {np.max(val[:, i])} and Min: {np.min(val[:, i])}")