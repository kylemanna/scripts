#!/usr/bin/env python
# Update a Eclipse .cdtfile with the Linux autoconf.h defines
# Copyright 2008 Simon Kagstrom
# Released under the GPLv3, see http://www.gnu.org/licenses/
#
# Updated by Kyle Manna
# To use this, export __KERNEL__ symbol prior to use so that the script
# knows where to start modifying the .cprojects file

import sys

stuff_to_add = []

if len(sys.argv) != 3:
    print "Usage: xxx.py autoconf.h eclipse-project-path-to-update"
    sys.exit(1)

f = open(sys.argv[1])

for line in f:
    line = line[:-1].replace("\"", "&quot;")
    words = line.split(None, 3)
    if len(words) == 0:
        continue
    if words[0] == "#define":
        if len(words) > 2:
            stuff_to_add.append("<listOptionValue builtIn=\"false\" value=\"%s=%s\"/> <!--GENERATED-->" % (words[1], words[2]))
        else:
            stuff_to_add.append("<listOptionValue builtIn=\"false\" value=\"%s=1\"/> <!--GENERATED-->" % (words[1]))

cur_config=open(sys.argv[2] + "/.cproject").readlines()

out = open(sys.argv[2] + "/.cproject", "w")

found = False
for line in cur_config:
    if line.find("valueType=\"definedSymbols\"") != -1:
        out.write(line)
        for generated in stuff_to_add:
            out.write(generated + "\n")
        continue
    if line.find("<!--GENERATED-->") != -1:
        continue
    out.write(line)

out.close()
