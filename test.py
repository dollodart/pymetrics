from counter import FastCounter, RecursiveCounter
from auxcl import NodeDict
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

def dirstream(path, filters = tuple()):
    """
    This loads all of the modules in the path into memory. This is because
    tests may want to run independently, but is memory inefficient compared to
    evaluating all tests on a single walk through the dir stream and keeping
    only one file in memory at any time.
    """
    p = Path(path)
    if p.is_dir():
        g = p.glob('**/*')
    else:
        g = (p,)

    rr = []
    for f in g:
        if f.suffix != '.py':
            continue
        for filter in filters:
            if not filter(f):
                continue

        try:
            with open(f, 'r') as _:
                r = _.read()
            rr.append(r)
        except Exception as e:
            print('module failed to load')
            print(e)

    return rr

def parsestream(path, filters = tuple()): 
    return [ast.parse(r) for r in dirstream(path, filters)]

def wc(rr):
    xy = []
    for r in rr:
        nlines = r.count('\n')
        nchars = len(r)
        nwords = re.sub('\n\s*', '', r).count(' ') # rough approximation of words
        xy.append((nlines, nchars, nwords))
    return zip(*xy)


if __name__ == '__main__':
    rr = dirstream('./ase/optimize')
    rrm = [ast.parse(r) for r in rr]

    # fc test
    mv = FastCounter()
    mvs = []
    for mod in rrm:
        mv.generic_visit(mod)
        mvs.append(FastCounter())
        mvs[-1].generic_visit(mod)

    table_report(mv)

    # run a distribution w.r.t. module

    nlines, nchars, nwords = wc(rr)
    plot_dist(nlines, nchars, nwords, [mv.n for mv in mvs])

    # ndict test
    ndict = NodeDict()
    for rr in rrm:
        ndict.accumulate(mod)
    #print(ndict.namesdistinctness) # slow

    # rc test
    rr2 = dirstream('./ase/optimize/neb.py')
    mv = RecursiveCounter()
    mv.generic_visit(ast.parse(rr2[0]))

    # this isn't the value in Recursive Counter
    mv.postwalk_merge()
    table_report(mv)

    # a distribution of subtree statistics is of value (though it requires a similar merging procedure)
    l = []
    def recur_n(mv):
        l.append(mv.n)
        for st in mv.subtrees:
            recur_n(st)
    print(sorted(l))
