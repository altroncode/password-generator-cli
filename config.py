import configparser
import os
import pathlib


config = configparser.ConfigParser()
config_path = pathlib.Path(os.curdir) / 'config.ini'
config.read(config_path)
