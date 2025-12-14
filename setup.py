from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    this will return list of requirements
    """
    req_list:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            # read lines from file 
            lines=file.readlines()
            for line in lines:
                req=line.strip()
                # ignore empty lines and -e.
                if req and req!='-e .':
                    req_list.append(req)
                
    except FileNotFoundError:
        print("File : requirements.txt not found")

    return req_list

setup(
    name="networksecurity",
    version="0.0.1",
    author="Neeraj",
    author_email="bneeraj2006@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
