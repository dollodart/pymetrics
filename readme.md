# Motivation

CLI utilities like `find`, `grep`, `wc`, `tree`, and others allow one
to get a fairly good understanding of the structure of a source code
directory. There is a python package for finding function calls and
making a directed graph out of them (pycallgraph). However, there may
be a desire for some intermediate analytics between just files sorted
by count of lines and every function call. This is designed for those
intermediate analytics.

This module makes use of the python abstract syntax tree package to do
source code analytics. The detail of analytics can range from simple
counts by node types to relatively complicated checks for certain
subtree structures.

It would also be possible to use the static code checking programs used in IDEs.

## Kinds of analytics questions


- does this module define more generator functions (count of yield) or standard functions (count of return)?
- does this module define more in-place methods or standard methods (ratio of count of def to count of return)?
- does this module use the "better to beg forgiveness then ask permission" design principle (ratio of count of if/then versus try/except)? 
- does this module use lots of fancy assignments (ratio of count of AugAssign and AnnAssign to count of Assign)?
- does this module do asynchronous evaluation (counts of asynchronous function definitions)?
- does this module have many default values for its arguments (ratio of sum of len(arguments.defaults) to sum of len(arguments.args))?
- does this module do lots of aliasing (ratio of count of non-None alias.asname to count of alias and therefore alias.name)?
- does this module define many global or nonlocal functions (ratio of global and nonlocal declared variables to all assigned variables)

While many of these analytics questions appear trivial by inspection,
there is some advantage in scripting them for (1) large modules, where
inspection of thousands of lines of source code is undesirable and (2)
in automated classification of codes. All of the above questions are
what may be called "composition questions", in analogy to physical
science applications where one asks the simple question of, given a
large number of items with identifiers belonging to different classes in
a system, what is the fraction of each identifier in each class? These
analytics can be easily accomplished, though, simply by walking through
the abstract syntax tree and counting each node type.

The purpose in defining a NodeVisitor is generally to look at the
subtree structure (though this can also be accomplished by iteration
through all nodes). Some analytics using this are

- how nested are the expressions (average number of child nodes in Expr nodes)?
- how many methods do the classes have (average number of FunctionDef nodes in ClassDef nodes)?
- how large are the loop bodies (average number of child nodes in For and While nodes)?

Of course, anytime a question regarding a statistic like the mean is
asked, one can also ask about other statistics (like the standard
deviation), and of course what the shape of the distribution is.

Finally, there may be a desire to compute pairwise comparisons between
objects which are not in the same subtree (other than trivially
the subtree of the module root). Example questions of interest are

- how distinct are the variable names (average length of longest common subsequence between each pair divided by average name length)?

Generally this requires memory of all nodes without structure, except
grouped by their class since most comparisons will be intraclass. This
is done by making a dictionary with keys of node type and a list of
nodes belonging to that type.

# References

Blog post by Viktor Tóth "Entropy of abstract syntax trees", which is
a mathematical quantification of how repetitive the code is. Cyclomatic
complexity is referenced there, but that is a measure of how the
program operates, not just simpler measures such as how many types of
a statement it has. Halstead complexity measures are a general class
of complexity measures, but again they measure complexity, not just
stylistic choice such as importing with or without aliases. 

The python package radon computes these metrics, and common linters,
such as flake8 for python, include such metric calculators. See, for
example, the cyclomatic complexity (=McCabe complexity) script at
https://github.com/PyCQA/mccabe included in flake8.
