from setuptools import setup,find_packages
from typing import List 

def get_requirements(path:str) -> List[str]:
    with open(path) as file_obj:
        file_data = file_obj.readlines()
        requirements = [file_datas.replace("\n","") for file_datas in file_data if file_datas.strip() != "-e ."]
        return requirements

setup(
    name="MCP_AGENT",
    author="Rajkumar",
    author_email="tech84602@gmail.com",
    version="1.0.0",
    packages=find_packages(),
    install_requires = get_requirements(path="requirements.txt")
)


# if __name__ == "__main__":
#     print(get_requirements("requirements.txt"))