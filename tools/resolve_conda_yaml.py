#!/usr/bin/env python3

import yaml
import subprocess
import sys
import os

def get_conda_list() -> dict:
    """Get the list of currently installed packages and their versions."""
    conda_list_output = subprocess.check_output(['mamba', 'list']).decode('utf-8')
    installed_packages = {}
    
    for line in conda_list_output.split('\n')[3:]:  # Skip the first three lines
        if line:
            parts = line.split()
            if len(parts) >= 2:
                package_name = parts[0]
                package_version = parts[1]
                installed_packages[package_name] = package_version
    
    return installed_packages

def update_yaml_with_versions(yaml_contents: str, installed_packages: dict) -> str:
    """Update the YAML contents with the installed package versions."""
    yaml_data = yaml.safe_load(yaml_contents)
    
    updated_dependencies = []
    for dep in yaml_data['dependencies']:
        if isinstance(dep, str) and dep in installed_packages:
            updated_dependencies.append(f"{dep}={installed_packages[dep]}")
        elif isinstance(dep, dict) and 'pip' in dep:
            updated_dependencies.append(dep)
        else:
            updated_dependencies.append(dep)
    
    yaml_data['dependencies'] = updated_dependencies
    
    return yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)

def main(input_file: str, output_file: str):
    # Read the contents of the uploaded YAML file
    with open(input_file, 'r') as file:
        yaml_contents = file.read()

    # Get the installed package versions
    installed_packages = get_conda_list()

    # Update the YAML contents with the package versions
    updated_yaml_contents = update_yaml_with_versions(yaml_contents, installed_packages)

    # Write the updated contents to a new YAML file
    with open(output_file, 'w') as file:
        file.write(updated_yaml_contents)

    print(f"Updated YAML file written to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: update_conda_yaml.py <input_yaml_file> <output_yaml_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    main(input_file, output_file)

