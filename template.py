from  pathlib import Path
import logging, os
logging.basicConfig(level=logging.INFO,format='[%(asctime)s]:%(message)s:')

project_name="network_security"
list_of_file=[
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    f"src/{project_name}/cloud/__init__.py",
    "params.yaml",
    "requirements.txt",
    "config.yaml",
    "Dockerfile",
    ".dockerignore",
    ".gitignore"
]
for filepath in list_of_file:
    filepath=Path(filepath)
    filedir,file_name=os.path.split(filepath)
    if filedir!="":
          os.makedirs(filedir,exist_ok=True)
          logging.info(f"Creating empty file {file_name}")
    if not os.path.exists(filepath) or (os.path.getsize(filepath))==0:
         with open(filepath,"w") as f:
              logging.info(f"Creating empty file {filepath}")
    else:
         logging.info(f"{file_name} already exists")