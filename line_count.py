import plotly.express as px
import pandas as pd
import subprocess
import os

# params file with variable path = 'foo/bar'
from line_count_params import path

try:
    os.chdir(path)
    print("Current working directory: {0}".format(os.getcwd()))
except FileNotFoundError:
    print("Directory: {0} does not exist".format(path))
except NotADirectoryError:
    print("{0} is not a directory".format(path))
except PermissionError:
    print("You do not have permissions to change to {0}".format(path))


file_extensions = [".sh",".py",".feature"]

names = []
counts = []
types = []

for file_extension in file_extensions:

    raw_output = subprocess.check_output(
        "find . -name '*{}' | xargs wc -l".format(file_extension), shell=True)


    string_output = str(raw_output)

    split_lines = string_output.split("   ")
    total = split_lines[-1]
    split_lines = split_lines[:-1]

    line_count_sum = 0


    excluded_files = ["config.py", ]

    for line in split_lines:

        stripped_line = line.strip()
        stripped_line.replace(r"\n", "")

        if ((r"\n") in stripped_line):
            stripped_line = stripped_line[:-2]

        if stripped_line != "":
            count_and_name = stripped_line.split(" ")
            if len(count_and_name) > 1:
                count = int(count_and_name[0])
                path = count_and_name[1]
                address = path.split("/")
                name = address[-1]
                print("Name: {:50}, Count: {:10}".format(name, count))
                line_count_sum += (count)

                if name not in excluded_files:
                    names.append(name)
                    counts.append(count)
                    types.append(file_extension)

print("Caclulated sum: {}".format(line_count_sum))
print("Actual Total {}".format(total))


d = {'Name': names, 'Line Count': counts, "Type": types}
df = pd.DataFrame(data=d)
df = df.sort_values(by=['Line Count'])
print(df)

fig = px.bar(df, x='Name', y='Line Count', color="Type")
# fig.show()

fig = px.pie(df, values='Line Count', names='Name',)
fig.show()
