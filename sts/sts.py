#  Copyright 2019, Cray Inc. All rights reserved.
""" Main entrypoint """
# pylint: disable=invalid-name

import logging

import connexion

from sts import config


def create_app():
    """ Create the connexion app """
    app = connexion.FlaskApp(__name__, port=9090)

    found_config = config.get_config()
    log_level = found_config.LOG_LEVEL.upper()
    logging.basicConfig(level=log_level)
    app.app.logger.setLevel(log_level)
    app.app.config.from_object(found_config)
    app.app.config['CONFIG_OBJ'] = found_config
    app.add_api(app.app.config['OPENAPI_FILE'], arguments={'title': 'STS Generator'})

    return app


conn_app = create_app()


if __name__ == '__main__':
    conn_app.run()
