import visa

READ_TERMINATION  = '\r\n'
WRITE_TERMINATION = '\r\n'


class SourceMeterServer(object):

    def __init__(self,port):
        self.port = port
        self.isOpen = False
        self.open()

        self.alias_sense = {
            'VOLT':'VOLT', 'CURR':'CURR', 'RES':'RES',
            'volt':'VOLT', 'curr':'CURR', 'res':'RES',
            'V'   :'VOLT', 'C'   :'CURR', 'R'  :'RES',
            'v'   :'VOLT', 'c'   :'CURR', 'r'  :'RES',
            }

        self.alias_source = {
            'VOLT':'VOLT', 'CURR':'CURR',
            'volt':'VOLT', 'curr':'CURR',
            'V'   :'VOLT', 'C'   :'CURR',
            'v'   :'VOLT', 'c'   :'CURR',
            }
            



    ##########################################
    #  Opening and closing visa connections  #
    ##########################################
    def close(self):
        """Closes the connection to the COM port"""
        if self.isOpen:
            self._cxn.close()
            self.isOpen = False
        else:
            raise ValueError("Connection already closed")
    def open(self):
        if not(self.isOpen):
            self._rm  = visa.ResourceManager()
            self._cxn = self._rm.open_resource(
                "COM{n}".format(n=self.port),
                read_termination=READ_TERMINATION,
                write_termination=WRITE_TERMINATION,
                )
            self.isOpen = True # wheter or not the connection is open
        else:
            raise ValueError("Connection already open")
        



    ##########################
    #  LOW-LEVEL READ/WRITE  #
    ##########################
    def write(self,data):
        if self.isOpen:
            self._cxn.write(data)
        else:
            raise ValueError("Connection is closed")
    def write_raw(self,data):
        if self.isOpen:
            self._cxn.write_raw(data)
        else:
            raise ValueError("Connection is closed")
    def read(self):
        if self.isOpen:
            return self._cxn.read()
        else:
            raise ValueError("Connection is closed")




    ############################
    #  SYSTEM + MISC COMMANDS  #
    ############################
    def reset(self):
        """Resets the SourceMeter"""
        self.write("*RST")
    def remote_on(self):
        self.write(":SYST:RSEN ON")
    def remote_off(self):
        self.write(":SYST:RSEN OFF")




    #############################
    #  SOURCE (SOUR) FUNCTIONS  #
    #############################

    def source_mode(self,setto=None):
        if setto == None:
            self.write(":SOUR:FUNC:MODE?")
            return self.read()
        else:
            if setto in self.alias_source.keys():
                self.write(":SOUR:FUNC {setto}".format(setto=self.alias_source[setto]))
            else:
                raise ValueError("Invalid source mode")

    def source_voltage_range(self,setto=None):
        if setto == None:
            self.write(":SOUR:VOLT:RANG?")
            return float(self.read())
        else:
            self.write(":SOUR:VOLT:RANG {setto}".format(setto=setto))

    def source_current_range(self,setto=None):
        if setto == None:
            self.write(":SOUR:CURR:RANG?")
            return float(self.read())
        else:
            self.write(":SOUR:CURR:RANG {setto}".format(setto=setto))

    def source_voltage_level(self,setto=None):
        if setto == None:
            self.write(":SOUR:VOLT:LEV?")
            return float(self.read())
        else:
            self.write(":SOUR:VOLT:LEV {setto}".format(setto=setto))

    def source_current_level(self,setto=None):
        if setto == None:
            self.write(":SOUR:CURR:LEV?")
            return float(self.read())
        else:
            self.write(":SOUR:CURR:LEV {setto}".format(setto=setto))




    ###########################
    # OURPUT (OUTP) FUNCTIONS #
    ###########################
    def output_on(self):
        self.write(":OUTP ON")
    def output_off(self):
        self.write(":OUTP OFF")




    ##########################
    # SENSE (SENS) FUNCTIONS #
    ##########################

    def sense_off_all(self):
        self.write(":SENS:FUNC:OFF:ALL")
    def sense_on_all(self):
        self.write(":SENS:FUNC:ON:ALL")

    def sense_on(self,which):
        if not (which in self.alias_sense.keys()):
            raise ValueError("Invalid sense setting")
        self.write(":SENS:FUNC:ON '{which}'".format(which=self.alias_sense[which]))
    def sense_off(self,which):
        if not (which in self.alias_sense.keys()):
            raise ValueError("Invalid sense setting")
        self.write(":SENS:FUNC:OFF '{which}'".format(which=self.alias_sense[which]))

    def get_active_sense_functions(self):
        self.write(":SENS:FUNC:ON?")
        ans = self.read()
        if ans == '""': # no active functions
            return []
        active = []
        while ',' in ans:
            channel,_,ans = ans.partition(',')
            active.append(channel)
        active.append(ans)
        return active
    def get_inactive_sense_functions(self):
        self.write(":SENS:FUNC:OFF?")
        ans=self.read()
        if ans == '""': # no inactive functions
            return []
        inactive = []
        while ',' in ans:
            channel,_,ans = ans.partition(',')
            inactive.append(channel)
        inactive.append(ans)
        return inactive

    def sense_current_range(self,setto=None):
        if setto == None:
            self.write(":SENS:CURR:RANG?")
            return self.read()
        else:
            self.write(":SENS:CURR:RANG {setto}".format(setto=setto))
    def sense_current_prot(self,setto=None):
        if setto == None:
            self.write(":SENS:CURR:PROT?")
            return self.read()
        else:
            self.write(":SENS:CURR:PROT {setto}".format(setto=setto))
    def sense_voltage_range(self,setto=None):
        if setto == None:
            self.write(":SENS:VOLT:RANG?")
            return self.read()
        else:
            self.write(":SENS:VOLT:RANG {setto}".format(setto=setto))
    def sense_voltage_prot(self,setto=None):
        if setto == None:
            self.write(":SENS:VOLT:PROT?")
            return self.read()
        else:
            self.write(":SENS:VOLT:PROT {setto}".format(setto=setto))

















if __name__ == '__main__':
    s = SourceMeterServer(4)
    v='VOLT'
    c='CURR'
    r='RES'

