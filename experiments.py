import multiprocessing
from multiprocessing import Process, Manager, Value
import sys, os, tempfile
from time import time, sleep
from itertools import product

# host process __abort should be always equal to 0
__abort = 0

def __start_process(args):
    global __abort
    if __abort:
        return "", "", []
    try:
        results = []
        
        func, iterations, kwargs = args
        if callable(iterations):
            iterations = iterations(**kwargs)
        
        stdout = sys.stdout
        sys.stdout = tempfile.TemporaryFile()
        sys.stderr = tempfile.TemporaryFile()
        for i in xrange(iterations):
            t = time()
            result = func(**kwargs)
            t = time() - t
            results.append({'args': dict(kwargs), 'result': result, 'time': t})
    except KeyboardInterrupt:
        __abort = 1
    finally:
        # acquiring output
        sys.stdout.flush()
        sys.stdout.seek(0)
        log = sys.stdout.read()
        # acquiring error log
        sys.stderr.flush()
        sys.stderr.seek(0)
        err = sys.stderr.read()
        return log, err, results

def start(func, iterations=10, cores=1, **kwargs):
    # creating an array of all necessary kwargs configurations
    calls = None
    for argname in kwargs:
        argvalue = kwargs[argname]
        if isinstance(argvalue, list):
            if calls is None:
                calls = [{argname: val} for val in argvalue]
            else:
                calls = [dict(call, **{argname: val}) for call, val in product(calls, argvalue)]
        else:
            if calls is None:
                calls = [{argname: argvalue}]
            else:
                calls = [dict(call, **{argname: argvalue}) for call in calls]
    
    pool = multiprocessing.Pool(processes=cores)
    calls = [(func, iterations, call) for call in calls]
    try:
        data = pool.map_async(__start_process, calls)
        while not data.ready():
            sleep(0.1)
        data = data.get()
        pool.close()
    except KeyboardInterrupt:
        if not isinstance(data, list):
            sys.stderr.write("Keyboard interrupt. Further computations aborted.\n")
            sys.stderr.write("Hit Ctrl+C again to abort all computations.\n")
            try:
                while not data.ready():
                    sleep(0.1)
                data = data.get()
                pool.close()
            except KeyboardInterrupt:
                pool.terminate()
                if not isinstance(data, list):
                    sys.stderr.write("Keyboard interrupt. All computations aborted. No results will be returned.\n")
                    data = None
                else:
                    sys.stderr.write("Keyboard interrupt. All computations aborted.\n")
        else:
            sys.stderr.write("Keyboard interrupt. All computations aborted.\n")
    pool.join()
    if data:
        #print "Computations done."
        results = [results for log, err, results in data if len(results) > 0]
        log = "\n".join([log for log, err,results in data])
        err = "\n".join([err for log, err,results in data])
        #print [results for log, err, results in data]
        return log, err, results
    
