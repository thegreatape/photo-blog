import os

for f in os.listdir('_posts'):
    f = '_posts/%s' % f
    lines = open(f).readlines()
    lines.insert(1, "layout: post\n")
    open(f,'w').write("".join(lines))
