import plotly.express as px
import pandas as pd
import subprocess
import os

# params file with variable path = 'foo/bar'
from line_count_params import path


print("Changing the directory to {}".format(path))
try:
    os.chdir(path)
    print("Current working directory: {0}".format(os.getcwd()))
except FileNotFoundError:
    print("Directory: {0} does not exist".format(path))
except NotADirectoryError:
    print("{0} is not a directory".format(path))
except PermissionError:
    print("You do not have permissions to change to {0}".format(path))


# File extensions to be counted
file_extensions = [".sh", ".py", ".feature"]

names = []
counts = []
types = []

# For loop searches for each type of file
for file_extension in file_extensions:
    line_count_sum = 0

    raw_output = subprocess.check_output(
        "find . -name '*{}' | xargs wc -l".format(file_extension), shell=True)

    # Converts terminal output to string"
    string_output = str(raw_output)
    split_lines = string_output.split("   ")
    total = split_lines[-1]
    split_lines = split_lines[:-1]

    # List of files to exclude from the count
    excluded_files = ["config.py", ]

    # Goes through each line in the find command's output
    for line in split_lines:

        stripped_line = line.strip()
        stripped_line.replace(r"\n", "")

        # Removes the new line chars from output
        if ((r"\n") in stripped_line):
            stripped_line = stripped_line[:-2]

        # Splits the line if not empty string
        if stripped_line != "":
            count_and_name = stripped_line.split(" ")
            if len(count_and_name) > 1:
                count = int(count_and_name[0])
                path = count_and_name[1]
                address = path.split("/")
                name = address[-1]
                print("Name: {:50}, Count: {:10}".format(name, count))
                line_count_sum += (count)

                # Adds metrics to lists which will create dataframe
                if name not in excluded_files:
                    names.append(name)
                    counts.append(count)
                    types.append(file_extension)

    # Check to see if all lines accounted for
    print("Caclulated sum: {}".format(line_count_sum))
    print("Actual Total {}".format(total))

# Turns list into dataframe
file_line_data = {'Name': names, 'Line Count': counts, "Type": types}
line_count_df = pd.DataFrame(data=file_line_data)
line_count_df = line_count_df.sort_values(by=['Line Count'])
print(line_count_df)

# Bar chart of different files and thier line count
fig = px.bar(line_count_df, x='Name', y='Line Count', color="Type")
fig.show()

# Pie chart of different file types and thier sum line count
fig = px.pie(line_count_df, values='Line Count', names='Type',)
fig.show()
