import configparser
import Utils

config = configparser.ConfigParser()
config.read(Utils.get_project_root() / "config.ini")
