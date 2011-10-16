#!/usr/bin/env python
import sys
from jscat import Maker

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-I", "--include-dir", help="adds INCLUDE_DIR to the import path. This option may be given multiple times.", action="append", default=[])
    parser.add_option("-o", "--output", help="write to OUTPUT instead of stdout")
    parser.add_option("-k", "--keep-order", help="keep files in the same order they were specified on the commandline", action="store_true", default=False)
    parser.add_option("-d", "--keep-dependency-order", help="keep files in the same order they were listed in source files", action="store_true", default=False)

    options, args = parser.parse_args()
    maker = Maker(include_dirs=options.include_dir, keep_order=options.keep_order, keep_dependency_order=options.keep_dependency_order)
    maker.load(*args)
    if options.output:
        with open(options.output, 'w') as out:
            maker.write(out)
    else:
        maker.write(sys.stdout)

if __name__ == '__main__':
    main()
    