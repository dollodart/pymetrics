import ast
from math import nan
from algs import lcs_length
from auxcl import NodeDict

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

    def _(self, node):
        self.n += 1
        self.generic_visit(node)

    # I couldn't find a way to dynamically create these methods
    # the problem is the instance passed to the function, if using setattr to set a method
    # will not modify the instance outside the scope of the function

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

    def visit_keyword(self, node):
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
            return nan

    @property
    def comprehensioness(self):
        """Note there is only one n trailing."""
        try: 
            return self.comprehensions / (self.comprehensions + self.loops)
        except ZeroDivisionError:
            return nan

    @property
    def defaultness(self):
        try:
            return self.ndefaults / self.nargs 
        except ZeroDivisionError:
            return nan

    @property
    def statictypeness(self):
        try:
            return self.annassigns / (self.assigns + self.augassigns + self.annassigns)
        except ZeroDivisionError:
            return nan

    # statistics
    @property
    def nestedness(self):
        try:
            return sum(self.expression_lengths) / len(self.expression_lengths)
        except ZeroDivisionError:
            return nan

    @property
    def functionnestedness(self):
        try:
            return self.functiondef_in_functiondef / self.nfuncs
        except ZeroDivisionError:
            return nan

    @property
    def classsize(self):
        try:
            return self.functiondef_in_classdef / self.nclasses
        except ZeroDivisionError:
            return nan

    @property
    def nameslengths(self):
        try:
            return sum(len(x) for x in self.names) / len(self.names)
        except ZeroDivisionError:
            return nan

    # distributions
    @property # idea from Ka-Ping Lee who named his logging package q since it was the least used letter in the alphabet
    def namesalphdistr(self):
        try:
            chars = ''.join(x.lower() for x in self.names)
            return [chars.count(i)/len(chars) for i in 'abcdefghijklmnopqrstuvwxyz']
        except ZeroDivisionError:
            return nan

class RecursiveCounter(Counter):
    """
    Recursive counter instantiates an instance of itself when encountering
    certain nodes. This instantiation may cost memory given the fact that
    Counter objects have many fields. This Counter should be used for
    evaluating distributions of subtree statistics. The merge is expensive.
    """
    def __init__(self):
        super().__init__()
        self.subtrees = []

    def merge(self, other):
        d = other.__dict__
        for k in d:
            setattr(self, k, getattr(self, k) + d[k])
            # this should work for list appending and floats or ints because of + polymorphism

    def postwalk_merge(self):
        for st in self.subtrees:
            st.postwalk_merge()
            self.merge(st)

    def count_visit(self, module):
        self.generic_visit(module)
        self.postwalk_merge()

    def root_visit(self, node):
        # visit method for subtree roots 
        try:
            g = node.body
        except AttributeError:
            g = node.value

        try:
            for el in g:
                self.generic_visit(el)
        except TypeError:
            self.generic_visit(g) # g is not a generator but an element

    def visit_FunctionDef(self, node):
        self.nfuncs += 1
        self.ndecorators += len(node.decorator_list)
        sc = self.__class__()
        sc.root_visit(node)
        self.functiondef_in_functiondef += sc.nfuncs
        self.subtrees.append(sc)

    def visit_ClassDef(self, node):
        self.ndecorators += len(node.decorator_list)
        self.nclasses += 1
        sc = self.__class__()
        sc.root_visit(node)
        self.functiondef_in_classdef += sc.nfuncs
        self.subtrees.append(sc)

    def visit_Expr(self, node):
        sc = self.__class__()
        sc.root_visit(node)
        self.expression_lengths.append(sc.n)
        self.subtrees.append(sc)

class FastCounter(Counter):
    """
    Fast counter doesn't keep the substructure, nor does it descend beyond the
    first level.
    """

    def visit_FunctionDef(self, node):
        self.nfuncs += 1
        self.ndecorators += len(node.decorator_list)

    def visit_ClassDef(self, node):
        self.ndecorators += len(node.decorator_list)
        self.nclasses += 1

    def visit_Expr(self, node):
        # this is a bad estimate because, e.g., a binary operator will make it
        # appear as length 1. you need to descend into the parse tree to get
        # expression lengths in terms of atoms. 
        try:
            self.expression_lengths.append(len(node.value))
        except TypeError:
            pass
