import csv
import json
import os
import re
from TCAS_IO_Utility import TCAS_IO_Utility

column_SysName = 4  # the column index of SysNamePhrase in Data_Dictionary.csv
column_CvtName = 1  # the column index of CvtName in Data_Dictionary.csv

class LogicFileProcessor:
    def __init__(self):
        ablolute_directory = os.path.dirname(os.path.abspath(__file__))
        self.logic_file_path = os.path.join(ablolute_directory, 'DataFile', 'Logic_Out0.txt')
        self.parameter_file_path = os.path.join(ablolute_directory, 'DataFile', 'parameters.txt')
        self.command_file_path = os.path.join(ablolute_directory, 'DataFile', 'common_commands.json')
        self.bif_file_path = os.path.join(ablolute_directory, 'DataFile', 'TXDTS_DXF.BIF')
        self.csv_file_path = os.path.join(ablolute_directory, 'DataFile', 'Data_Dictionary.csv')
        # self.tp_folder_path = '.\NewTestProcedure'         
        self.req_num = None
        self.tp_file_name = os.path.join(ablolute_directory, 'NewTestProcedure', 'TCAS_RBLT_TestProcedure.bts')            
        self.parameter_map = {}  
        self.bif_map = {}
        self.selected_tc_index = []
        self.TCGroup = {}  
        self.TPDescription = {}
        self.keys = {}
        self.statements = {}
        
    def load_commands(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)    
        
    def build_parameter_map(self):
        with open(self.parameter_file_path, 'r') as file:
            for line in file:
                line = line.strip()  
                if line.startswith("#") or not line:
                    continue 
                parts = line.split(':')
                if len(parts) == 5:
                    param, data_type, var_type, var_range, resolution = map(str.strip, parts)
                    if data_type == 'enum':
                        enum_values = [enum.strip().strip("'").split('-')[0].strip("'") for enum in var_range.split(',')]
                        self.parameter_map[param] = {
                            'DataType': data_type,
                            'Type': var_type,
                            'Range/Enums': enum_values,
                            'Resolution': resolution
                        }
                    else:
                        self.parameter_map[param] = {
                            'DataType': data_type,
                            'Type': var_type,
                            'Range/Enums': var_range,
                            'Resolution': resolution
                        }

    def buid_BIF_map(self):
        bif_keyword_index = []
        with open(self.bif_file_path, 'r') as bif_file:
            lines = bif_file.readlines()
            for index, line in enumerate(lines):
                line = line.strip()
                if ("SIG" in line and 
                    " OUT " in line and 
                    "LABEL" in line and 
                    "BITS" not in line):
                    bif_signal_name = line.split("SIG")[1].split()[0].strip()
                    bif_var_name = "Label " + line.split("LABEL")[1].split()[0].strip()
                    self.bif_map[bif_var_name] = {'signal': bif_signal_name}
                    bif_keyword_index.append(index)
     
    def remove_duplicates_preserve_order(self,arr):
        seen = set()
        result = []
        for num in arr:
            if num not in seen:
                seen.add(num)
                result.append(num)
        return result
           
    def select_lines_contains_useful_tc(self):
        with open(self.logic_file_path, 'r') as file:
            content = file.readlines()
        content = [line.strip() for line in content]
        keyword = 'Test No.'
        tc_lines_index = [index for index, line in enumerate(content) if keyword in line]
        tc_lines_index.append(len(content) - 1)
        p_start = None
        p_end   = None
        for i in range(len(tc_lines_index) - 1):
            p_start = tc_lines_index[i]
            p_end = tc_lines_index[i+1]
            find_set_flag = any("set" in line for line in content[p_start:p_end])
            if find_set_flag:
                self.selected_tc_index.append(p_start)
                self.selected_tc_index.append(p_end)
        print("selected_tc_index1:", self.selected_tc_index)  
        self.selected_tc_index = self.remove_duplicates_preserve_order(self.selected_tc_index)  
        print("selected_tc_index2:", self.selected_tc_index) 
    
    
    def save_TCGroup(self):
        # self.req_num = re.search(r'HLSW(\d+)', self.logic_file_path).group()
        with open(self.logic_file_path, 'r') as file:
            content = file.readlines()
        p_start = None
        p_end   = None
        tc_counter = None
        for i in range(len(self.selected_tc_index) - 1):
            p_start = self.selected_tc_index[i]
            p_end = self.selected_tc_index[i+1]
            tc_counter = i+1
            tc_name = self.tp_file_name + str(tc_counter)
            # tc_file_name = os.path.join(self.file_path, tc_name)
            section = content[p_start - 1:p_end]  
            self.TCGroup[tc_name] = {}
            self.TCGroup[tc_name]['section'] = section  
            print(f"TCGroup Selected from line {p_start} to line {p_end} to {tc_name}.")  
    
    def save_description_part(self):
        with open(self.logic_file_path, 'r') as file:
            content = file.readlines()
        content = [line.strip() for line in content]
        for index, line in enumerate(content):
            if "Given logic" in line:
                des_start_line = index
            if "Test cases" in line:
                des_end_line = index
        des_section = content[des_start_line - 1:des_end_line] 
        # Add "//" to the beginning of each line
        des_section_with_comments = ["// " + line for line in des_section]
        self.TPDescription = des_section_with_comments
        
    def extract_keys_statements_from_TCGroup(self):
        for tc_name in self.TCGroup:
            tc_content = self.TCGroup[tc_name]['section']
            for line in range(len(tc_content)):
                if " : " in tc_content[line]: 
                    key_variable, key_value = tc_content[line].split(' : ')
                    variable = key_variable.strip() 
                    value = key_value.strip()
                    self.keys[variable] = value 
                    self.TCGroup[tc_name]['keys'] = self.keys
                elif "set" in tc_content[line]: 
                    if " to " in tc_content[line]:
                        statement_variable, st_value= tc_content[line].split(' to ')
                        variable_parts = statement_variable.split('set ')
                        st_variable = variable_parts[1].strip()
                    else:
                        statement_variable, statement_value = tc_content[line].split(' set ')
                        variable = statement_variable.strip()
                        value = statement_value.strip()
                    self.statements.setdefault(st_variable, {})['value'] = st_value
                    self.TCGroup[tc_name]['statements'] = self.statements
    
    #this function is used to map values and add elements to variables  according to parameters.txt               
    def map_keys_with_para(self)->None:
        for variable, value in self.keys.items(): 
            para_variable = self.parameter_map[variable]
            para_var_type = para_variable['Type']                
            para_var_data_type = para_variable['DataType']
            para_Resolution = para_variable['Resolution']
            self.keys[variable] = {}
            self.keys[variable]['Type'] = para_var_type
            self.keys[variable]['DataType'] = para_var_data_type
            self.keys[variable]['Resolution'] = para_Resolution
            self.keys[variable]['Value'] = value
            '''
            if para_var_data_type != 'enum':
                self.keys[variable]['Value'] = value
            else:
                value_int = int(value) 
                enum_range = list(para_variable['Range/Enums'])
                if value_int < len(enum_range):
                    self.keys[variable]['Value'] = enum_range[value_int]
                else:
                    self.keys[variable] = None        
            '''
    
    def add_operation_command_to_keys(self)->None:
        commands = self.load_commands(self.command_file_path)
        for variable in self.keys:
            var = self.keys[variable]
            value = self.keys[variable]['Value']
            if variable in commands and value in commands[variable]:
                var['Command'] = commands[variable][value]
            else:
                var['Command'] = "Command not founded.To be added"

                
                    

    
    def add_verify_command_to_statements(self):
        for state in self.statements:
            self.statements[state]['command'] = self.get_command_of_statements()
            
    def map_statements_CvtName(self):
        with open(self.csv_file_path, 'r',encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for state in self.statements: 
                for row in csv_reader:
                    if state == row[column_SysName]:
                        self.statements[state]['cv_name'] = row[column_CvtName]
        
    def get_command_of_statements(self)->list:
        cv_verify_command = []
        for state in self.statements:
            cv_name = self.statements[state]['cv_name']
            cv_value = self.statements[state]['value']
            delay_line = "DELAY 1000"
            cv_verify_command.append(delay_line)
            verify_line = "test if " + cv_name + " EQ " + cv_value  
            cv_verify_command.append(verify_line)
        return cv_verify_command
            
    def wr_TPDescription_to_tp_file(self):
        if os.path.exists(self.tp_file_name):
            os.remove(self.tp_file_name)        
        with open(self.tp_file_name, 'a') as tp:
            #write tp header
            tp.write("// This work contains valuable confidential and proprietary information of \n" 
                            "// Honeywell International Inc.  Disclosure, use or reproduction without the \n"
                            "// prior written authorization of Honeywell International Inc is prohibited. \n"
                            "// Copyright (c) 2023 Honeywell International Inc.  All rights reserved. \n\n\n")
            tp.write("//*********Test Name:       *********\n")
            tp.write("//*********Test Author:     ********* \n")
            tp.write("//*********Update Date:     ********* \n\n")
            #write tp description
            tp.write('\n'.join(self.TPDescription) + '\n')
                
    def wr_TCGroup_to_tp_file(self):
        for tc_name, tc_data  in self.TCGroup.items():
            with open(self.tp_file_name, 'a') as tp_file:
                tp_file.write(f"//Test Case Name: {tc_name}\n")
                tp_file.write(f"//========================Test Case Description===============================\n\n")                
                tp_file.write("//Test Case Section:\n")
                for line in tc_data['section']:
                    tp_file.write("//" + line)
                '''  
                tp_file.write("'Keys In Test Case:\n")
                for key, value in tc_data['keys'].items():
                    tp_file.write(f"'   {key}:\n")
                    for sub_key, sub_value in value.items():
                        tp_file.write(f"'     {sub_key}: {sub_value}\n")
                tp_file.write(f"'----------------------------------------------\n\n")
                        
                tp_file.write("'Statements in Test Case :\n")
                for state in tc_data['statements'].items():
                    tp_file.write(f"'   {state}: \n")
                '''
                tp_file.write(f"//========================End of Test Case Description===============================\n\n")  
            self.wr_command_to_tp_file()

    def wr_command_to_tp_file(self):
        with open(self.tp_file_name, 'a') as tpc_file:
            tpc_file.write(f"//***********************Excutable Commands of Test Case*******************************\n\n")                    
            tpc_file.write(f"//-------------------------------------\n")
            tpc_file.write(f"//Set up input : \n\n")
            for key, value in self.keys.items():
                if 'Command' in value:                        
                    tpc_file.write(value['Command'] + "\n")
            tpc_file.write(f"//-------------------------------------\n")
            tpc_file.write(f"//Verify output : \n\n")                         
            for state, value in self.statements.items():
                if 'command' in value:
                    for command in value['command']:
                        tpc_file.write(command + "\n")
            tpc_file.write(f"//************************End of Excutable Commands of Test Case**********************\n\n\n\n")
                
    def print_class_member_value(self):
        print('LogicFileProcessor-TCGroup:')
        print(json.dumps(self.TCGroup, indent=4))
        print('LogicFileProcessor-Keys:')
        print(json.dumps(self.keys, indent=4))
        print('LogicFileProcessor-Statements:')
        print(json.dumps(self.statements, indent=4))
        
    def process_file(self):
        self.build_parameter_map()
        self.buid_BIF_map()        
        self.select_lines_contains_useful_tc()
        self.save_TCGroup()        
        self.save_description_part()
        self.wr_TPDescription_to_tp_file()
        
        self.extract_keys_statements_from_TCGroup()
        self.map_keys_with_para()
        self.map_statements_CvtName()
        self.add_operation_command_to_keys()
        self.add_verify_command_to_statements()
        self.wr_TCGroup_to_tp_file()
        

# Example usage:
file_processor = LogicFileProcessor()
file_processor.process_file()
