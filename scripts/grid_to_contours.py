#!/usr/bin/python

import json
import math
import matplotlib.pyplot as plt
import numpy as np
import sys
from optparse import OptionParser

def grid_to_contours(grid_json, levels):
    '''
    Convert a grid json file to a set of contours.

    @param grid_json: A hash map containing the values 'grid_z', 'min_x', 'max_x', 'min_y', 'max_y'
    @param levels: A sorted list of levels between which to draw the filled contour plot
    @param return: An array of dictionaries {'path': {'x':1, 'y':2, 'type', 'L'}, 'level':4.17, 'k':0}
    '''
    x_res = len(grid_json['grid_z'])
    y_res = len(grid_json['grid_z'][0])

    xs = np.linspace(grid_json['min_x'], grid_json['max_x'], x_res)
    ys = np.linspace(grid_json['min_y'], grid_json['max_y'], y_res)

    X, Y = np.meshgrid(xs, ys)
    Z = np.array(grid_json['grid_z'])

    cs = plt.contourf(X, Y, Z.T, levels)
    #plt.show()

    new_contours = []

    for i, collection in enumerate(cs.collections):
        for path in collection.get_paths():
            coords = path.vertices
            new_contour = {}
            new_contour['path'] = []
            new_contour['level'] = i
            new_contour['k'] = i
            
            prev_coords = None

            for (coords, code_type) in zip(path.vertices, path.codes):

                '''
                if prev_coords is not None and np.allclose(coords, prev_coords):
                    continue
                '''
                
                prev_coords = coords

                #print >>sys.stderr, "coords, code_type:", coords, code_type, i
                
                if code_type == 1:
                    new_contour['path'] += [['M', float('{:.3f}'.format(coords[0])),float('{:.3f}'.format(coords[1])) ]]
                elif code_type == 2:
                    new_contour['path'] += [['L', float('{:.3f}'.format(coords[0])),float('{:.3f}'.format(coords[1])) ]]
                    
            new_contours += [new_contour]

    return new_contours

def main():
    usage = """
    python grid_to_contours.py grid.json

    Convert a grid of data values to a list of contours.
    """
    num_args= 1
    parser = OptionParser(usage=usage)

    parser.add_option('-i', '--interval', dest='interval', default=2, 
            help="The interval to which the contours correspond (in hours)", 
            type=float)
    parser.add_option('', '--min-level', dest='min_level', default=0,
                      help='The first level')
    parser.add_option('', '--max-level', dest='max_level', default=24,
                      help='The last level')
    parser.add_option('', '--num-levels', dest='num_levels', default=13,
                      help='The number of levels')
    #parser.add_option('-o', '--options', dest='some_option', default='yo', help="Place holder for a real option", type='str')
    #parser.add_option('-u', '--useless', dest='uselesss', default=False, action='store_true', help='Another useless option')

    (options, args) = parser.parse_args()

    if len(args) < num_args:
        parser.print_help()
        sys.exit(1)

    if args[0] == '-':
        f = sys.stdin
    else:
        f = open(args[0], 'r')

    levels = [((i + 0.125) * 60 ) for i in np.linspace(options.min_level, options.max_level, options.num_levels)]


    print >>sys.stderr, "args[0]:", args[0]
    grid_json = json.load(f)
    contours = grid_to_contours(grid_json,levels)
    print json.dumps(contours, separators=(',', ':'))

    f.close()
    

if __name__ == '__main__':
    main()

