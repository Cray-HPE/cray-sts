# Copyright 2019, Cray Inc. All rights reserved.
""" These are the routes that are mapped to from connexion """
import uuid
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from flask import current_app as app

from sts import client as c


def put_token():
    """ PUT /token - Generate a new STS token and return in payload """
    # pylint: disable=broad-except, invalid-name
    try:
        client = c.get_sts_client()
    except Exception as e:
        app.logger.error(e)
        return "Error", 500

    conf = app.config['RADOS_CONFIG']

    response = client.assume_role(
        RoleArn=conf.get('arn'),
        RoleSessionName=str(uuid.uuid4()),  # Confirm with Craig that this wont cause issues
        DurationSeconds=3600  # Max expiration, 12 hours
    )
    if response.get('ResponseMetadata', {}).get('HTTPStatusCode', -1) != 200:
        app.logger.error(response.get('ResponseMetadata'))
        return 'Error', 500
    creds = response['Credentials']
    creds['EndpointURL'] = conf.get('ext_endpoint_url')
    return {"Credentials": creds}, 201


def get_healthz():
    """ Return health status """

    return {"Status": "ok"}, 200
