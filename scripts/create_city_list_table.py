#!/usr/bin/python

import math
import sys
from optparse import OptionParser

def main():
    usage = """
    python create_city_list_table.py city_names

    Create an html table with links to the isochrone maps for each city.
    """
    num_args= 0
    parser = OptionParser(usage=usage)

    #parser.add_option('-o', '--options', dest='some_option', default='yo', help="Place holder for a real option", type='str')
    #parser.add_option('-u', '--useless', dest='uselesss', default=False, action='store_true', help='Another useless option')

    (options, args) = parser.parse_args()

    if len(args) < num_args:
        parser.print_help()
        sys.exit(1)

    num_cols = 4
    num_rows = int(math.ceil(len(args) / float(num_cols)))

    args.sort()
    out_str = ''
    total_output = 0
    out_str += "<table style='width: 550px;'>\n"
    for i in range(num_rows):
        out_str +=  "<tr>\n"
        for j in range(num_cols):
            out_str += "<td>\n"

            output_index = j * num_rows + i

            if output_index < len(args):
                out_str += "<a href='/supp/isochrone_driving/{}'>".format(args[output_index])
                out_str += args[output_index].replace('_', ' ').title()
                out_str += "</a>"

            out_str += "</td>\n"
        out_str += "</tr>\n"

    out_str += "</table>\n"
    print out_str


if __name__ == '__main__':
    main()

