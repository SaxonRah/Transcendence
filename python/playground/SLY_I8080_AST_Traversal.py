from SLY_I8080 import *

# TODO: create functions that use TODO lexer / parser functions from SLY_I8080
# TODO: use the real AST created from SLY AST LIST and labels, macros, and directive dictionaries
abstract_syntax_tree = []


# TODO: traverse label, macros, directives dictionaries
# simple recursive traversal with comma removal example
def traverse_ast(in_abstract_syntax_tree):
    if isinstance(in_abstract_syntax_tree, list):
        for item in in_abstract_syntax_tree:
            # print(item)
            traverse_ast(item)

    elif isinstance(in_abstract_syntax_tree, tuple):
        for node in in_abstract_syntax_tree:
            if isinstance(node, tuple):
                traverse_ast(node)
            else:
                if node != ',':
                    abstract_syntax_tree.append(node)
                # print(node)
    else:
        ...


def test_traverse_ast():
    ast = ['DB', (((((((((('0', ',', '78H'),
                          ',', '80H'),
                         ',', '84H'),
                        ',', '88H'),
                       ',', '8AH'),
                      ',', '8CH'),
                     ',', '8EH'),
                    ',', '90H'),
                   ',', '91H'),
                  ',', '92H')]
    traverse_ast(ast)
    print(abstract_syntax_tree)


if __name__ == "__main__":
    test_traverse_ast()
