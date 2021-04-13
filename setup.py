import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-fireplan",
    version="0.1.0",
    author="bouni",
    author_email="bouni@owee.de",
    description="python wrapper for fireplan API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bouni/python-fireplan",
    project_urls={
       "Bug Tracker": "https://github.com/bouni/python-fireplan/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "cerberus"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
