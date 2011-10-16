import os
import re
import sys

_require_re = re.compile(r'^//=\s*require\s*(?P<q>["<])(?P<path>[^"]+)[">]\s*$')

class Maker(object):
    def __init__(self, include_dirs=(), keep_order=True, keep_dependency_order=True, closure_wrapped=False):
        self.include_dirs = include_dirs
        self.dependencies = {}
        self.keep_order = keep_order
        self.keep_dependency_order = keep_dependency_order
        self.closure_wrapped = closure_wrapped
        self.files = set()

    def find_path(self, path):
        for base in self.include_dirs:
            f = os.path.join(base, path)
            if os.path.exists(f):
                return f
            elif os.path.exists(f + '.js'):
                return f + '.js'
        return None
        
    def add_dependency(self, src, dep):
        self.dependencies.setdefault(src, set()).add(dep)

    def load(self, *src_files):
        self.files |= set(src_files)

        if self.keep_order:
            for i in xrange(0, len(src_files) - 1):
                self.add_dependency(src_files[i+1], src_files[i])

        queue = list(src_files)
        while queue:
            src = queue.pop()
            basedir = os.path.dirname(src)
            last_dep = None
            for line in open(src, 'r'):
                match = _require_re.match(line)
                if not match:
                    continue
                path = match.group('path')
                q = match.group('q')
                if q == '"':
                    path = os.path.join(basedir, path)
                elif q == '<':
                    name = self.find_path(path)
                    if not name:
                        sys.stderr.write('Cannot find <%s>. Aborting.\n' % path)
                        sys.exit(1)
                    path = name
                self.add_dependency(src, path)
                if path not in self.files:
                    queue.append(path)
                self.files.add(path)
                if last_dep and self.keep_dependency_order:
                    self.add_dependency(path, last_dep)
                last_dep = path
    
    def sort(self):
        order = []
        files = set(self.files)
        while files:
            found = False
            for src in files:
                deps = self.dependencies.get(src)
                if not deps or all(dep in order for dep in deps):
                    files.remove(src)
                    order.append(src)
                    found = True
                    break
            if not found:
                sys.stderr.write("Found cyclic dependencies:\n")
                sys.stderr.write("%s\n" % "\n".join(all_files))
                sys.exit(2)
        return order

    def write(self, out):
        for path in self.sort():
            if self.closure_wrapped:
                out.write('(function(){\n')
            with open(path, 'r') as src:
                out.write(src.read())
            if self.closure_wrapped:
                out.write('})();\n')


def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-I", "--include-dir", help="adds INCLUDE_DIR to the import path. This option may be given multiple times.", action="append", default=[])
    parser.add_option("-o", "--output", help="write to OUTPUT instead of stdout")
    parser.add_option("-k", "--keep-order", help="keep files in the same order they were specified on the commandline", action="store_true", default=False)
    parser.add_option("-d", "--keep-dependency-order", help="keep files in the same order they were listed in source files", action="store_true", default=False)
    parser.add_option("-c", "--closure-wrapped", help="wrap all source files in closures")

    options, args = parser.parse_args()
    maker = Maker(
        include_dirs=options.include_dir, 
        keep_order=options.keep_order, 
        keep_dependency_order=options.keep_dependency_order, 
        closure_wrapped=options.closure_wrapped, 
    )
    maker.load(*args)
    if options.output:
        with open(options.output, 'w') as out:
            maker.write(out)
    else:
        maker.write(sys.stdout)

if __name__ == '__main__':
    main()
    