# Copyright 2006 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Pattern compiler.

The grammar is taken from PatternGrammar.txt.

The compiler compiles a pattern to a pytree.*Pattern instance.
"""

__author__ = "Guido van Rossum <guido@python.org>"

# Python imports
import io

# Fairly local imports
from .pgen2 import driver, literals, token, tokenize, parse, grammar

# Really local imports
from . import pytree
from . import pygram


class PatternSyntaxError(Exception):
    pass


def tokenize_wrapper(input):
    """Tokenizes a string suppressing significant whitespace."""
    skip = {token.NEWLINE, token.INDENT, token.DEDENT}
    tokens = tokenize.generate_tokens(io.StringIO(input).readline)
    for quintuple in tokens:
        type, value, start, end, line_text = quintuple
        if type not in skip:
            yield quintuple


class PatternCompiler(object):

    def __init__(self, grammar_file=None):
        """Initializer.

        Takes an optional alternative filename for the pattern grammar.
        """
        if grammar_file is None:
            self.grammar = pygram.pattern_grammar
            self.sym_s = pygram.pattern_symbols
        else:
            self.grammar = driver.load_grammar(grammar_file)
            self.sym_s = pygram.Symbols(self.grammar)
        self.py_grammar = pygram.python_grammar
        self.py_sym_s = pygram.python_symbols
        self.driver = driver.Driver(self.grammar, convert=pattern_convert)

    def compile_pattern(self, _input, debug=False, with_tree=False):
        """Compiles a pattern string to a nested pytree.*Pattern object."""
        tokens = tokenize_wrapper(_input)
        try:
            root = self.driver.parse_tokens(tokens, debug=debug)
        except parse.ParseError as e:
            raise PatternSyntaxError(str(e)) from None
        if with_tree:
            return self.compile_node(root), root
        else:
            return self.compile_node(root)

    def compile_node(self, node):
        """Compiles a node, recursively.

        This is one big switch on the node type.
        """
        # XXX Optimize certain Wildcard-containing-Wildcard patterns
        # that can be merged
        if node._type == self.sym_s.Matcher:
            node = node.children[0]  # Avoid unneeded recursion

        if node._type == self.sym_s.Alternatives:
            # Skip the odd children since they are just '|' tokens
            alts = [self.compile_node(ch) for ch in node.children[::2]]
            if len(alts) == 1:
                return alts[0]
            p = pytree.WildcardPattern([[a] for a in alts], min=1, max=1)
            return p.optimize()

        if node._type == self.sym_s.Alternative:
            units = [self.compile_node(ch) for ch in node.children]
            if len(units) == 1:
                return units[0]
            p = pytree.WildcardPattern([units], min=1, max=1)
            return p.optimize()

        if node._type == self.sym_s.NegatedUnit:
            pattern = self.compile_basic(node.children[1:])
            p = pytree.NegatedPattern(pattern)
            return p.optimize()

        assert node._type == self.sym_s.Unit

        name = None
        nodes = node.children
        if len(nodes) >= 3 and nodes[1]._type == token.EQUAL:
            name = nodes[0].value
            nodes = nodes[2:]
        repeat = None
        if len(nodes) >= 2 and nodes[-1]._type == self.sym_s.Repeater:
            repeat = nodes[-1]
            nodes = nodes[:-1]

        # Now we've reduced it to: STRING | NAME [Details] | (...) | [...]
        pattern = self.compile_basic(nodes, repeat)

        if repeat is not None:
            assert repeat._type == self.sym_s.Repeater
            children = repeat.children
            child = children[0]
            if child._type == token.STAR:
                min = 0
                max = pytree.HUGE
            elif child._type == token.PLUS:
                min = 1
                max = pytree.HUGE
            elif child._type == token.LBRACE:
                assert children[-1].type == token.RBRACE
                assert len(children) in (3, 5)
                min = max = self.get_int(children[1])
                if len(children) == 5:
                    max = self.get_int(children[3])
            else:
                assert False
            if min != 1 or max != 1:
                pattern = pattern.optimize()
                pattern = pytree.WildcardPattern([[pattern]], min=min, max=max)

        if name is not None:
            pattern.name = name
        return pattern.optimize()

    def compile_basic(self, nodes, repeat=None):
        # Compile STRING | NAME [Details] | (...) | [...]
        assert len(nodes) >= 1
        node = nodes[0]
        if node._type == token.STRING:
            value = str(literals.evalString(node.value))
            return pytree.LeafPattern(_type_of_literal(value), value)
        elif node._type == token.NAME:
            value = node.value
            if value.isupper():
                if value not in TOKEN_MAP:
                    raise PatternSyntaxError("Invalid token: %r" % value)
                if nodes[1:]:
                    raise PatternSyntaxError("Can't have details for token")
                return pytree.LeafPattern(TOKEN_MAP[value])
            else:
                if value == "any":
                    _type = None
                elif not value.startswith("_"):
                    _type = getattr(self.py_sym_s, value, None)
                    if _type is None:
                        raise PatternSyntaxError("Invalid symbol: %r" % value)
                if nodes[1:]:  # Details present
                    content = [self.compile_node(nodes[1].children[1])]
                else:
                    content = None
                return pytree.NodePattern(_type=_type, content=content)
        elif node.value == "(":
            return self.compile_node(nodes[1])
        elif node.value == "[":
            assert repeat is None
            subpattern = self.compile_node(nodes[1])
            return pytree.WildcardPattern([[subpattern]], min=0, max=1)
        assert False, node

    def get_int(self, node):
        assert node._type == token.NUMBER
        return int(node.value)


# Map named tokens to the type value for a LeafPattern
TOKEN_MAP = {"NAME": token.NAME,
             "STRING": token.STRING,
             "NUMBER": token.NUMBER,
             "TOKEN": None}


def _type_of_literal(value):
    if value[0].isalpha():
        return token.NAME
    elif value in grammar.opmap:
        return grammar.opmap[value]
    else:
        return None


def pattern_convert(grammar, raw_node_info):
    """Converts raw node information to a Node or Leaf instance."""
    _type, value, context, children = raw_node_info
    if children or _type in grammar.number2symbol:
        return pytree.Node(_type, children, context=context)
    else:
        return pytree.Leaf(_type, value, context=context)


def compile_pattern(pattern):
    return PatternCompiler().compile_pattern(pattern)
