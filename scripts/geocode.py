#!/usr/bin/python

import geocode
import os.path as op
import sys
from optparse import OptionParser

def geocode(location):
    '''
    Get the coordinates for a particular location string.

    @param location: A location name, i.e "Vienna, Austria"
    @return: A (longitude, latitude) pair
    '''


def main():
    usage = """
    python geocode.py location
    """
    num_args= 1
    parser = OptionParser(usage=usage)

    #parser.add_option('-o', '--options', dest='some_option', default='yo', help="Place holder for a real option", type='str')
    #parser.add_option('-u', '--useless', dest='uselesss', default=False, action='store_true', help='Another useless option')
    parser.add_option('-d', '--directory', dest='directory', default='tmp', 
            help='The output directory')

    (options, args) = parser.parse_args()

    if len(args) < num_args:
        parser.print_help()
        sys.exit(1)

    from geopy.geocoders import Nominatim
    geolocator = Nominatim()

    try:
        location = geolocator.geocode(args[0])

        if location is not None:
            with open(op.join(options.directory, args[0].split(',')[0].lower()), 'w') as f:
                out_str = "{} {} {} {}".format(args[0].split(',')[0].lower(), args[0].split(',')[1], location.longitude, location.latitude)
                f.write(out_str)

        print "finished:", args
    except Exception as ex:
        print "exception:", ex
        print "args:", args

if __name__ == '__main__':
    main()

