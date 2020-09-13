import multiprocessing as mpi


def run(a):
    print(a.get())

if __name__ == '__main__':
    queue=mpi.Queue()
    for i in range(10):
        queue.put(i)
    for i in range(5):
        p = mpi.Process(target=run, args=(queue,))
        p.start()
        p.join()
    print(queue.get())