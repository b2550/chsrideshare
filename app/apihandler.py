import json
import urllib

from app import app
from config import GOOGLE_API_KEY, DEBUG
from .models import User


def geocodeing_parser(user):
    dbuser = User.query.filter_by(email=user).first()
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
        app.logger.error('GOOGLE GEOCODING ERR: ' + jsonResponse['status'] + ": " + jsonResponse['error_message'])
        if DEBUG:
            app.logger.error(url)
            app.logger.error(jsonResponse)
        return {'latitude': None, 'longitude': None, 'address': None, 'error': jsonResponse['status']}
