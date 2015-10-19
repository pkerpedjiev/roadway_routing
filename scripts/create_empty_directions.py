#!/usr/bin/python

import json
import sys
from optparse import OptionParser

def main():
    usage = """
    python create_empty_connections.py geojson/city

    Create a connections file with just one connection to the moon.
    This will be used to create walking times because the time to
    walk will (almost) always be faster.
    """
    num_args= 1
    parser = OptionParser(usage=usage)

    #parser.add_option('-o', '--options', dest='some_option', default='yo', help="Place holder for a real option", type='str')
    #parser.add_option('-u', '--useless', dest='uselesss', default=False, action='store_true', help='Another useless option')

    (options, args) = parser.parse_args()

    if len(args) < num_args:
        parser.print_help()
        sys.exit(1)

    with open(args[0], 'r') as f:
        line = f.readlines()[0].strip().split()

        lon,lat = line[-2:] 

        connections = [{"duration": 999999999999,
                        "to": { "coordinate": { "y": 0, "x": 0 }},
                        "from" : { "coordinate": { "y": lon, "x": lat}}}]

        print json.dumps(connections)

if __name__ == '__main__':
    main()

