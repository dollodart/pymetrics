import ast
from algs import lcs_length

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

    def accumulate(self, node):
        """Return a dictionary of nodes by class (removes all structure)."""

        self[node.__class__] = [node]
        for i in ast.walk(node):
            c = i.__class__
            if c in self.keys():
                self[c].append(i)
            else:
                self[c] = [i]
        return self

