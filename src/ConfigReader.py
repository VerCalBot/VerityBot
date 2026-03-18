import configparser
import Utils

config = configparser.ConfigParser()
config.read(f'{Utils.get_project_root()}/config.ini')
