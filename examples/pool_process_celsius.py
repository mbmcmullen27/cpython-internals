import multiprocessing as mp
import os

def to_celsius(f):
  c = (f-32) * (5/9)
  pid = os.getpid()
  print(f"{f}F is {c}C (pid {pid})")

if __name__ == '__main__':
  mp.set_start_method('spawn')
  # with mp.Pool(4) as pool:
  with mp.Pool(4, maxtasksperchild=1) as pool:
    pool.map(to_celsius, range(110, 150, 10))
