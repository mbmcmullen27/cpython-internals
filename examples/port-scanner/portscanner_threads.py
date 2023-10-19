from threading import Thread
from queue import Queue
import time
import socket

timeout = 1.0

def check_port(host: str, port: int, results: Queue):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(timeout)
  result = sock.connect_ex((host, port))
  if result == 0:
    results.put(port)
  sock.close()

if __name__ == '__main__':
  start = time.time()
  host = "localhost" # Replace with a host you own
  threads = []
  results = Queue()
  for port in range(80,100):
    t = Thread(target=check_port,args=(host, port, results))
    t.start()
    threads.append(t)
  for t in threads:
    t.join()
  while not results.empty():
    print("Port {0} is open".format(outputs.get()))
  print("Completed scan in {0} seconds".format(time.time() - start))
