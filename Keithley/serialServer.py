import serial

class serialServer(object):

    def __init__(
        self,
        port,
        baudrate,
        timeout=0,
        write_termination='\r',
        read_termination='\r',
        mclsep=None,
        ):
        
        self._port     = port
        self._baudrate = baudrate
        self._timeout  = timeout
        self._write_termination = write_termination
        self._read_termination  = read_termination
        self._mclsep = mclsep

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
                    function(self,*args,**kwargs)
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
        self._ser = serial.Serial(port,baudrate,timeout=timeout)
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

            if self._mclsep: # non-empty string; not None
                while self._mclsep in line:
                    bef,_,line = line.partition(self._mclsep)
                    self.lines_read.append(bef)
            
            if self._read_termination: # non-empty string; not None
                if line.endswith(self._read_termination):
                    line,_,_ = line.rpartition(self._read_termination)

            self.lines_read.append(line)

        return True