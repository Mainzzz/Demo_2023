import csv
import os
import re
import shutil
import cv_map as cm

csv_file = '.\DataFile\Data_Dictionary.csv'           # the path to Data Dictionary
para_file_path = '.\DataFile\parameters_HLSW1369.txt' # the path to parameters.txt
bif_file_name = ".\DataFile\TXDTS_DXF.BIF"            # the path to BIF file
tets_result_folder_path = '.\TestProcedure\\'         # the path to store test result
column_SysName = 4  # the column index of SysNamePhrase
column_CvtName = 1  # the column index of CvtName

parameter_map = None

#input :parameters.txt
#output:map of al the variables (name,datatype,value)
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
     
#Identify and extract all keys and statements of test cases in logic out file---currently not in use
def extract_key_statement(req_out_file_name):
    # file_name = 'output.txt'
    keys = {}
    statements = {}
    
    # Read the file
    with open(req_out_file_name, 'r') as file:
        content = file.readlines()

    # Remove leading/trailing whitespaces and newlines
    content = [line.strip() for line in content]
    # Find the start and end lines for the keys/statement section
    keys_start = None
    keys_end = None
    statement_start = None
    statement_end = None

    for i, line in enumerate(content):
        if line == "'Keys":
            keys_start = i + 1
        elif line == "'Statements":
            keys_end = i
            statement_start = i + 1
        elif line == "'Truth Table":
            statement_end = i
            break


    # Extract key variables and values
    keys_content = content[keys_start:keys_end]
    
    # Extract statement variables and values
    statement_content = content[statement_start:statement_end]
    
    # # Process keys section
    # for line in keys_content:
    #     if line and not (line.startswith("'") and (line.endswith("-") or line[1:].strip() == "")):
    #         variable, value = line.split('=')
    #         keys[variable.strip()] = value.strip()
            
    # Process keys section
    for line in keys_content:
        if line and not (line.startswith("'") and (line.endswith("-") or line[1:].strip() == "")):
            variable, value = line.split('=')
            variable = variable.split('-')[1].strip() # Remove leading single quote
            value = value.strip()
            keys[variable] = value 
             
     # Process statement section
    for line in statement_content:
        if line and not (line.startswith("'") and (line.endswith("-") or line[1:].strip() == "")):
            variable, value = line.split('SET')
            variable = variable.split(' - ')[1].strip() # Remove leading single quote
            value = value.strip()
            statements[variable] = value        

    # Print the key variables and values
    print("Keys:")
    for variable, value in keys.items():
        print(f"variable : {variable} - value : {value}")
        
    # Print the statement variables and values
    print("statements:")
    for variable, value in statements.items():
        print(f"variable : {variable} - value : {value}")

#split the whole test cases to single ones---not in use now  
def split_test_cases(req_out_file_name):
    hllsw_number = re.search(r'HLSW(\d+)', req_out_file_name).group()
    tc_list = []
    # Read the file
    with open(req_out_file_name, 'r') as file:
        content = file.readlines()

    # Remove leading/trailing whitespaces and newlines
    content = [line.strip() for line in content]

    test_numbers = []
    test_cases_section = False
    test_case_section = False
    count = 0
    test_case_number = None
    test_case_section_start_line = None
    test_case_section_end_line   = None
    # Iterate through the lines
    for i in range(len(content)):
        if content[i].startswith("'Test cases"):
            test_cases_section = True
        elif test_cases_section:
            
            if content[i].startswith("'Test cases"):
                break  # Break the loop when encountering the next "Test cases" line
            elif "'Test No." in content[i]:                
                # get start of test case section in test cases section
                if count == 0 :
                     test_case_section_start_line = i
                if test_case_section:
                    test_case_section_start_line = test_case_section_end_line
                if i+1 < len(content):
                    test_case_head_line = content[i+1]
                    # Extract the test case number
                    test_case_number = next((int(s) for s in test_case_head_line.split() if s.isdigit()), None)  # Extract the test case number
                    if test_case_number is not None:
                        test_numbers.append((test_case_number))
                        test_case_file_name = hllsw_number + '_TC_0' + str(test_case_number - 1 ) + ".txt"
                        if test_case_number >= 2 :
                            # get end of test case section in test cases section
                            test_case_section_end_line = i
                            count = test_case_number
                            test_case_section = True
                            # Copy the section to the new file
                            copy_file_section(req_out_file_name, 
                                              test_case_section_start_line, 
                                              test_case_section_end_line, 
                                              test_case_file_name)
                            tc_list.append(test_case_file_name)
    
                        else:
                            count = 1
    
    # Print the identified test numbers
    print("Identified Test Numbers:")
    for test_case_number in test_numbers:
        print(f"Test Case No. {test_case_number}")
        
    return tc_list

# input  : logic file with truth table and test cases generated by Logic Parser
# output : tc_select_index - the useful test cases index in the current file to generate single test case
def identify_test_case(req_out_file_name):
    with open(req_out_file_name, 'r') as file:
        content = file.readlines()

    # Remove leading/trailing whitespaces and newlines
    content = [line.strip() for line in content]
    #create a list to store the index of lines that contain the keyword 'Test No.'
    keyword = 'Test No.'
    tc_lines_index = [index for index, line in enumerate(content) if keyword in line]
    # Add the end of file line index to the list
    tc_lines_index.append(len(content) - 1)
    p_start = None
    p_end   = None
    tc_select_index = []
    # Iterate over the line indices and check for 'SET' between p_start and p_end
    for i in range(len(tc_lines_index) - 1):
        p_start = tc_lines_index[i]
        p_end = tc_lines_index[i+1]

        # Check if 'SET' is found between p_start and p_end
        find_set_flag = any("SET" in line for line in content[p_start:p_end])

        if find_set_flag:
            # Perform desired actions when 'SET' keyword is found
            tc_select_index.append(p_start)
            tc_select_index.append(p_end)
            
    tc_select_index = list(set(tc_select_index))    
    return tc_select_index
 
# input  :   useful test cases index and logic file name
# output :   single test cases file name   
def copy_tc_section(req_out_file_name, tc_select_line_index):
    hllsw_number = re.search(r'HLSW(\d+)', req_out_file_name).group()
    tc_name_list = []   
    # Read the current file
    with open(req_out_file_name, 'r') as file:
        content = file.readlines()
        
    p_start = None
    p_end   = None
    tc_counter = None
    for i in range(len(tc_select_line_index) - 1):
        p_start = tc_select_line_index[i]
        p_end = tc_select_line_index[i+1]
        tc_counter = i+1
        
        filename = hllsw_number + '_TC_0' + str(tc_counter) + ".txt"
        tc_file_name = os.path.join(tets_result_folder_path, filename)
        # tc_file_name = hllsw_number + '_TC_0' + str(tc_counter) + ".txt"
        tc_name_list.append(tc_file_name)      
        # Extract the desired section of lines
        section = content[p_start - 1:p_end]  
        # Write the section to the new file
        with open(tc_file_name, 'w') as new_file:
            new_file.writelines(section)

        print(f"Section copied from line {p_start} to line {p_end} to {tc_file_name}.")  
    return tc_name_list       
          
#copy test case from test cases, not select useful test case ----not in use now         
def copy_file_section(req_out_file_name, start_line, end_line, new_file_name):
    # Read the current file
    with open(req_out_file_name, 'r') as file:
        content = file.readlines()

    # Extract the desired section of lines
    section = content[start_line - 1:end_line]

    # Write the section to the new file
    with open(new_file_name, 'w') as new_file:
        new_file.writelines(section)

    print(f"Section copied from line {start_line} to line {end_line} to {new_file_name}.")
       
  
# input  : keys and parameter_map
# output : tp_keys matched with keys according to parameter_map
def test_case_keys_map_param(keys,parameter_map):
    tp_variable = {}

    # Loop through keys and assign values to variables
    for variable, value in keys.items():
        if variable not in parameter_map:
            # Skip variables not present in the parameter_map
            print("Skip variables not present in the parameter map")
            continue
        
        variable_details = parameter_map[variable]
        data_type = variable_details['DataType']

        # Assign value to the actual variable tp
        if data_type != 'enum':
            tp_variable[variable] = value
        else:
            value_int = int(value) 
            enum_range = list(variable_details['Range/Enums'])
            if value_int < len(enum_range):
                tp_variable[variable] = enum_range[value_int]
            else:
                # Handle invalid enum value
                tp_variable[variable] = None

    return tp_variable

# input  : single test case file name
# output : keys, statements in test case file
def read_test_case_file(test_case_file_name):
    keys = {}
    statements = {}
    # Read the file
    with open(test_case_file_name, 'r') as file:
        content = file.readlines()
    # Process statement section
    for line in range(len(content)):
        # Remove "//" comments from each line
        content[line] = content[line].split("//")[0].strip()
        if " : " in content[line]: 
            key_variable, key_value = content[line].split(' : ')
            variable = key_variable.strip() # Remove leading single quote
            value = key_value.strip()
            keys[variable] = value 
        elif "SET" in content[line]: 
            statement_variable, statement_value = content[line].split(' SET ')
            variable = statement_variable.strip() # Remove leading single quote
            value = statement_value.strip()
            statements[variable] = value
    return keys, statements                          

#add "//" to all existing lines in test case file
def add_comments_to_test_case_file(test_case_file_name):
    try:
        # Read the contents of the file
        with open(test_case_file_name, 'r') as file:
            lines = file.readlines()
        
        # Modify the lines by adding "//" to the beginning
        modified_lines = ['//' + line.strip() for line in lines]
        modified_lines.append('\n')
        # Write the modified lines back to the file
        with open(test_case_file_name, 'w') as file:
            file.write('\n'.join(modified_lines))
        
        print(f"Comments added successfully to '{test_case_file_name}'.")
    
    except FileNotFoundError:
        print(f"File '{test_case_file_name}' not found.")

# input  : tp_keys (label type variables) and bif file to find signal names
# output : formatted commands to set signals
def find_signal_in_bif(bif_file_name, tp_keys):
    signals = []
    commands = []
    with open(bif_file_name, 'r') as bif_file:
        for line in bif_file:
            line = line.strip()
            for variable, value in tp_keys.items():
                if "Label" in variable:
                    sig_variable = variable.replace(variable, " LABEL " + variable.split('_')[1])
                    if sig_variable in line and "SIG" in line and " OUT " in line:
                        signal_name = line.split("SIG")[1].split()[0].strip()
                        print("Found signal:", signal_name,"of variable:" ,variable)
                        signals.append(signal_name)
                        if value == 'INVALID':
                            sig_value = 'fw'
                            comments = "//Set {} {}".format(variable, value)
                            commands.append(comments)
                            command = "set {} {} \n".format(signal_name, sig_value)
                            commands.append(command)
                            # space_line = "\n"
                            # commands.append(space_line)
    return commands

# input  : single test_case_file_name and commands to set signals
# output : single test_procedure_file_name converted by test case with commands added
def update_test_case2procedure(test_case_file_name,commands):
    tp_file_name = test_case_file_name.rsplit(".", 1)[0] + "_procedure.bts"
    shutil.copy(test_case_file_name, tp_file_name)
    with open(tp_file_name, 'a') as test_procedure_file:
        for command in commands:
            test_procedure_file.write(command + '\n')
    print("Test case updated and converted to executable procedure. File renamed to:", tp_file_name)
    return tp_file_name

#add test verify command into test procedure --------------lable way   
# input  : single test_procedure_file_name and tp_statements(output to verify)
# output : no output - just update the single test_procedure_file     
def add_verify_in_tp(tp_file_name,tp_statements):
    verify_commands = []
    for variable, value in tp_statements.items():
        tcas_out_variable = variable.replace('_', ' ')
        tcas_out_cv_name = find_CvtName(csv_file, tcas_out_variable, column_SysName, column_CvtName)
        if tcas_out_cv_name is not None:
            print(f"Found variable CvtName: {tcas_out_cv_name}")
            delay_line = "DELAY 1000"
            verify_commands.append(delay_line)
            verify_line = "test if " + tcas_out_cv_name + " EQ " + value  
            verify_commands.append(verify_line)
            with open(tp_file_name, 'a') as tp_file:
                for command in verify_commands:
                    tp_file.write(command + '\n')
        else:
            print("TCAS Variable CvtName to verify not found.")
        
#add test verify command into test procedure  --------------cv way--not use now        
def generate_test_verify_file(verify_file_name,variable):
    tcas_out_variable = variable
    tcas_out_cv_name = find_CvtName(csv_file, tcas_out_variable, column_SysName, column_CvtName)
    if tcas_out_cv_name is not None:
        print(f"Found variable CvtName: {tcas_out_cv_name}")
        line = "cxr " + tcas_out_cv_name  # Create the line to be written to the file
        with open(verify_file_name, 'w') as output_file:
            output_file.write(line)
            print("Line written to file.")
    else:
        print("Variable CvtName not found.")
    


#match tcas output with 
# input  : Data Dictionary csv file and two corresponding column to map cv name, tcas output variable in req to test,
# output : cv name which matched tcas output variable in req
def find_CvtName(csv_file, tcas_out_variable, column_SysName, column_CvtName):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[column_SysName] == tcas_out_variable:
                return row[column_CvtName]
    return None


def main():
    #####@Example usage  
    
    req_out_file_name = ".\DataFile\Logic_out_HLSW1369.txt"
    ## extract_key_statement(file_name)
    tp_index = identify_test_case(req_out_file_name)
    tc_list = copy_tc_section(req_out_file_name, tp_index)
    # tc_file_list = split_test_cases(req_out_file_name)
    for tc_file in tc_list:
        keys, statements = read_test_case_file(tc_file)
        print(keys) 
        if keys != {}:    
            parameter_map = build_parameter_map(para_file_path)
            tp_keys = test_case_keys_map_param(keys,parameter_map)
            print(tp_keys)   
            
            # Example usage
            add_comments_to_test_case_file(tc_file)
            
            tp_statements = statements
            commands = find_signal_in_bif(bif_file_name, tp_keys)    
            tp_file_name = update_test_case2procedure(tc_file,commands)
            add_verify_in_tp(tp_file_name,tp_statements)
        else:
            with open(tc_file, 'a') as tp_file:
                note = "There are no input and output variables in current test case."
                tp_file.write(note + '\n')
            print(tc_file + " is not excutable!")
    
if __name__ == '__main__':
    main()