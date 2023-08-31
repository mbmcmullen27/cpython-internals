import multiprocessing as mp

def to_celsius(child_pipe: mp.Pipe, child_lock: mp.Lock):
  child_lock.acquire(blocking=False)
  try:
    f = child_pipe.recv()
  finally:
    child_lock.release()
  
  c = (f-32) * (5/9)
  
  child_lock.acquire(blocking=False)
  try:
    child_pipe.send(c)
  finally:
    child_lock.release()

if __name__ == '__main__':
  mp.set_start_method('spawn')
  pool_manager = mp.Manager()
  with mp.Pool(2) as pool:
      parent_pipe, child_pipe = mp.Pipe()
      child_lock = pool_manager.Lock()
      results = []
      for input in range(110, 150, 10):
        parent_pipe.send(input)
        results.append(pool.apply_async(
          to_celsius, args=(child_pipe, child_lock)))
        print(parent_pipe.recv())
      parent_pipe.close()
      child_pipe.close()
      