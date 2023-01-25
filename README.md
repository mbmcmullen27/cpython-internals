# cpython internals
- this book targets version 3.9<sup>a</sup> of the CPython source code.
    - <sup>a</sup> https://github.com/python/cpython/tree/3.9
- code samples [realpython.com](realpython.com/cpython-internals/resources)

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
**[with statement/context managers](https://dbader.org/blog/python-context-managers-and-with-statement)

- while statements in python can have an else block
  ```python
  while item := next(iterable)
    print(item)
  else
    print("iterable is empty")
  ```