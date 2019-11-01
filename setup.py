#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="rcli",
    author="Bruno Gregório",
    author_email="bruno.gregorio.silva@outlook.com",
    version="0.2.0b1",
    description="A small lib to make good command line interfaces effortlessly.",
    project_urls={"Source": "https://github.com/reclusivebox/rcli", "Web Page": "https://reclusivebox.github.io/rcli/"},
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Interpreters"
    ],
    python_requires=">=3.6"
)
