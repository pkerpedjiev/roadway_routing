#!/usr/bin/python

import itertools as it
import numpy as np
import sys
from optparse import OptionParser

def main():
    usage = """
    python create_grid.py
    """
    num_args= 0
    parser = OptionParser(usage=usage)

    parser.add_option('-r', '--resolution', dest='resolution', default=4, 
            help="The resolution we want the grid to be at", type='int')
    parser.add_option('-o', '--output-file', dest='output_file', default=None,
            help="A file to dump the output to", type='str')
    parser.add_option('', '--min-x', dest='min_x', default=None,
            help='The minimum longitude', type='float')
    parser.add_option('', '--max-x', dest='max_x', default=None,
            help='The maximum longitude', type='float')
    parser.add_option('', '--min-y', dest='min_y', default=None,
            help='The minimum latitude', type='float')
    parser.add_option('', '--max-y', dest='max_y', default=None,
            help='The maximum latitude', type='float')

    #parser.add_option('-o', '--options', dest='some_option', default='yo', help="Place holder for a real option", type='str')
    #parser.add_option('-u', '--useless', dest='uselesss', default=False, action='store_true', help='Another useless option')

    (options, args) = parser.parse_args()

    xs = np.linspace(options.min_x, options.max_x, options.resolution)
    ys = np.linspace(options.min_y, options.max_y, options.resolution)

    from mpl_toolkits.basemap import Basemap

    my_map = Basemap(llcrnrlon=options.min_x,llcrnrlat=options.min_y,
                  urcrnrlon=options.max_x,urcrnrlat=options.max_y,\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',area_thresh=1000.,projection='merc',\
                lat_1=50.,lon_0=-107.)# draw coastlines, country boundaries, fill continents.

    is_land = dict()

    for x, y in it.product(xs, ys):
        mx, my = my_map(x, y)

        if my_map.is_land(mx, my):
            print x, y

    (options, args) = parser.parse_args()

    if len(args) < num_args:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()

