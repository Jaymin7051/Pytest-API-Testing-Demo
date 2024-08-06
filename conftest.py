"""
The file contains setups for test folder
"""
import logging
import pytest
import sys
import os
from datetime import datetime


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """
    Configure logging to capture pytest terminal output.
    """
    log_dir = 'logs'
    dt_string = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    log_file = open(os.path.join(log_dir, 'pytest_output_'+dt_string+'.log'), 'w')

    class TeeStream:
        def __init__(self, *streams):
            self.streams = streams

        def write(self, data):
            for stream in self.streams:
                stream.write(data)
                stream.flush()

        def flush(self):
            for stream in self.streams:
                if not stream.closed:
                    stream.flush()

        def isatty(self):
            return all(stream.isatty() for stream in self.streams if hasattr(stream, 'isatty'))

    # Redirect stdout and stderr to both console and log file

    sys.stdout = TeeStream(sys.stdout, log_file)
    sys.stderr = TeeStream(sys.stderr, log_file)

    # Configure root logger to log to a file and console

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:  # Check if handlers are already added to avoid duplicates

        # Console Handler

        console_handler = logging.StreamHandler(sys.stdout)

        # Add Handlers
        logger.addHandler(console_handler)

    # Log the configuration

    logger.debug('Logging is configured.')

    # Store the log file handle for closure

    config._log_file = log_file


@pytest.hookimpl(trylast=True)
def pytest_unconfigure(config):
    """
    Close log file handle after pytest finishes.
    """
    log_file = getattr(config, '_log_file', None)
    if log_file:
        log_file.close()

