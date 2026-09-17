from pathlib import Path

from setuptools import find_packages, setup


ROOT = Path(__file__).parent

requirements_path = ROOT / "requirements.txt"

if requirements_path.exists():
    requirements = [
        line.strip()
        for line in requirements_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
        and not line.startswith("#")
    ]
else:
    requirements = []


readme_path = ROOT / "README.md"

long_description = (
    readme_path.read_text(encoding="utf-8")
    if readme_path.exists()
    else ""
)


setup(
    name="neurocortex",
    version="0.1.0",
    description=(
        "NeuroCortex SRDF prototype framework "
        "for bounded runtime structural adaptation."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mohammed Al-Athwary",
    author_email="mohammedqaidalathwary@gmail.com",
    url="https://github.com/mohammedqaidamanlift-hub/-NEUROCORTEX",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    keywords=[
        "ai",
        "machine-learning",
        "srdf",
        "structural-adaptation",
        "runtime-adaptation",
    ],
    project_urls={
        "Documentation":
            "https://github.com/mohammedqaidamanlift-hub/-NEUROCORTEX/tree/main/docs",
        "Source":
            "https://github.com/mohammedqaidamanlift-hub/-NEUROCORTEX",
        "Tracker":
            "https://github.com/mohammedqaidamanlift-hub/-NEUROCORTEX/issues",
    },
)
