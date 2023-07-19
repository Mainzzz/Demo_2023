def build_parameter_map(file_path):
    parameter_map = {}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line.startswith("#") or not line:
                continue  # Skip comment lines or empty lines

            parts = line.split(':')
            if len(parts) == 5:
                param, data_type, var_type, var_range, resolution = map(str.strip, parts)
                if data_type == 'enum':
                    enum_values = [enum.strip().strip("'").split('-')[0].strip("'") for enum in var_range.split(',')]
                    parameter_map[param] = {
                        'DataType': data_type,
                        'Type': var_type,
                        'Range/Enums': {enum for enum in enum_values},
                        'Resolution': resolution
                    }
                else:
                    parameter_map[param] = {
                        'DataType': data_type,
                        'Type': var_type,
                        'Range/Enums': var_range,
                        'Resolution': resolution
                    }

    return parameter_map

