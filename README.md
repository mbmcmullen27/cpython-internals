# cpython internals
- this book targets version 3.9<sup>a</sup> of the CPython source code.
    - <sup>a</sup> https://github.com/python/cpython/tree/3.9
- code samples 
  - [realpython.com](https://realpython.com/cpython-internals/resources)
  - [book samples](https://github.com/tonybaloney/cpython-book-samples)

## Compiling CPython
- (61) The \[...\] build processes have flags for **profile-guilded optimization (PGO)**. PGO isn't something created by the Python team, but a feature of many compilers
- (61) PGO works by doing an initial compilation, then profiling the application by running a series of tests. The profile is then analyzed, and the compiler makes changes to the binary that improve performance.
- (62) \[When compiling\] profile-guided optimizations include these checks and improvements:
  - **Function inlining:** \[...\]
  - **Virtual call speculation and inlining:** If a virtual function call frequently targets a certain function, then PGO can insert a conditionally executed direct call to that function. The direct call can then be inlined
  - **Register allocation optimization:** Based on profile data results the PGO will optimize register allocation.
  - **Basic block optimization:** Basic block opitimization allows commonly execued basic blocks that temporally execute within a givin frame to be placed in the same **locality**, or set of pages . It minimizes the number of pages used, which minimizes memory overhead.
  - **Hot spot optimization:** Functions that the program spends the most execution time on can be optimized for speed.
  - **Function layout optimization:** After PGO analyzes the call graph, functions that tend to be along the same execution path are moved to the same section of the compiled application.
  - **Conditional branch optimization:** PGO can look at a decision branch, like an if ... else if or switch statement, and spot the most commonly used path. For example, if there are ten cases in a switch statement, and one is used 95 percent of the time, then that case will be moved to the top so that it will be executed immediately in the code path.
  - **Dead spot separation:** Code that isn't called during PGO is moved to a separate section of the application. 

## The Python Language and Grammar
- the cpython interpreter compiles source code and caches it in .pyc files on the first execution
  - (66) If you run the same Python application twice without changing the source code, then it will be faster on the second execution

- (66) **Self-hosted compilers** are compilers written in the language they compile, such as the Go compiler. This is done by a process known as **bootstrapping**
- (66) **Source-to-source compilers** are compilers written in another language that already has a compiler.
- (67) If you want to learn more about parsers, then check out the [Lark](https://github.com/lark-parser/lark) project

**[Python reference guide](https://docs.python.org/3/reference)**

**['with' statement/context managers](https://dbader.org/blog/python-context-managers-and-with-statement)**

- while statements in python can have an else block
  ```python
  while item := next(iterable)
    print(item)
  else
    print("iterable is empty")
  ```

- when changing the [grammar](./cpython/Grammar/python.gram) regenerate grammar files with `make regen-pegen` and recompile

- (78) To see a verbose readout of the C parser, you can run a debug build of Python with the -d flag
  ```sh
  ./python -d ../examples/test_tokens.py
  ```

## Configuration and Input
- you can run a python script by piping python code to the python executable
  ```sh
  cat <file> | python
  ```

### Configuration
- `./python cpython/Tools/scripts/smelly.py` 
  - used to check compliance with PEP 7
- [initconfig.h](cpython/Include/cpython/initconfig.h)
  - defines preinitialization & runtime configuration structures
- `./python -m sysconfig`
  - view build configuration

### Input
- (89) there are 4 main files that deal with the command-line interface
  - [Lib/runpy.py](cpython/Lib/runpy.py)
    - Standard library module for importing Python modules and executing them
  - [Modules/main.c](cpython/Moduels/main.c)
    - Functions wrapping the execution of external code, such as from a file, module or input stream
  - [Programs/python.c](cpython/Programs/python.c)
    - The entry point for the python executable for Windows, Linux, and macOS. Serves only as a wrapper for Modules/main.c
  - [Python/pythonrun.c](cpython/Python/pythonrun.c)
    - Functions wrapping the internal C APPIs for processing inputs from the command line

- (90) Once CPython has the runtime configuration adn the command-line arguments, it can load the code it needs to execute. This task is handlled by pymain_main() inside [Modules/main.c](cpython/Modules/main.c)

- Python input can be given 4 ways
  1. input from command line
  1. input from a local module
      - `python -m <module>` is equivalent to `python -m runpy <module>`
      - `runpy` module also supports executing directories and ZIP files
  1. input from a script file or standar input
  1. input from compiled bytecode

## Lexing and Parsing with Syntax Trees

- (96) There are two structures used to parse code in CPython, the **concrete syntax tree (CST)** and the **abstract syntax tree (AST)**

- (100) parser-tokenizer source files
  - [Python/pythonrun.c](cpython/Python/pythonrun.c)
    - Executes the parser and the compiler from an input
  - [Parser/parsetok.c](cpython/Parser/parsetok.c)
    - The parser and tokenizer implementation
  - [Parser/tokenizer.c](cpython/Parser/tokenizer.c)
    - Tokenizer implementation
  - [Parser/tokenizer.h](cpython/Parser/tokenizer.h)
    - Header file for the tokenizer implementation that describes data models like token state
  - [Include/token.h](cpython/Include/token.h)
    - Declaration of token types, generated by [Tools/scripts/generate_token.py](cpython/Tools/scripts/generate_token.py)
  - [Include/node.h](cpython/Include/node.h)
    - Parse tree node interface and macros for the tokenizer

- (103) CPython has a standard library module, _parser_, which exposes the C functions with a Python API.
  ```python
  from pprint import pprint
  import parser
  st = parser.expr('a + 1')
  pprint(parser.st2list(st))
  ```
  - **NOTE** Python 3.9 deprecated the symbol and parser modules and 3.10 removed them
    - [PEP 617](https://peps.python.org/pep-0617/)
    - [bugs.python.org - 40759](https://bugs.python.org/issue40759)
    - breaks [parser module example](examples/parser_lexer.py)
    - parser replaced by [ast module](https://docs.python.org/3.10/library/ast.html?highlight=parser#ast.parse)
    - ~~Symbol replaced with SymbolTable~~
      - Symbol held a list of possible tokens symtable implements a list of declared identifiers from an AST
      - blog about symtable
        - [part 1](https://eli.thegreenplace.net/2010/09/18/python-internals-symbol-tables-part-1/)
        - [part 2](https://eli.thegreenplace.net/2010/09/20/python-internals-symbol-tables-part-2/)

      - [symtable definition](./cpython/Python/symtable.c)
      - The compiler builds a symbol table from the AST representing the Python source code
      - The symbol table is responsible for calculating the scope of every identifier in the code
      - An entry object is created for each block in the Python source code
**NOTE** list comprehension syntax:
  ```newlist = [expression for item in iterable if condition == True]```

- use `instaviz` module for a detailed view of the AST
  ```python
  import instaviz
  def example():
    a = 1
    b = a + 1
    return b

  instaviz.show(example)
  ```

- adding an operator (Almost Equal)
  1. add new rule to [grammar](./cpython/Grammar/python.gram)
      ```
      compare_op_bitwise_or_par[CmpopExprPair*]:
        | eq_bitwise_or
        ...
        | ale_bitwsie_or
      ```
  1. define the new ale_bitwise_or expression
      ```
      is_bitwise_or[CmpopExprPair*]: 'is' a=bitwise_or { _PyPegen_cmpop_expr_pair(p, Is, a) }
      ale_bitwise_or[CmpopExprPair*]: '~=' a=bitwsie_or { _PyPegen_cmpop_expr_pair(p, ALE, a)}
      ```
  1. add the token to [tokens](./cpython/Grammar/Tokens)
      ```
      ALMOSTEQUAL             '~='
      ```
  1. regenerate headers
      ```sh
      make regen-token regen-pegen
      ```
      - this will automatically update the [tokenizer](./cpython/Parser/token.c)
  1. Add `AlE` to the list of possible leaf nodes for a comparison expression defined in [Parser](./cpython/Parser/Python.asdl)
      ```
      cmpop = Eq | NotEq | Lt | LtE | Gt | GtE | Is | IsNot | In | NotIn | AlE
      ```
  1. regenerate AST
      ```sh
      make regen-ast
      ```
  1. add ALMOSTEQUAL to the switch statement matching tokens in [ast.c](./cpython/Python/ast.c)
      ```c
      ast_for_comp_op(struct compiling *c, const node *n) {
        // ...
        switch(TYPE(n)) {
          // ...
          case ALMOSTEQUAL:
            return AlE;
        }
      }

      ```

## The Compiler
- (124) PyAST_CompileObject() is the main entry point to teh CPython compiler
- future flags:
  - `barry_as_FLUFL` "includes easter egg" [PEP401](https://peps.python.org/pep-0401/)
- (136) You can call the compiler in Python by calling the build-in function `compile()`
    ```python
    co = compile("b+1", "test.py", mode="eval")
    ```
  - a simple expression should have a mode of "eval", and a module, funciton or class should have a mode of "exec"
- (136) The standard library also includes a `dis` module, which disassembles the bytecode instructions
    ```python
    import dis
    dis.dis(co.co_code)
    ```
  - (137) if you import `dis` and give `dis()` the code object's `co_code` property, then the function disassembles it and prints the instructions on the REPL
**LINK** [list of bytecode instructions](https://docs.python.org/3/library/dis.html#python-bytecode-instructions)
  - [opcode definitions](./cpython/Include/opcode.h)

- (148) You can pull together all the compiler statges with the `instaviz` module:
  ```python
  import instaviz

  def foo():
    a = 2**4
    b = 1 + 5
    c = [1, 4, 6]
    for i in c:
      print(i)
    else:
      print(a)
    return c

  instaviz.show(foo)
  ```
  - instaviz proving to be an important tool for python debugging

- (150-156) Implementing the almost equal operator
  - define a new opcode in [object.h](./cpython/Include/object.h)
  - add update COMPARE_OP opcode to support Py_AlE as a value for an operator type
    - [object.c](./cpython/Objects/object.c) 
      - add Py_AlE to the _Py_SwappedOp list
      - add `~=` to opstrings list
    - [opcode.py](./cpython/Lib/opcode.py)
      - add `~=` to list of rich comparison operators `cmp_op`
  - update the compiler to handle PyCmp_AlE property in a BinOp node
    - [compile.c](./cpython/Python/compile.c)
      - find `compiler_addcompare()` and add a case for AlE
    - update `float_richcompare()` in [floatobject.c](./cpython/Objects/floatobject.c)
  - update evaluation loop
    - [ceval.c](./cpython/Python/ceval.c)
      - update assertion in TARGET case `assert(oparg <= Py_AlE);`

## The Evauluation Loop
- (157) Execution of code in CPython happens within a central loop called the __Evaluation Loop__
  - takes input in the form of local and global variables stored in the __value stack__
  - bytecode instructions are executed using a stack frame system

this is all starting to sound very familiar

- (158) the evaluation loop will take a code object and convert it into a series of frame objects
- (159) CPython can have many threads running at any one time within a single interpreter. The __interpreter state__ includes a linked list of those threads
- (162) In Python, local and global variables are stored as a dictionary. You can access this dictionary with the built-in functions locals() and globals():
    ```python
    a = 1
    print(locals()["a"])
    ```

- ["this is gonna sound real weird"](./cpython/Python/ceval.c#L4071)

- **NOTE:** Python has variable argument definitions for functions using the unpacking operator `*` for positional arguments, and `**` for named arguments
  - `*args`
    ```python
    def example(arg, *args):
      print(arg, args[0], args[1])

    example(1, 2, 3) # 1 2 3
    ```
  - `**kwargs`
    ```python
    def example(arg, arg2=None, **kwargs):
      print(kwargs["x"], kwargs["y"])

    example(1, x=2, y=3) # 2 3
    ```
- **NOTE:** You can use positional-only arguments to stop users from using positional arguments with keyword syntax by using the special argument `/` that separates positional-onlky arguments from other arguments
  ```python
  def to_celsius(fahrenheit, /, options=None):
    return (fahrenheit-32)*5/9

  to_celsius(110) # acceptable

  to_celsius(fahrenheit=110) # will raise a TypeError
  ```

(173-176) did we really need 4 pages to describe how a stack works?
- (178) a call to `PREDICT` is made, which guesses that the next operation witll be `JUMP_ABSOLUTE`.
  - how does that work? and what's the point of 'guessing?'

## Memory Management
- (185) "The `const` value `five_ninths` is allocated statically because it has the `static` keyword"
  - I think this is wrong. I'm pretty sure the static keyword is about scope and doesn't actually have anything to do with memory management in c
