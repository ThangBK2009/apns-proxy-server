# -*- coding: utf-8 -*-
import logging
import traceback

from . import server
from . import validator
import settings


def init_log(level):
    logging.basicConfig(
        level=level,
        format='%(asctime)s %(levelname)s %(message)s')


def main():
    try:
        init_log(settings.LOG_LEVEL)
        validator.validate_settings(settings)
        server.start()
    except Exception, e:
        logging.error(e)
        logging.error(traceback.format_exc())


if __name__ == "__main__":
    main()
