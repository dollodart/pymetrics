import ast
def lcs_length(x,y):
    """See CLRS section 15.4"""
    m = len(x) 
    n = len(y)
    c = [[0]*n]*m
    for i in range(1, m):
        c[i][0] = 0
    for j in range(n):
        c[0][j] = 0

    for i in range(1, m):
        for j in range(1, n):
            if x[i] == y[j]:
                c[i][j] = c[i-1][j-1] + 1
            elif c[i-1][j] >= c[i][j-1]:
                c[i][j] = c[i-1][j]
            else:
                c[i][j] = c[i][j-1]
    return c[m-1][n-1]

# test case
if __name__ == '__main__':
    l = lcs_length('bdcaba', 'abcdbdab')
    print(l)


class NodeDict(dict):
    @property
    def namesdistinctness(self):
        names = self[ast.Name]
        n = len(names)
        l = 0
        ll = 0
        for i in range(n):
            for j in range(i):
                n1 = names[i].id
                n2 = names[j].id
                l += 2*lcs_length(n1, n2)
                ll += len(n1) + len(n2)
        return l / ll

class Counter(ast.NodeVisitor):

    def __init__(self):
        super().__init__()
        self.l = []

        self.n = 0
        self.expression_lengths = []
        for i in ('add', 'sub', 'mult', 'div', 'gt', 'lt', 
                  'eq', 'lte', 'gte', 'floordiv', 'mod', 
                  'pow', 'lshift', 'rshift', 'bitor', 
                  'bitxor', 'bitand', 'matmult', 'is_', 'isnot', 'in_', 'notin'):
            setattr(self, i, 0)

        for i in ('nonlocals', 'globals', 'breaks', 'continues', 'fors', 'whiles', 'tries',
                  'imports', 'fromimports', 'setcomps', 'dictcomps', 'listcomps', 'assigns', 'augassigns', 'annassigns'):
            setattr(self, i, 0)

        for i in ('nargs', 'ndefaults', 'imports_asis', 'imports_aliased', 'fromimports_asis', 'fromimports_aliased'):
            setattr(self, i, 0)

        self.functiondef_in_classdef = 0
        self.functiondef_in_functiondef = 0
        self.nclasses = 0
        self.nfuncs = 0
        self.ndecorators = 0

        self.names = []

    # I couldn't find a way to dynamically create these methods
    # the problem is the instance passed to the function, if using setattr to set a method
    # will not modify the instance outside the scope of the function

    def make_node_dict(self, node):
        """Return a dictionary of nodes by class (removes all structure)."""

        self.node_dict = NodeDict()
        self.node_dict[node.__class__] = [node]
        for i in ast.walk(node):
            c = i.__class__
            if c in self.node_dict.keys():
                self.node_dict[c].append(i)
            else:
                self.node_dict[c] = [i]
        return self.node_dict

    def _(self, node):
        self.n += 1
        self.generic_visit(node)

    # Binary Operators
    def visit_Add(self, node):
        self.add += 1
        self._(node)
    def visit_Sub(self, node):
        self.sub += 1
        self._(node)
    def visit_Mult(self, node):
        self.mult += 1
        self._(node)
    def visit_Div(self, node):
        self.div += 1
        self._(node)
    def visit_Gt(self, node):
        self.gt += 1
        self._(node)
    def visit_Lt(self, node):
        self.lt += 1
        self._(node)
    def visit_LtE(self, node):
        self.lte += 1
        self._(node)
    def visit_GtE(self, node):
        self.gte += 1
        self._(node)
    def visit_FloorDiv(self, node):
        self.floordiv += 1
        self._(node)
    def visit_Mod(self, node):
        self.mod += 1
        self._(node)
    def visit_Pow(self, node):
        self.pow += 1
        self._(node)
    def visit_LShift(self, node):
        self.lshift += 1
        self._(node)
    def visit_RShift(self, node):
        self.rshift += 1
        self._(node)
    def visit_BitOr(self, node):
        self.bitor += 1
        self._(node)
    def visit_BitXor(self, node):
        self.bitxor += 1
        self._(node)
    def visit_BitAnd(self, node):
        self.bitand += 1
        self._(node)
    def visit_MatMult(self, node):
        self.matmult += 1
        self._(node)
    def visit_Is(self, node):
        self.is_ += 1
        self._(node)
    def visit_IsNot(self, node):
        self.isnot += 1
        self._(node)
    def visit_In(self, node):
        self.in_ += 1
        self._(node)
    def visit_NotIn(self, node):
        self.notin += 1
        self._(node)
        
    # the following collect information at the base level
    # methods on parent nodes would have to be defined to know the parents of name leaves (the most common leaf)
    def visit_Name(self, node):
        self.names.append(node.id)
        self._(node)

    def visit_alias(self, node):
        self._(node)

    def visit_Attr(self, node):
        self._(node)

    def visit_Assign(self, node):
        self.assigns += len(node.targets)
        self._(node)

    def visit_AugAssign(self, node):
        self.augassigns += 1
        self._(node)

    def visit_AnnAssign(self, node):
        self.annassigns += 1
        self._(node)

    def visit_FunctionDef(self, node):
        self.nfuncs += 1
        self.ndecorators += len(node.decorator_list)
        sc = Counter()
        sc.generic_visit(node)
        self.functiondef_in_functiondef += sc.nfuncs - 1
        self._(node)

    def visit_keyword(self, node):
        self._(node)

    def visit_ClassDef(self, node):
        self.ndecorators += len(node.decorator_list)
        self.nclasses += 1
        sc = Counter()
        sc.generic_visit(node)
        self.functiondef_in_classdef += sc.nfuncs - 1
        self._(node)

    def visit_Global(self, node):
        self.globals += len(node.names)
        self._(node)

    def visit_Nonlocal(self, node):
        self.nonlocals += len(node.names)
        self._(node)

    def visit_Break(self, node):
        self.breaks += 1
        self._(node)

    def visit_Continue(self, node):
        self.continues += 1
        self._(node)

    def visit_For(self, node):
        self.fors += 1
        self._(node)

    def visit_While(self, node):
        self.whiles += 1
        self._(node)

    def visit_Try(self, node):
        self.tries += 1
        self._(node)

    def visit_Expr(self, node):
        count = 0
        sc = Counter()
        sc.generic_visit(node)
        self.expression_lengths.append(sc.n)
        self._(node)

    def visit_Import(self, node):
        self.imports += 1
        for alias in node.names:
            if alias.asname is None:
                self.imports_asis += 1
            else:
                self.imports_aliased += 1

        self._(node)

    def visit_ImportFrom(self, node):
        self.fromimports += 1
        for alias in node.names:
            if alias.asname is None:
                self.fromimports_asis += 1
            else:
                self.fromimports_aliased += 1

        self._(node)

    def visit_arguments(self, node):
        self.nargs += len(node.args)
        self.ndefaults += len(node.defaults)
        self._(node)

    def visit_ListComp(self, node):
        self.listcomps += 1
        self._(node)

    def visit_SetComp(self, node):
        self.setcomps += 1
        self._(node)

    def visit_DictComp(self, node):
        self.dictcomps += 1
        self._(node)

    # counts of classes
    @property
    def comprehensions(self):
        return self.listcomps + self.setcomps + self.dictcomps

    @property
    def control_statements(self):
        return self.breaks + self.continues

    @property
    def loops(self):
        return self.fors + self.whiles

    @property
    def descoped(self):
        """Returns count of variables which are 'descoped', either to the outside scope or globally, when defined."""
        return self.nonlocals + self.globals

    @property
    def comparators(self):
        return self.gt + self.lt + self.eq + self.gte + self.lte + self.is_ + self.isnot + self.in_ + self.notin

    # compositions

    @property
    def decoratedness(self):
        return self.ndecorations / (self.nclasses + self.nfuncs)

    @property
    def descopedness(self):
        return self.descoped / (self.descoped + self.assigns)

    @property
    def importfromness(self):
        return self.fromimports / (self.fromimports + self.imports)

    @property
    def importaliasingness(self):
        """

        Usually modules have a standard alias they use for shortening, especially for submodules, e.g.,

        import numpy as np
        import numpy.linalg as la

        When using functions from a module, how often are they
        aliased. Unless the package aliases in their own docs, e.g.,
        `from scipy.linalg import Rotation as R` or the function will
        have a name conflict, most packages do not alias.

        """
        try:
            return (self.imports_aliased + self.fromimports_aliased) /\
                   (self.imports_asis + self.imports_aliased + self.fromimports_aliased + self.fromimports_asis)
        except ZeroDivisionError:
            return None

    @property
    def comprehensioness(self):
        """Note there is only one n trailing."""
        try: 
            return self.comprehensions / (self.comprehensions + self.loops)
        except ZeroDivisionError:
            return None

    @property
    def defaultness(self):
        try:
            return self.ndefaults / self.nargs 
        except ZeroDivisionError:
            return None

    @property
    def statictypeness(self):
        try:
            return self.annassigns / (self.assigns + self.augassigns + self.annassigns)
        except ZeroDivisionError:
            return None

    # statistics
    @property
    def nestedness(self):
        try:
            return sum(self.expression_lengths) / len(self.expression_lengths)
        except ZeroDivisionError:
            return None

    @property
    def functionnestedness(self):
        try:
            return self.functiondef_in_functiondef / self.nfuncs
        except ZeroDivisionError:
            return None

    @property
    def classsize(self):
        try:
            return self.functiondef_in_classdef / self.nclasses
        except ZeroDivisionError:
            return None

    @property
    def nameslengths(self):
        try:
            return sum(len(x) for x in self.names) / len(self.names)
        except ZeroDivisionError:
            return None

    # distributions
    @property # idea from Ka-Ping Lee who named his logging package q since it was the least used letter in the alphabet
    def namesalphdistr(self):
        try:
            chars = ''.join(x.lower() for x in self.names)
            return [chars.count(i)/len(chars) for i in 'abcdefghijklmnopqrstuvwxyz']
        except ZeroDivisionError:
            return None
