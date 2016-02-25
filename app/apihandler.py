import json
import urllib

from app import app
from .models import Users


def geocodeing_parser(user):
    GOOGLE_API_KEY = app.config.get('GOOGLE_API_KEY')
    DEBUG = app.config.get('DEBUG')

    dbuser = Users.query.filter_by(email=user).first()
    address = dbuser.address.replace(' ', '+')

    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=' + GOOGLE_API_KEY

    googleResponse = urllib.urlopen(url)
    jsonResponse = json.load(googleResponse)

    if jsonResponse['status'] == 'OK':
        app.logger.info('GOOGLE GEOCODING REQUEST: ' + jsonResponse['status'])
        if DEBUG:
            app.logger.debug(url)
            app.logger.debug(jsonResponse)
        latitude = jsonResponse['results'][0]['geometry']['location']['lat']
        longitude = jsonResponse['results'][0]['geometry']['location']['lng']
        address = jsonResponse['results'][0]['formatted_address']
        return {'latitude': latitude, 'longitude': longitude, 'address': address, 'error': None}
    else:
        app.logger.error(url)
        app.logger.error(jsonResponse)
        return {'latitude': None, 'longitude': None, 'address': None, 'error': jsonResponse['status']}
