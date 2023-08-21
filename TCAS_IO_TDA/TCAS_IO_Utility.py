class TCAS_IO_Utility:
    # def __init__(self):
    #     # Create an instance of LogicFileProcessor
    #     self.lp = LP()
        
    def get_command_of_select_transponder(self,variable, Value):
        select_transponder_command = []
        signal_name = 'XPDR1_276'
        if Value == 'Transponder #1':
            sig_value = 'NORMAL'
            comments = "//comments: Set {} {}".format(variable, Value)
            select_transponder_command.append(comments)
            command = "set {} {} \n".format(signal_name, sig_value)
            select_transponder_command.append(command)
        elif Value == 'Transponder #2': 
            sig_value = 'fw'
            comments = "//Set {} {}".format(variable, Value)
            select_transponder_command.append(comments)
            command = "set {} {} \n".format(signal_name, sig_value)
            select_transponder_command.append(command)
        return select_transponder_command
    
    def get_command_of_label(self,variable, Value, Signame):
        label_command = []
        signal_name = Signame
        if Value == 'INVALID':
            sig_value = 'fw'
            comments = "//Set {} {}".format(variable, Value)
            label_command.append(comments)
            command = "set {} {} \n".format(signal_name, sig_value)
            label_command.append(command)
        elif Value == 'VALID': 
            sig_value = 'NORMAL'
            comments = "//comments: Set {} {}".format(variable, Value)
            label_command.append(comments)
            command = "set {} {} \n".format(signal_name, sig_value)
            label_command.append(command)
        return label_command
    
    def get_command_of_unit_mode(self,variable, Value):
        select_transponder_command = []
        signal_name = 'T2016SNSLVL'
        if Value == 'Self-Test':
            sig_value = '1'
            comments = "//Set {} {}".format(variable, Value)
            select_transponder_command.append(comments)
            command = "set {} {} \n".format(signal_name, sig_value)
            select_transponder_command.append(command)
        elif Value == 'VALID': 
            sig_value = 'NORMAL'
            comments = "//Set {} {}".format(variable, Value)
            select_transponder_command.append(comments)
            command = "set {} {} \n".format(signal_name, sig_value)
            select_transponder_command.append(command)
        return select_transponder_command
    
    def get_command_of_unit_mode_SSM(self,variable, Value):
        select_transponder_command = [] 
        signal_name = 'T2016SNSLVL'
        if Value == 'TA':
            sig_value = '1'
            comments = "//Set {} {}".format(variable, Value)
            select_transponder_command.append(comments)
            command = "set {} {} \n".format(signal_name, sig_value)
            select_transponder_command.append(command)
        elif Value == 'TA/RA': 
            sig_value = '0'
            comments = "//Set {} {}".format(variable, Value)
            select_transponder_command.append(comments)
            command = "set {} {} \n".format(signal_name, sig_value)
            select_transponder_command.append(command)
        return select_transponder_command