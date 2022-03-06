from counter import Counter
from pathlib import Path
import re
import ast

d = {}

xy = []
mv = Counter()
for f in Path('./ase/optimize/gpmin').glob('**/*'):
    if f.suffix != '.py':
        continue
    with open(f, 'r') as _:
        r = _.read()
    
    # these can be compared with counts found from parsing
    # should be roughly correlated
    f = str(f)

    nlines = r.count('\n')
    nchars = len(r)
    nwords = re.sub('\n\s*', '', r).count(' ') # rough approximation of words
    
    module = ast.parse(r)
    mv.count_visit(module)
    xy.append((nlines, nchars, nwords, mv.n))

print(f'count comparators={mv.comparators}')
print(f'comprehensioness {mv.comprehensioness:.2f}')
print(f'decoratedness {mv.statictypeness:.2f}')
print(f'descopedness {mv.descopedness:.2f}')
print(f'import aliasingness {mv.importaliasingness:.2f}')
print(f'import fromness {mv.importfromness:.2f}')
print(f'kwarg defaultness {mv.defaultness:.2f}')
print(f'statictypeness {mv.statictypeness:.2f}')
print(f'expression nestedness {mv.nestedness:.1f}')
print(f'function nestedness {mv.functionnestedness:.1f}')
print(f'average number of methods in class {mv.classsize:.1f}')
print(f'average character length of a name {mv.nameslengths:.1f}')
print(f'a-z character distribution {[round(x*100) for x in mv.namesalphdistr]}')

nd = mv.make_node_dict(module)
print(f'node distinctness {nd.namesdistinctness:.2f}')

import matplotlib.pyplot as plt
y1, y2, y3, x = zip(*xy)
fig, axs = plt.subplots(nrows=1,ncols=3)
axs[0].set_ylabel('nnodes')
axs[0].plot(y1, x, 'o')
axs[0].set_xlabel('Nlines')
axs[1].plot(y2, x, 'o')
axs[1].set_xlabel('Nchars')
axs[2].plot(y3, x, 'o')
axs[2].set_xlabel('Nwords')
plt.show()
