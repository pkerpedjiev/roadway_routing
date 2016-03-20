#!/usr/bin/python

import sys
from optparse import OptionParser

def main():
    usage = """
    python create_isochrone_driving_template geocodes_file

    The geocodes file should look like this:

    dar_es_salaam Tanzania 39.2803756 -6.8142737

    The output will be a jekyll template for creating
    the driving isochrone for this city.
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
        line = f.readlines()[0]
        city_name, country, longitude, latitude = line.split()

    real_city_name = city_name.replace('_',' ').title()
    template = """---
layout: isochrone_driving_details
title:  "Isochrone Map for Driving from {}"
tags: maps javascript leaflet isochrone
city: {} 
real_city_name: {}
latitude: {}
longitude: {}
---
""".format(real_city_name, city_name, real_city_name, latitude, longitude)

    template += """
<script type="text/javascript">
        drawIsochroneMap({{ page.latitude }}, {{ page.longitude }}, '/jsons/isochrone_driving_contours/{{page.city | downcase}}.json');
        </script>
"""
    print template

if __name__ == '__main__':
    main()

