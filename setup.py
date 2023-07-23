from setuptools import setup, find_packages

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
    name='neo4j_marshaller',
    version='0.0.1',
    url='https://github.com/arunsundaram50/neo4j-marshaller.git',
    author='Arun Sundaram',
    author_email='arun_co@yahoo.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='Simplified Neo4J Cypher Query execution',
    packages=find_packages(where="src"),  # Specifies the src directory
    package_dir={"": "src"},  # Specifies the package directory
    install_requires=requirements,
)
