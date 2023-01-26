# change 'pass' keyword in small_stmt grammar 
# to ('pass' | 'proceed') and recompile

# ./python -m tokenize -e ../examples/test_tokens.py

# Demo application
def my_function():
  proceed