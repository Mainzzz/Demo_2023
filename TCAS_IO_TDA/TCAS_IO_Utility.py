import LogicFileProcessor as LP

class TCAS_IO_Utility:
    def __init__(self):
        # Create an instance of LogicFileProcessor
        self.lp = LP()
        
    def get_command_of_select_transponder(self, variable):
        select_transponder_command = []
        if variable in self.lp.keys:
            var = self.lp.keys[variable] 
            signal_name = 'XPDR1_276'
            if var['Value'] == 'Transponder #1':
                sig_value = 'NORMAL'
                comments = "//comments: Set {} {}".format(variable, var['Value'])
                select_transponder_command.append(comments)
                command = "set {} {} \n".format(signal_name, sig_value)
                select_transponder_command.append(command)
            elif var['Value'] == 'Transponder #2': 
                sig_value = 'fw'
                comments = "//Set {} {}".format(variable, var['Value'])
                select_transponder_command.append(comments)
                command = "set {} {} \n".format(signal_name, sig_value)
                select_transponder_command.append(command)
        return select_transponder_command
    
    def get_command_of_label(self,variable):
        label_command = []
        if variable in self.keys:
            var = self.keys[variable]
            signal_name = self.bif_map[variable]['signal']
            if var['Value'] == 'INVALID':
                sig_value = 'fw'
                comments = "//Set {} {}".format(variable, var['Value'])
                label_command.append(comments)
                command = "set {} {} \n".format(signal_name, sig_value)
                label_command.append(command)
            elif var['Value'] == 'VALID': 
                sig_value = 'NORMAL'
                comments = "//comments: Set {} {}".format(var, var['Value'])
                label_command.append(comments)
                command = "set {} {} \n".format(signal_name, sig_value)
                label_command.append(command)
        return label_command
    
    def get_command_of_unit_mode(self, variable):
        select_transponder_command = []
        if variable in self.lp.keys:
            var = self.lp.keys[variable] 
            signal_name = 'T2016SNSLVL'
            if var['Value'] == 'Self-Test':
                sig_value = '1'
                comments = "//Set {} {}".format(variable, var['Value'])
                select_transponder_command.append(comments)
                command = "set {} {} \n".format(signal_name, sig_value)
                select_transponder_command.append(command)
            elif var['Value'] == 'VALID': 
                sig_value = 'NORMAL'
                comments = "//Set {} {}".format(var, var['Value'])
                select_transponder_command.append(comments)
                command = "set {} {} \n".format(signal_name, sig_value)
                select_transponder_command.append(command)
        return select_transponder_command
    
    def get_command_of_unit_mode_SSM(self, variable):
        select_transponder_command = []
        if variable in self.lp.keys:
            var = self.lp.keys[variable] 
            signal_name = 'T2016SNSLVL'
            if var['Value'] == 'TA':
                sig_value = '1'
                comments = "//Set {} {}".format(variable, var['Value'])
                select_transponder_command.append(comments)
                command = "set {} {} \n".format(signal_name, sig_value)
                select_transponder_command.append(command)
            elif var['Value'] == 'TA/RA': 
                sig_value = 'NORMAL'
                comments = "//Set {} {}".format(var, var['Value'])
                select_transponder_command.append(comments)
                command = "set {} {} \n".format(signal_name, sig_value)
                select_transponder_command.append(command)
        return select_transponder_command