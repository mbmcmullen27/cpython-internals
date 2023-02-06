from symtable import SymbolTable
import token
import ast
from pprint import pprint

def lex(expression):
    symbols = {v: k for k, v in SymbolTable.__dict__.items()
               if isinstance(v,int)}
    tokens = {v: k for k, v in token.__dict__.items()
              if isinstance(v, int)}
    lexicon = {**symbols, **tokens}
    st_list = ast.Expr(expression).value
    # st_list = parser.st2list(st)
    pprint(st_list)
    pprint(symbols)
    pprint(SymbolTable)

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