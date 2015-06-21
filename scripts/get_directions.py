#!/usr/bin/python

import gzip
import itertools as it
import os
import os.path as op
import random
import sys
import time
import urllib2
from optparse import OptionParser

def main():
    usage = """
    python get_directions.py start_lon start_lat end_lon end_lat
    """
    num_args= 3
    parser = OptionParser(usage=usage)

    #parser.add_option('-o', '--options', dest='some_option', default='yo', help="Place holder for a real option", type='str')
    #parser.add_option('-u', '--useless', dest='uselesss', default=False, action='store_true', help='Another useless option')
    parser.add_option('-o', '--output-dir', dest='output_dir', default='/tmp',
            help='output_dir')
    parser.add_option('-c', '--check-existing', dest='check_existing', default=False, action='store_true', help='Check if there are existing entries for that station')

    (options, args) = parser.parse_args()

    if len(args) < num_args:
        parser.print_help()
        sys.exit(1)

    if not op.exists(options.output_dir):
        os.makedirs(options.output_dir)

    args = map(lambda x: x.strip('"'), args)

    url = "http://openls.geog.uni-heidelberg.de/testing2015/route?Start={},{}&End={},{}&Via=&lang=de&distunit=KM&routepref=Fastest&avoidAreas=&useTMC=false&noMotorways=false&noTollways=false&instructions=false".format(args[0], args[1], args[2], args[3])

    filename = op.join(options.output_dir, '_'.join(map(lambda x: x.strip('"'), args)) + ".gz")
    if options.check_existing:
        if op.exists(filename):
            with gzip.open(filename, 'r') as f:
                if len(f.read()) > 0:
                    sys.stdout.write("exists... {}\n".format(filename))
            return

    found = False
    sleep_multiplier = 2

    while not found:
        sleep_multiplier *= 2
        try:
            time.sleep(random.random() * sleep_multiplier)
            u = urllib2.urlopen(url, timeout=60)
            read_text = u.read()

            if len(read_text) < 20:
                found = False
                sys.stdout.write('read_text:' + read_text)
                sys.stdout.write("not found..." + filename + " ... sleep({})\n".format(sleep_multiplier))
                sys.stdout.flush()
                continue

            with gzip.open(filename, 'w') as f:
                found = True
                sys.stdout.write(filename + "\n")
                sys.stdout.flush()
                f.write(read_text)

        except Exception as ex:
            print >>sys.stderr, "Exception:", ex
            pass

if __name__ == '__main__':
    main()


