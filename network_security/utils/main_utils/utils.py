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
# def write_yaml_file(file_path:str,content:object, replace:bool=False)->None:
#     try:
#         if replace:
#                 if os.path.exists(file_path):
#                     os.remove(file_path)
#                 os.makedirs(file_path)
#         os.makedirs(file_path,exist_ok=True)
#         with open(file_path,"w") as file:
#              yaml.dump(content,file)
#     except Exception as e:
#         raise NetworkSecurityException(e,sys)
    

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        # Get the directory path from the file path
        dir_path = os.path.dirname(file_path)
        
        # Create the directory if it doesn't exist
        # os.makedirs(dir_path, exist_ok=True)
        
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        
        # Write the file
        with open(file_path, "w") as file:
            yaml.dump(content, file)
            
    except Exception as e:
        raise NetworkSecurityException(e, sys)