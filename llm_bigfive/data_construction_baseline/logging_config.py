# logging_config.py
import sys
import logging
from datetime import datetime

def setup_logging(mode='training'):
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Generate a timestamped log file name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"logs/{mode}_{timestamp}.log"
    
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S',
        level=logging.INFO,
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
    )
    
    # Redirect stdout and stderr to the logger
    redirect_output_to_logger()

def redirect_output_to_logger():
    class LoggerWriter:
        def __init__(self, logger, level):
            self.logger = logger
            self.level = level
            self.linebuf = ''
        
        def write(self, message):
            if message.rstrip() != "":
                self.logger.log(self.level, message.rstrip())
        
        def flush(self):
            pass
    
    logger = logging.getLogger()
    sys.stdout = LoggerWriter(logger, logging.INFO)
    sys.stderr = LoggerWriter(logger, logging.ERROR)
