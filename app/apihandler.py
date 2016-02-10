import json
import urllib
from pprint import pprint

from config import GOOGLE_API_KEY, DEBUG
from .models import User


def geocodeing_parser(user):
    dbuser = User.query.filter_by(email=user).first()
    address = dbuser.address.replace(' ', '+')

    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + address + '&key=' + GOOGLE_API_KEY

    googleResponse = urllib.urlopen(url)
    jsonResponse = json.load(googleResponse)

    if jsonResponse['status'] == 'OK':
        if DEBUG:
            print('GOOGLE GEOCODING REQUEST: ' + jsonResponse['status'])
            print(url)
            pprint(jsonResponse)
        latitude = jsonResponse['results'][0]['geometry']['location']['lat']
        longitude = jsonResponse['results'][0]['geometry']['location']['lng']
        address = jsonResponse['results'][0]['formatted_address']
        return {'latitude': latitude, 'longitude': longitude, 'address': address, 'error': None}
    else:
        if DEBUG:
            print('GOOGLE GEOCODING ERR: ' + jsonResponse['status'] + ": " + jsonResponse['error_message'])
            print(url)
            pprint(jsonResponse)
        return {'latitude': None, 'longitude': None, 'address': None, 'error': jsonResponse['status']}
