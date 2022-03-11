from counter import FastCounter, RecursiveCounter
from pathlib import Path
import re
import ast

def table_report(mv):
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

def plot_dist(nlines, nchars, nwords, nnodes):
    import matplotlib.pyplot as plt
    y1, y2, y3, x = nlines, nchars, nwords, nnodes
    fig, axs = plt.subplots(nrows=1,ncols=3)
    axs[0].set_ylabel('nnodes')
    axs[0].plot(y1, x, 'o')
    axs[0].set_xlabel('Nlines')
    axs[1].plot(y2, x, 'o')
    axs[1].set_xlabel('Nchars')
    axs[2].plot(y3, x, 'o')
    axs[2].set_xlabel('Nwords')
    plt.show()

# TODO: test node_dict
#def flattened_report(module):
#    nd = mv.make_node_dict(module)
#    print(f'node distinctness {nd.namesdistinctness:.2f}')

def test_counter(mv, path):
    d = {}
    xy = []
    p = Path(path)
    if p.is_dir():
        g = p.glob('**/*')
    else:
        g = (p,)

    for f in g:
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
        xy.append((nlines, nchars, nwords, mv.n))
        
        module = ast.parse(r)
        mv.generic_visit(module)
    return zip(*xy)

if __name__ == '__main__':
    mv = FastCounter()
    nlines, nchars, nwords, nnodes = test_counter(mv, './ase/optimize')
    table_report(mv)
    plot_dist(nlines, nchars, nwords, nnodes)

    ts = './ase/optimize/neb.py'
    mv = RecursiveCounter()
    #nlines, nchars, nwords, nnodes = test_counter(mv, './ase/optimize/neb.py')
    mv.postwalk_merge()
    table_report(mv)
    #plot_dist(nlines, nchars, nwords, nnodes)
