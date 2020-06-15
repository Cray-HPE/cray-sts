from setuptools import setup, find_packages


with open('LICENSE') as license_file:
    LICENSE = license_file.read()

with open('requirements.txt') as reqs_file:
    REQUIRMENTS = reqs_file.read()

with open('.version') as vers_file:
    VERSION = vers_file.read()

setup(
    name='sts',
    author="Cray Inc.",
    author_email="rbezdicek@cray.com",
    url="http://cray.com",
    description="Generates short term ceph s3 credentials",
    long_description="Generates short term ceph s3 credentials",
    version=VERSION,
    package_data={'': ['../api/openapi.yaml']},
    packages=find_packages(),
    license=LICENSE,
    include_package_data=True,
    install_requires=REQUIRMENTS
)