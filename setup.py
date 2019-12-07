#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="reclusivecli",
    author="Bruno Gregório",
    author_email="reclusivebox@outlook.com",
    version="0.4.0a1",
    description="A small lib to make good command line interfaces effortlessly.",
    project_urls={"Source": "https://github.com/reclusivebox/reclusivecli", "Web Page": "https://reclusivebox.github.io/reclusivecli/"},
    packages=setuptools.find_packages(),
    py_modules=["rcllib", "rclerrors"],
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
