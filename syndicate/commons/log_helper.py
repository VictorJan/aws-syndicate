"""
    Copyright 2018 EPAM Systems, Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import logging
import getpass
import os
from logging import DEBUG, Formatter, INFO, getLogger

SDCT_HOME_ENV_NAME = 'SDCT_HOME'
LOG_FOLDER_NAME = 'logs'
LOG_FILE_NAME = 'syndicate.log'
LOG_NAME = 'syndicate'
LOG_LEVEL = DEBUG if os.environ.get('SDCT_DEBUG', False) else INFO
USER_NAME = getpass.getuser()
LOG_FORMAT_FOR_FILE = ('%(asctime)s [%(levelname)s] USER:{} %(filename)s:'
                       '%(lineno)d:%(funcName)s LOG: %(message)s'
                       .format(USER_NAME))

def get_project_log_file_path() -> str:
    """Returns the path to the file where logs will be saved.
    :rtype: str
    :returns: a path to the main log file
    """
    sdct_home = os.getenv(SDCT_HOME_ENV_NAME)
    if not sdct_home:
        logs_path = os.getcwd()
    else:
        logs_path = os.path.join(sdct_home, LOG_FOLDER_NAME)
    os.makedirs(logs_path, exist_ok=True)

    log_file_path = os.path.join(logs_path, LOG_FILE_NAME)
    return log_file_path


log_file_path = get_project_log_file_path()

# formatter
formatter = Formatter(LOG_FORMAT_FOR_FILE)
# file output
file_handler = logging.FileHandler(filename=log_file_path)
file_handler.setFormatter(formatter)
# console output
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

user_logger = getLogger(f'user-{LOG_NAME}')
user_logger.addHandler(console_handler)
user_logger.addHandler(file_handler)

syndicate_logger = getLogger(LOG_NAME)
syndicate_logger.addHandler(file_handler)

if LOG_LEVEL == DEBUG:
    syndicate_logger.addHandler(console_handler)

logging.captureWarnings(True)


def get_logger(log_name, level=LOG_LEVEL):
    """
    :param level:   CRITICAL = 50
                    ERROR = 40
                    WARNING = 30
                    INFO = 20
                    DEBUG = 10
                    NOTSET = 0
    :type log_name: str
    :type level: int
    """
    module_logger = syndicate_logger.getChild(log_name)
    if level:
        module_logger.setLevel(level)
    return module_logger


def get_user_logger(level=LOG_LEVEL):
    """
    :param level:   CRITICAL = 50
                    ERROR = 40
                    WARNING = 30
                    INFO = 20
                    DEBUG = 10
                    NOTSET = 0
    :type log_name: str
    :type level: int
    """
    module_logger = user_logger.getChild('child')
    if level:
        module_logger.setLevel(level)
    return module_logger
