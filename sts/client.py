# Copyright 2019, Cray Inc. All rights reserved.
""" Helper for getting a boto client for the request """
from flask import current_app as app, g
import boto3


def create_sts_client():
    """ Create a boto3 sts client from the app config """

    conf = app.config['CONFIG_OBJ'].update_rados_config()
    opts = {
        "verify": False,
        "endpoint_url": conf.get('int_endpoint_url'),
        "aws_access_key_id": conf.get("access_key"),
        "aws_secret_access_key": conf.get("secret_key"),
        "region_name": ""  # always empty string for rados
    }
    return boto3.client('sts', **opts)


def get_sts_client():
    """ Get the boto3 sts client from the app context, or create it if id DNE """

    if 'sts_client' not in g:
        app.logger.debug("Client not found, creating.")
        g.sts_client = create_sts_client()

    return g.sts_client
