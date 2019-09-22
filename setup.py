from setuptools import setup

__name__: "Sprite Utility"
__author__: "Khang VU"
__copyright__: "Copyright (C) 2019, Intek Institute"
__credits__: "Khang VU"
__email__: "khang.vu@alumni.intek.edu.vn"
__license__: "MIT"
__maintainer__: "Khang VU"
__version__: "1.0.0"
__name__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="An internal project for Intek Institute",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khagkhangg/sprite_sheet_solution",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
