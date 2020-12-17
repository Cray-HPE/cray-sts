# Copyright 2019, Cray Inc. All rights reserved.
""" This module holds the configs for each env and has some helper to get it for use """
# pylint: disable=invalid-name

# NOTE (rbezdicek): This isn't really that great, but it shows how we can refresh
# from disk and have different configs for dev purposes. Probably could use some
# more work.

import os

from sts.util import get_yaml_file


class Config():
    """
    STS Config. The following env vars can be used:

    STS_CREDS_PATH - path to directory with AWS creds
        Required files in directory: access_key, secret_key
    STS_RADOS_CONFIG_PATH - path to valid yaml file with rados configuration settings
        Require values in file: arn, ext_endpoint_url, int_endpoint_url
    STS_RUNTIME - whether running locally or in a container, defaults to local
        Valid values: container, local
    STS_ENV - The environment to use while sourcing config files.
        Valid values: production, development
    """
    LOG_LEVEL = "debug"
    DEFAULT_RADOS_ACCESS_KEY_FILE = "/conf/creds/access_key"
    DEFAULT_RADOS_SECRET_KEY_FILE = "/conf/creds/secret_key"
    DEFAULT_RADOS_CONFIG_FILE = "/conf/rados_conf"

    def __init__(self):
        self.RADOS_CONFIG = {}
        # Run in init to ensure files exist during bring up
        self.update_rados_config()

    def update_rados_config(self):
        """ Gathers the S3 config params, we try to grab from a file
        so rolling the credentials in k8s wont require a restart """
        o = {}

        access_key = get_yaml_file(os.environ.get('STS_CREDS_PATH', self.DEFAULT_RADOS_ACCESS_KEY_FILE))
        secret_key = get_yaml_file(os.environ.get('STS_CREDS_PATH', self.DEFAULT_RADOS_SECRET_KEY_FILE))
        rados_config = get_yaml_file(os.environ.get('STS_RADOS_CONFIG_PATH', self.DEFAULT_RADOS_CONFIG_FILE))

        o.update({'access_key': access_key})
        o.update({'secret_key': secret_key})
        o.update(rados_config)
        self.RADOS_CONFIG = o

        return self.RADOS_CONFIG


class LocalConfig(Config):
    """ Local Config defaults """
    DEFAULT_RADOS_ACCESS_KEY_FILE = os.path.join(os.getcwd(), "conf/creds/access_key")
    DEFAULT_RADOS_SECRET_KEY_FILE = os.path.join(os.getcwd(), "conf/creds/secret_key")
    DEFAULT_RADOS_CONFIG_FILE = os.path.join(os.getcwd(), "conf/rados_conf")
    OPENAPI_FILE = "../api/openapi.yaml"


class ContainerConfig(Config):
    """ Container Config defaults """
    DEFAULT_RADOS_CREDS_FILE = "/conf/creds"
    DEFAULT_RADOS_CONFIG_FILE = "/conf/rados_conf"
    OPENAPI_FILE = "/api/openapi.yaml"


class LocalDevelopmentConfig(LocalConfig):
    """ Local dev config """
    ENV = "development"
    DEBUG = True
    DEVELOPMENT = True


class ContainerDevelopmentConfig(ContainerConfig):
    """ Container dev config """
    ENV = "development"
    DEBUG = True
    DEVELOPMENT = True


class ProductionConfig(ContainerConfig):
    """ Production Config """
    ENV = "production"
    DEBUG = False
    DEVELOPMENT = False
    LOG_LEVEL = "info"


_CONFIGS = {
    "local": {
        "development": LocalDevelopmentConfig,
    },
    "container": {
        "development": ContainerDevelopmentConfig,
        "production": ProductionConfig
    }

}

_CONFIG = None


def get_config():
    """ Get the proper config based on local env """

    if _CONFIG is not None:
        return _CONFIG

    rt = os.environ.get('STS_RUNTIME', "local")
    env = os.environ.get('STS_ENV', 'development')

    if rt.lower() in ['container', 'docker']:
        rt = 'container'
    elif rt.lower() in ['local']:
        rt = 'local'

    if rt not in _CONFIGS:
        raise Exception("Runtime not found: {}".format(env))

    # Purposely ignore checking rt here so keyerror propegates up if DNE
    rt_configs = _CONFIGS[rt]

    if env.lower() in ['production', 'prod']:
        env = 'production'
    elif env.lower() in ['dev', 'development']:
        env = 'development'

    if env not in rt_configs:
        raise Exception("Environment not found: {}".format(env))

    return rt_configs[env]()
