import os
import json
import re
import string


# Define the regex patterns
pattern1 = r'^\s*(\d+)\s+(\d+)\s+(\S+)\s+([\d.-]+)\s+(\d+)\s*$'
pattern2 = r'^\s*(\S+)\s+(\S+)\s+(\S+)\s+([\d.-]+)\s*$'
pattern3 = r'^\s*(\S+)\s*[:,\s]\s*([\d.-]+)\s*$'
pattern4 = r'(\w+)\s*:\s*([\d\.]+),?'

import re
import os


def filter_blacklisted(params):
    blacklist = []
    with open('blacklist.txt', 'r') as f:
        blacklist = f.read().splitlines()
        print(blacklist)

    # filter json_data by checking if they keys contain any of the lines in blacklist.txt
    return {k: v for k, v in params.items() if not any(x in k for x in blacklist)}


def parse_file(file_path, included_files=None):
    if included_files is None:
        included_files = set()
    elif file_path in included_files:
        return {}  # Avoid circular includes

    included_files.add(file_path)
    file_params = {}

    pattern4 = r'(\w+)\s*:\s*([\d\.]+),?'

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Ignore comments
            if line.startswith('#') or line.startswith('//'):
                continue
            # Check for include directive
            if line.startswith('%include'):
                included_file = line.split(' ')[1].strip("'").strip('"')
                included_file_path = os.path.normpath(os.path.join(os.path.dirname(file_path), included_file))
                if included_file_path not in included_files and os.path.isfile(included_file_path):
                    included_params = parse_file(included_file_path, included_files)
                    print(f"Included {len(included_params)} parameters from {included_file_path}")
                    file_params.update(included_params)
            else:
                match1 = re.match(pattern1, line)
                match2 = re.match(pattern2, line)
                match3 = re.match(pattern3, line)
                match4 = re.match(pattern4, line)  # New match for 'MNT_TYPE: 1,' format
                if match1:
                    key = sanitize_key(match1.group(3))
                    file_params[key] = float(match1.group(4))
                elif match2:
                    key = sanitize_key(match2.group(3))
                    file_params[key] = float(match2.group(4))
                elif match3:
                    key = sanitize_key(match3.group(1))
                    value = match3.group(2).strip()
                    try:
                        file_params[key] = float(value)
                    except ValueError:
                        file_params[key] = value
                elif match4:  # Handle match4
                    key = sanitize_key(match4.group(1))
                    try:
                        file_params[key] = float(match4.group(2))
                    except ValueError:
                        file_params[key] = match4.group(2)
                else:
                    print(f"Unmatched line in {file_path}: '{line}'")
    return filter_blacklisted(file_params)



def sanitize_key(key):
    allowed_chars = string.ascii_letters + string.digits + '_'
    return ''.join(c for c in key if c in allowed_chars)

# Start at the root directory and walk the directory tree
root_directory = os.getcwd()  # Get current directory
json_data = {}
for dirpath, dirnames, filenames in os.walk(root_directory):
    for filename in filenames:
        if filename.endswith('.params'):
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, root_directory)
            file_params = parse_file(file_path)
            json_data[relative_path] = file_params

# Save the json_data to a JSON file
with open('params_v1.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)
