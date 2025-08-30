# setup.py
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="neurocortex",
    version="0.1.0",
    description="Self-Evolving AI Framework with SRDF Architecture",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mohammed Al-Athwary",
    author_email="mohammedqaidalathwary@gmail.com",
    url="https://github.com/mohammedqaidamanlift-hub/NEUROCORTEX",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    keywords="ai machine-learning self-evolving autonomous",
    project_urls={
        "Documentation": "https://github.com/mohammedqaidamanlift-hub/NEUROCORTEX/docs",
        "Source": "https://github.com/mohammedqaidamanlift-hub/NEUROCORTEX",
        "Tracker": "https://github.com/mohammedqaidamanlift-hub/NEUROCORTEX/issues",
    },
)
