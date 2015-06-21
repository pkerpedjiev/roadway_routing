#!/usr/bin/python

import json
import sys
from optparse import OptionParser

def parse_distances(filename):
    with open(filename, 'r') as f:
        try:
            data = json.loads(f.read())
        except Exception as e:
            print >>sys.stderr, "Error decoding JSON", filename, e
            return []

        small_data = []
        for path in data['paths']:
            small_data +=  [{'from': { 'coordinate': 
                                { 'x': path['startPoint']['lat'],
                                  'y': path['startPoint']['lon'] }},
                             'to': { 'coordinate':
                                 { 'x': path['endPoint']['lat'],
                                   'y': path['endPoint']['lon']}},
                              'duration': path['time'] / (60 * 1000)}]
            fastest = sorted(small_data, key=lambda x: x['duration'])

            if len(fastest) == 0:
                return []

            return [fastest[0]]

def main():
    usage = """
    python parse_distances.py distances_output.json    
    """
    num_args= 0
    parser = OptionParser(usage=usage)

    #parser.add_option('-o', '--options', dest='some_option', default='yo', help="Place holder for a real option", type='str')
    #parser.add_option('-u', '--useless', dest='uselesss', default=False, action='store_true', help='Another useless option')

    parser.add_option('-l', '--file-list', dest='file_list', default=False, action='store_true', help='The input is actually a file containing a list of files')

    (options, args) = parser.parse_args()

    if len(args) < num_args:
        parser.print_help()
        sys.exit(1)

    data = []

    if options.file_list:
        with open(args[0], 'r') as f:
            for line in f:
                data += parse_distances(line.strip())
    else:
        for arg in args:
            data += parse_distances(arg)    

    import copy

    data += [copy.deepcopy(data[-1])]
    data[-1]['to'] = data[-1]['from']
    data[-1]['duration'] = 0

    print >>sys.stderr, "done"
    print json.dumps(data, indent=2)

if __name__ == '__main__':
    main()

