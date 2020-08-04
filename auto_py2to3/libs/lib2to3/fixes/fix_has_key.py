# Copyright 2006 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Fixer for has_key().

Calls to .has_key() methods are expressed in terms of the 'in'
operator:

    d.has_key(k) -> k in d

CAVEATS:
1) While the primary target of this fixer is dict.has_key(), the
   fixer will change any has_key() method call, regardless of its
   class.

2) Cases like this will not be converted:

    m = d.has_key
    if m(k):
        ...

   Only *calls* to has_key() are converted. While it is possible to
   convert the above to something like

    m = d.__contains__
    if m(k):
        ...

   this is currently not done.
"""

# Local imports
from .. import pytree
from .. import fixer_base
from ..fixer_util import Name, parenthesize


class FixHasKey(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = """
    anchor=power<
        before=any+
        trailer< '.' 'has_key' >
        trailer<
            '('
            ( not(arglist | argument<any '=' any>) arg=any
            | arglist<(not argument<any '=' any>) arg=any ','>
            )
            ')'
        >
        after=any*
    >
    |
    negation=not_test<
        'not'
        anchor=power<
            before=any+
            trailer< '.' 'has_key' >
            trailer<
                '('
                ( not(arglist | argument<any '=' any>) arg=any
                | arglist<(not argument<any '=' any>) arg=any ','>
                )
                ')'
            >
        >
    >
    """

    def transform(self, node, results):
        assert results
        sym_s = self.syms
        if (node.parent.type == sym_s.not_test and
            self.pattern.match(node.parent)):
            # Don't transform a node matching the first alternative of the
            # pattern when its parent matches the second alternative
            return None
        negation = results.get("negation")
        anchor = results["anchor"]
        prefix = node.prefix
        before = [n.clone() for n in results["before"]]
        arg = results["arg"].clone()
        after = results.get("after")
        if after:
            after = [n.clone() for n in after]
        if arg.type in (sym_s.comparison, sym_s.not_test, sym_s.and_test,
                        sym_s.or_test, sym_s.test, sym_s.lambdef, sym_s.argument):
            arg = parenthesize(arg)
        if len(before) == 1:
            before = before[0]
        else:
            before = pytree.Node(sym_s.power, before)
        before.prefix = " "
        n_op = Name("in", prefix=" ")
        if negation:
            n_not = Name("not", prefix=" ")
            n_op = pytree.Node(sym_s.comp_op, (n_not, n_op))
        new = pytree.Node(sym_s.comparison, (arg, n_op, before))
        if after:
            new = parenthesize(new)
            new = pytree.Node(sym_s.power, (new,) + tuple(after))
        if node.parent.type in (sym_s.comparison, sym_s.expr, sym_s.xor_expr,
                                sym_s.and_expr, sym_s.shift_expr,
                                sym_s.arith_expr, sym_s.term,
                                sym_s.factor, sym_s.power):
            new = parenthesize(new)
        new.prefix = prefix
        return new
