# Copyright 2006 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Fixer for apply().

This converts apply(func, v, k) into (func)(*v, **k)."""

# Local imports
from .. import pytree
from ..pgen2 import token
from .. import fixer_base
from ..fixer_util import Call, Comma, parenthesize


class FixApply(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = """
    power< 'apply'
        trailer<
            '('
            arglist<
                (not argument<NAME '=' any>) func=any ','
                (not argument<NAME '=' any>) args=any [','
                (not argument<NAME '=' any>) kwds=any] [',']
            >
            ')'
        >
    >
    """

    def transform(self, node, results):
        sym_s = self.sym_s
        assert results
        func = results["func"]
        args = results["args"]
        kwds = results.get("kwds")
        # I feel like we should be able to express this logic in the
        # PATTERN above but I don't know how to do it so...
        if args:
            if args.type == sym_s.star_expr:
                return  # Make no change.
            if (args.type == sym_s.argument and
                args.children[0].value == '**'):
                return  # Make no change.
        if kwds and (kwds.type == sym_s.argument and
                     kwds.children[0].value == '**'):
            return  # Make no change.
        prefix = node.prefix
        func = func.clone()
        if (func.type not in (token.NAME, sym_s.atom) and
            (func.type != sym_s.power or
             func.children[-2].type == token.DOUBLESTAR)):
            # Need to parenthesize
            func = parenthesize(func)
        func.prefix = ""
        args = args.clone()
        args.prefix = ""
        if kwds is not None:
            kwds = kwds.clone()
            kwds.prefix = ""
        l_new_args = [pytree.Leaf(token.STAR, "*"), args]
        if kwds is not None:
            l_new_args.extend([Comma(),
                              pytree.Leaf(token.DOUBLESTAR, "**"),
                              kwds])
            l_new_args[-2].prefix = " "
        return Call(func, l_new_args, prefix=prefix)
