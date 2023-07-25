import LogicFileProcessor as LP

class TCAS_IO_Utility:
    def __init__(self):
        # Create an instance of LogicFileProcessor
        self.lp = LP()
        
    def get_command_of_select_transponder(self, variable):
        select_transponder_command = []
        if variable in self.lp.keys:
            var = self.lp.keys[variable] 
            if var['Value'] == 'INVALID':
                sig_value = 'fw'
                comments = "//Set {} {}".format(variable, var['Value'])
                select_transponder_command.append(comments)
                command = "set {} {} \n".format(variable, sig_value)
                select_transponder_command.append(command)
            elif var['Value'] == 'VALID': 
                sig_value = 'NORMAL'
                comments = "//Set {} {}".format(var, var['Value'])
                select_transponder_command.append(comments)
                command = "set {} {} \n".format(variable, sig_value)
                select_transponder_command.append(command)
        return select_transponder_command
    
    def get_command_of_set_unit_mode(self, variable):
        select_transponder_command = []
        if variable in self.lp.keys:
            var = self.lp.keys[variable] 
            if var['Value'] == 'INVALID':
                sig_value = 'fw'
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