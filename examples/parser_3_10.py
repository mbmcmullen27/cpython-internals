from symtable import SymbolTable
import token
import ast
from pprint import pprint

def lex(expression):
    # symbols = {v: k for k, v in SymbolTable.get_symbols()
    #            if isinstance(v,int)}
    tokens = token.__dict__.items()
            # {v: k for k, v in token.__dict__.items()}
            #   if isinstance(v, int)}
    # lexicon = {**symbols, **tokens}
    for i in tokens:
        pprint(i)
        pprint('\n')
    st_list = ast.Expr(expression)
    # st_list = parser.st2list(st)
    # pprint(st_list)
    # pprint(symbols)
    # pprint(tokens)
    table = SymbolTable(st_list)
    pprint(table.get_symbols())

    def replace(l: list):
        r = []
        for i in l:
            if isinstance(i, list):
                r.append(replace(i))
            else:
                if i in lexicon:
                    r.append(lexicon[i])
                else:
                    r.append(i)
        return r
    
    return replace(st_list)

lex("a+1")