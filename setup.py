# coding: utf-8

"""


    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: beta

    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import setuptools
from setuptools import setup, find_packages

NAME = "kensu"

VERSION = "1.6.9.3"



# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

def get_extra_requires(path, add_all=True, add_all_but_test=True, add_no_extra_deps=True):
    import re
    from collections import defaultdict

    with open(path) as fp:
        extra_deps = defaultdict(set)
        for k in fp:
            if k.strip() and not k.startswith('#'):
                tags = set()
                if ':' in k:
                    k, v = k.split(':')
                    tags.update(vv.strip() for vv in v.split(','))
                tags.add(re.split('[<=>]', k)[0])
                for t in tags:
                    extra_deps[t].add(k)

        # add tag `all` at the end
        if add_all:
            extra_deps['all'] = set(vv for v in extra_deps.values() for vv in v)

        # add tag `all-but-test` at the end
        if add_all_but_test:
            extra_deps['all-but-test'] = set(vv for v in extra_deps.values() for vv in v if vv != "test")
        
        if add_no_extra_deps:
            extra_deps['no-extra-deps'] = set()
            

    print("Collected the following dependencies from " + path + ":")
    print(extra_deps)

    return extra_deps


def get_install_requires(path):
    with open(path) as fp:
        deps = []
        for l in fp:
            if l.strip() and not l.startswith('#'):
                deps.append(l)
        return deps

setup(
    name=NAME,
    version=VERSION,
    description="",
    author_email="",
    url="",
    keywords=["DODD", "Data Observability Driven Development", "Data Observability", "Analytics Observability"],
    packages=[
        package
        for package in setuptools.PEP420PackageFinder.find()
        if package.startswith("kensu")
    ],
    install_requires=get_install_requires('common-requirements.txt'),
    extras_require=get_extra_requires('extra.requirements'),
    platforms="Posix; MacOS X; Windows",
    include_package_data=True,
    long_description="""\
    DODD Python Agent: enable Data Observability Driven Development in your Python script\
    """
)
