#!/usr/bin/python

import sys
from optparse import OptionParser

template = """
 ---
  layout: isochrone_driving_details
  title:  "Isochrone Map for Train Travel from {{city_full}}"
  tags: maps javascript leaflet isochrone
  city: {{city_replaced}}
  latitude: {{latitude}}
  longitude: {{longitude}}
  ---

<script type="text/javascript">
      drawIsochroneMap({{ page.latitude }}, {{ page.longitude }}, '/jsons/isochrone_driving_contours/{{page.city | downcase}}.json');
      </script>
"""

def main():
    usage = """
    python create_emptypipes_page.py geocode_file

    The geocode file should contain just one line:

    los_angeles  CA -118.2427266 34.053717
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
        (city, country, longitude, latitude) = line.strip().split()

        text = template.replace('{{city_full}}', " ".join(map(lambda x: x.capitalize(), city.split('_'))))
        text = text.replace("{{city_replaced}}", city)
        text = text.replace("{{latitude}}", latitude)
        text = text.replace("{{longitude}}", longitude)

        print text

if __name__ == '__main__':
    main()

