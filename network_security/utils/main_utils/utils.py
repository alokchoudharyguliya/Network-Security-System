import yaml, numpy as np, os, sys, pickle
# import dill

from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
                return yaml.safe_load(yaml_file)
    except Exception as e:
         raise NetworkSecurityException(e,sys) from e