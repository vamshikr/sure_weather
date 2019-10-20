import asyncio
import logging
import os
import sys

import uvloop
from aiohttp import web

from sure_weather.helper import google_maps
from sure_weather.weather import get_available_weather_services
from .routes import add_routes


def init_logger(logger_level):
    """
    Initialize the logger
    :param logger_level:
    :return:
    """
    logger_format = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    logging.basicConfig(format=logger_format,
                        level=logger_level,
                        datefmt='%d-%m-%Y:%H:%M:%S')


async def init_app() -> web.Application:
    """
    Initializes the application
    :return web.Application object
    """
    init_logger(os.environ.get('LOGGING_LEVEL', logging.INFO))

    # Using uvloop for better performance
    event_loop = uvloop.new_event_loop()
    asyncio.set_event_loop(event_loop)

    app = web.Application()

    # Get the available external weather services
    weather_services = get_available_weather_services()
    if not weather_services:
        logging.error("No weather services available")
        sys.exit(1)
    app['weather_services'] = weather_services

    # Checking if maps can be used for validation and zipcode lookup
    google_maps_key = os.environ.get('GOOGLE_MAPS_APIKEY', None)
    if google_maps_key:
        logging.error("Google Maps available")
        app['google_maps'] = google_maps.GoogleMaps(google_maps_key)
    else:
        logging.error("Google Maps NOT available")

    # Adding routes
    add_routes(app)
    return app
