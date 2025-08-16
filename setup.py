from setuptools import find_packages,setup
from typing import List


def get_requirements()->List[str]:
    """
    This function will return list of requirements
    
    """
    requirement_list:List[str]=[]
    try:
        with (open('requirements.txt','r')) as file:
            lines=file.readlines()
            for line in lines:
                requirements=line.strip()
                ## ignore empty lines and -e .
                if requirements and requirements!='-e .':
                    requirement_list.append(requirements)
    except FileNotFoundError as e:
        raise e
    
    return requirement_list
setup(
    name="Network",version="0.0.1",
    author="Alok",author_email="waynerooney0089@gmail.com",
    packages=find_packages(),
    requires=get_requirements()
)