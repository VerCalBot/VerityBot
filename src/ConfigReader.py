import configparser
from Utils import get_project_root

config = configparser.ConfigParser()
config.read(f"{get_project_root()}/config.ini")
