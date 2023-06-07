import tracemalloc

tracemalloc.start()

def to_celsius(farenheit, /, options=None):
  return (farenheit-32)*5/9

values = range(0, 100, 10) # values 0, 10, 20, ... 90

for v in values:
  c = to_celsius(v)

after = tracemalloc.take_snapshot()

tracemalloc.stop()
after = after.filter_traces([tracemalloc.Filter(True, '**/trace_demo.py')])
stats = after.statistics('lineno')

for stat in stats:
  print(stat)

# python -X tracemalloc=2 trace_demo.py