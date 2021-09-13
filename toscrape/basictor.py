import time, logging
from stem import Signal
from stem.control import Controller
from stem.util.log import get_logger as get_stem_logger
class BasicTor:    
    def __init__(self, port=9051, pwd='jelszo', log_level_string = 'DEBUG'):
        self.port = port    # control port, usually for 9050
        self.pwd = pwd
        # https://stackoverflow.com/questions/18786912/get-output-from-the-logging-module-in-ipython-notebook
        self.logger = logging.getLogger()
        # https://stackoverflow.com/questions/35679012/how-to-convert-python-logging-level-name-to-integer-code
        self.logger.setLevel(getattr(logging, log_level_string))
        self.logger.info("Tor settings initialized")        
        
    def new_tor_identity(self):     
        # https://stackoverflow.com/questions/43942689/error-while-receiving-a-control-message-socketclosed-empty-socket-content-i
        stem_logger = get_stem_logger()
        stem_logger.propagate = False
        
        # https://dokumen.pub/mastering-python-for-networking-and-security-leverage-the-scripts-and-libraries-of-python-version-37-and-beyond-to-overcome-networking-and-security-issues-1839216212-9781839216213.html
        with Controller.from_port(port=self.port) as controller:
            controller.authenticate(password=self.pwd)
            controller.signal(Signal.NEWNYM)
            if controller.is_newnym_available() == False: 
                self.logger.info("Waiting time for Tor to change IP: " 
                    + str(controller.get_newnym_wait()) 
                    + " seconds"
                ) 
                time.sleep(controller.get_newnym_wait()) 
            controller.close()
       
    def __del__(self):
        self.logger.info('BasicTor deleted')   
        

