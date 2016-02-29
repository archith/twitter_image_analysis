import multiprocessing
import time

def func(n):
    for i in range(10000):
        for j in range(10000):
            s=j*i
    #print(n)

def worker(n):
    """worker function"""
    print 'Worker' + str(n)

    for i in range(10000):
        for j in range(10000):
            s=j*i
    return s

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()

    for i, p in enumerate(jobs):
        p.join()
        print ('Job %d done!!' % i)



# if __name__ == '__main__':
    # t1 = time.time()
    # pool = multiprocessing.Pool(processes=10)
    # pool.map(func, range(10))
    # pool.close()
    # pool.join()
    # print('MultiProc done')
    # t2 = time.time()
    # print('Multi Proc Processing time : ' + str(t2-t1))
    #
    # t1 = time.time()
    # for n in range(10):
    #    func(n)
    # t2 = time.time()
    # print('SingleProc done')
    # print('Single Proc Processing time : ' + str(t2-t1))



