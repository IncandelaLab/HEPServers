import serial

DEBUG = False

def partition_any(string,seps):
    """partitions string at first instance of any element of seps"""
    least_index = [len(string),-1]
    for i,sep in enumerate(seps):
        if sep in string:
            index = string.index(sep)
            if index < least_index[0]:
                least_index = [index,i]
    if least_index[1] == -1:
        return string,'',''
    return string.partition(seps[least_index[1]])

class serialServer(object):

    def __init__(
        self,
        port,
        baudrate,
        timeout=0,
        write_termination='\r\n',
        read_termination='\r\n',
        mclsep=None,
        ):

        self._port     = port
        self._baudrate = baudrate
        self._timeout  = timeout
        self._write_termination = write_termination
        self._read_termination  = read_termination
        self._mclsep = mclsep

        self._seps = [self._read_termination]
        if self._mclsep:self._seps.append(self._mclsep)

        self.lines_read = []

        self._mode = 'closed'
        self.open()

    def enforce_mode(mode):
        if not (type(mode) in [str,list]):
            raise ValueError
        def wrapper(function):
            def wrapped_function(self,*args,**kwargs):
                if type(mode) is str:
                    valid_mode = self._mode == mode
                elif type(mode) is list:
                    valid_mode = self._mode in mode
                else:
                    valid_mode = False
                if valid_mode:
                    if DEBUG:
                        print("mode {} req {} calling function {} with args {} kwargs {}".format(
                            self._mode,
                            mode,
                            function.__name__,
                            args,
                            kwargs,
                            ))
                    ret = function(self,*args,**kwargs)
                    return ret
                else:
                    print("mode is {}, needed {} for function {} with args {} kwargs {}".format(
                        self._mode,
                        mode,
                        function.__name__,
                        args,
                        kwargs,
                        ))
            return wrapped_function
        return wrapper

    @enforce_mode('closed')
    def open(self):
        self._ser = serial.Serial(self._port,self._baudrate,timeout=self._timeout)
        self._mode = 'open'

    @enforce_mode('open')
    def close(self):
        self._ser.close()
        self._mode = 'closed'

    @enforce_mode('open')
    def _write_line(self,line):
        write_bytes = (line + self._write_termination).encode('utf-8')
        self._ser.write(write_bytes)

    @enforce_mode('open')
    def _read_line(self):
        read_bytes = self._ser.readline().decode('utf-8')
        return read_bytes

    @enforce_mode('open')
    def _read_lines(self):
        read_lines_bytes = self._ser.readlines()
        return [_.decode('utf-8') for _ in read_lines_bytes]

    @enforce_mode('open')
    def read_lines(self):
        avail = self._read_lines()
        if len(avail) == 0:
            return False

        for line in avail:
            while len(line)>0:
                bef,_,line = partition_any(line,self._seps)
                self.lines_read.append(bef)

        return True


# Test base server on basic Keithly 2410 commands
if __name__ == '__main__':
    import time
    s = serialServer('COM6',9600,mclsep=';')
    s._write_line("*RST")
    s._write_line(":SOUR:FUNC?")
    s._write_line(":SOUR:FUNC?")
    s._write_line(":SOUR:FUNC?")
    s._write_line("*IDN?")
    s._write_line("*IDN?")
    s._write_line("*IDN?")
    s._write_line("*IDN?")
    s.read_lines()
    print(s.lines_read)
    time.sleep(1)
    s.read_lines()
    print(s.lines_read)

    s.close()
