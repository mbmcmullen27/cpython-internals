import multiprocessing as mp

def to_celsius(child_pipe: mp.Pipe):
  f = child_pipe.recv()
  c = (f-32) * (5/9)
  child_pipe.send(c)

if __name__ == '__main__':
  mp.set_start_method('spawn')
  pool_manager = mp.Manager()
  with mp.Pool(2) as pool:
      parent_pipe, child_pipe = mp.Pipe()
      results = []
      for input in range(110, 150, 10):
        parent_pipe.send(input)
        results.append(pool.apply_async(to_celsius, args=(child_pipe,)))
        print("Got {0:}".format(parent_pipe.recv()))
      parent_pipe.close()
      child_pipe.close()
      