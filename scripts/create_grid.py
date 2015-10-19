#!/usr/bin/python

import sys
import json
from optparse import OptionParser

sys.path.append('..')

import plot_travel_times as ptt

def main():
    usage = """
    python create_grid.py all_connections_x.csv

    Calculate an y x y grid for the travel times in the entire region.
    """
    num_args= 1
    parser = OptionParser(usage=usage)

    parser.add_option('-m', '--method', dest='method', default='time', help='which method to calculate the distance using', type='str')

    parser.add_option('-r', '--resolution', dest='resolution', default=4, 
            help="The resolution we want the grid to be at", type='int')
    parser.add_option('-o', '--output-file', dest='output_file', default=None,
            help="A file to dump the output to", type='str')
    parser.add_option('-d', '--old', dest='old', action='store_true', default=False,
            help='Use old grid function')
    parser.add_option('-a', '--haversine', dest='haversine', action='store_true', default=False,
            help='Use the haversine distance to create the grid')

    parser.add_option('', '--walking-speed', dest='walking_speed', default=5,
            help='The speed with which one transports oneself from a train station \
                  to somewhere else', type='float')

    #parser.add_option('-u', '--useless', dest='uselesss', default=False, action='store_true', help='Another useless option')

    (options, args) = parser.parse_args()

    if len(args) < num_args:
        parser.print_help()
        sys.exit(1)

    print >>sys.stderr, "res:", options.resolution
    (distances, xs, ys, zs, from_x, from_y) = ptt.get_connection_coordinates_and_times(args[0])

    print >>sys.stderr, "xs:", min(xs), max(xs)
    print >>sys.stderr, "ys:", min(ys), max(ys)

    options.min_x = min(xs)
    options.min_y = min(ys)

    options.max_x = max(xs)
    options.max_y = max(ys)
    
    sys.setrecursionlimit(8500)

    if options.method == 'time':
        if options.old:
            (grid_x, grid_y, grid_z, min_x, max_x, min_y, max_y) = ptt.create_grid(distances, xs, ys, zs, complex(0, options.resolution))
        else:
            print >>sys.stderr, "creating time grid"
            (grid_x, grid_y, grid_z, min_x, max_x, min_y, max_y) = ptt.create_grid2(distances, xs, ys, zs, complex(0, options.resolution), options.min_x, options.max_x, options.min_y, options.max_y, walking_speed = options.walking_speed)
    elif options.method == 'speed':
            (grid_x, grid_y, grid_z, min_x, max_x, min_y, max_y) = ptt.create_grid2(distances, xs, ys, zs, complex(0, options.resolution), options.min_x, options.max_x, options.min_y, options.max_y, walking_speed = options.walking_speed)

            grid_z = ptt.calc_speed_grid(grid_x, grid_y, grid_z, from_x, from_y)
    else:
        print >>sys.stderr, "Invalid method... choose one of 'time' or 'speed'"
        sys.exit(1)

    if options.output_file is None:
        json.dump({'grid_z':[list(map(int, g)) for g in grid_z], 'min_x':min_x,
                   'max_x': max_x, 'min_y': min_y, 'max_y': max_y}, sys.stdout)
    else:
        with open(options.output_file, 'w') as f:
            json.dump({'grid_z':[list(map(int, g)) for g in grid_z], 'min_x': min_x, 
                       'max_x': max_x, 'min_y': min_y, 'max_y': max_y}, f)

if __name__ == '__main__':
    main()

