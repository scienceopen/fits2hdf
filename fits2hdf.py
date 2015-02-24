#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fits2hdf.py
===========

FITS to HDF5 conversion utility. This script takes a 
"""

import os
import time
import optparse
import warnings

from fits2hdf.idi import IdiHdulist
from fits2hdf.io.fitsio import *
from fits2hdf.io.hdfio import *


if __name__ == '__main__':
    
    # Parse options and arguments
    parser = optparse.OptionParser(
        usage = 'Usage: %prog input_dir output_dir <options>',
        description  = 'Convert FITS files to HDF5 files in HDFITS format.')
    parser.add_option('-c', '--compression', dest='comp', type='string',
                      help='Data compression. Defaults to none, also lzf, bitshuffle, gzip') 
    parser.add_option('-x', '--extension', dest='ext', type='string', default='fits',
                      help='File extension of FITS files. Defaults to .fits')
    parser.add_option('-v', '--verbosity', dest='vb', type='int', default=0,
                      help='verbosity level (default 0, up to 5)')
    parser.add_option('-w', '--nowarn', dest='warn', action='store_false', default=True,
                      help='Turn off warnings created by FITS parsing')
    (opts, args) = parser.parse_args()
    if len(args) == 2:
        dir_in  = args[0]
        dir_out = args[1]
        comp = opts.comp
        if not os.path.exists(dir_out):
            print "Creating directory %s" % dir_out
            os.mkdir(dir_out)
    else:
        parser.print_usage()
        exit() 

    if not opts.warn:
        warnings.simplefilter("ignore")

    # Create list of files to process
    filelist = os.listdir(dir_in)
    filelist = [fn for fn in filelist if fn.endswith(opts.ext)]

    t1 = time.time()
    file_count = 0
    for filename in filelist:
        file_in = os.path.join(dir_in, filename)
        file_out = os.path.join(dir_out, filename.split('.' + opts.ext)[0] + '.h5')

        a = IdiHdulist()
        try:
            a = read_fits(file_in)
            export_hdf(a, file_out, compression=comp, verbosity=opts.vb)
            print "\nCreating %s" % file_out
            print "Input  filesize: %sB" % os.path.getsize(file_in)
            print "Output filesize: %sB" % os.path.getsize(file_out)
            compfact = float(os.path.getsize(file_in)) / float(os.path.getsize(file_out))
            print "Compression:     %2.2fx" % compfact

            file_count += 1

        except IOError:
            print "ERROR: Cannot load %s" % file_in

    print "\nSUMMARY"
    print "-------"
    print "Files created: %i" % file_count
    print "Time taken:    %2.2fs" % (time.time() - t1)