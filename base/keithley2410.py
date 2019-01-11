from serialServer import serialServer

class keithley2410Server(serialServer):

    def __init__(self,port):
        super(keithley2410Server,self).__init__(
            port,
            9600,
            mclsep=';',
            )

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

        self.alias_bool = {
            True:'ON', False:'OFF',
            1   :'ON', 0    :'OFF',
            'on':'ON', 'off':'OFF',
            'ON':'ON', 'OFF':'OFF',
            }



    # system commands

    @serialServer.enforce_mode('open')
    def reset(self):
        """Resets the device"""
        self._write_line("*RST")

    @serialServer.enforce_mode('open')
    def remote(self,setto=None):
        if setto is None:
            self._write_line(":SYST:RSEN?")
        else:
            self._write_line(":SYST:RSEN {}".format(self.alias_bool[setto]))



    # output commands

    @serialServer.enforce_mode('open')
    def output(self,setto=None):
        if setto is None:
            self._write_line(":OUTP?")
        else:
            self._write_line(":OUTP {}".format(self.alias_bool[setto]))



    # source commands

    @serialServer.enforce_mode('open')
    def source_mode(self,setto=None):
        if setto is None:
            self._write_line(":SOUR:FUNC:MODE?")
        else:
            self._write_line(":SOUR:FUNC:MODE {}".format(self.alias_source[setto]))

    @serialServer.enforce_mode('open')
    def source_voltage_range(self,setto=None):
        if setto is None:
            self._write_line(":SOUR:VOLT:RANG?")
        else:
            self._write_line(":SOUR:VOLT:RANG {}".format(setto))

    @serialServer.enforce_mode('open')
    def source_current_range(self,setto=None):
        if setto is None:
            self._write_line(":SOUR:CURR:RANG?")
        else:
            self._write_line(":SOUR:CURR:RANG {}".format(setto))

    @serialServer.enforce_mode('open')
    def source_voltage_level(self,setto=None):
        if setto is None:
            self._write_line(":SOUR:VOLT:LEV?")
        else:
            self._write_line(":SOUR:VOLT:LEV {}".format(setto))

    @serialServer.enforce_mode('open')
    def source_current_level(self,setto=None):
        if setto is None:
            self._write_line(":SOUR:CURR:LEV?")
        else:
            self._write_line(":SOUR:CURR:LEV {}".format(setto))



    # sense functions

    @serialServer.enforce_mode('open')
    def sense_all(self,setto):
        self._write_line(":SENS:FUNC:{}:ALL".format(self.alias_bool[setto]))

    @serialServer.enforce_mode('open')
    def sense(self,which,setto):
        self._write_line(":SENS:FUNC:{} '{}'".format(
            self.alias_bool[setto],
            self.alias_sense[which],
            ))

    @serialServer.enforce_mode('open')
    def get_sense_functions(self,which='ON'):
        self._write_line(":SENS:FUNC:{}?".format(self.alias_bool[which]))

    @serialServer.enforce_mode('open')
    def sense_current_range(self,setto):
        if setto is None:
            self._write_line(":SENS:CURR:RANG?")
        else:
            self._write_line(":SENS:CURR:RANG {}".format(setto))

    @serialServer.enforce_mode('open')
    def sense_current_prot(self,setto):
        if setto is None:
            self._write_line(":SENS:CURR:PROT?")
        else:
            self._write_line(":SENS:CURR:PROT {}".format(setto))

    @serialServer.enforce_mode('open')
    def sense_voltage_range(self,setto):
        if setto is None:
            self._write_line(":SENS:VOLT:RANG?")
        else:
            self._write_line(":SENS:VOLT:RANG {}".format(setto))

    @serialServer.enforce_mode('open')
    def sense_voltage_prot(self,setto):
        if setto is None:
            self._write_line(":SENS:VOLT:PROT?")
        else:
            self._write_line(":SENS:VOLT:PROT {}".format(setto))



if __name__ == '__main__':
    import time
    s = keithley2410Server('COM6')
    s.reset()

    s.source_mode()
    s.source_voltage_range()
    s.source_current_range()
    s.source_voltage_level()
    s.source_current_level()
    s.get_sense_functions('ON')
    s.get_sense_functions('OFF')
    s.sense_all('off')
    s.get_sense_functions('ON')
    s.get_sense_functions('OFF')

    s.read_lines()
    print(s.lines_read)
    time.sleep(1)
    s.read_lines()
    print(s.lines_read)
    s.close()
