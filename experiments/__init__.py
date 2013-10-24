import multiprocessing
from multiprocessing import Pool
import sys, os, tempfile
from time import time, sleep
from itertools import product

# host process __abort should be always equal to 0
__abort = 0


def average(l):
    return sum(l) / float(len(l))


class ExperimentalData(list):
  def __init__(self, raw, result_selection_func = lambda x: x[0]):
    self.raw = raw
    __h = lambda args: frozenset(args.items())
    
    by_arg = {}
    for item in raw:
	args = item['args']
	time = item['time']
	result = item['result']
	args = __h(args)
	if args not in by_arg:
	  by_arg[args] = []
	by_arg[args].append((time, result))
    
    averaged = []
    for a, data in by_arg.iteritems():
	times, results = zip(*data)
	averaged.append({
	    'args'  : dict(a),
	    'result': result_selection_func(results),
	    'time'  : average(times),
	})
    
    super(ExperimentalData, self).__init__(averaged)

def __start_process(args):
    global __abort
    if __abort:
        return []
    try:
        results = []
        
        func, iterations, kwargs = args
        if callable(iterations):
            iterations = iterations(**kwargs)
        
        for i in xrange(iterations):
            t = time()
            result = func(**kwargs)
            t = time() - t
            results.append({'args': dict(kwargs), 'result': result, 'time': t})
    except KeyboardInterrupt:
        __abort = 1
    finally:
	return results

def start(func, iterations=10, cores=1, **kwargs):
    global __abort
    __abort = 0
    # creating an array of all necessary kwargs configurations
    calls = None
    for argname, argvalue in kwargs.items():
        if isinstance(argvalue, (list, tuple)):
            if calls is None:
                calls = [{argname: val} for val in argvalue]
            else:
                calls = [dict(call, **{argname: val}) for call, val in product(calls, argvalue)]
        else:
            if calls is None:
                calls = [{argname: argvalue}]
            else:
                calls = [dict(call, **{argname: argvalue}) for call in calls]
    pool = Pool(cores)
    calls = [(func, iterations, call) for call in calls]
    try:
        data = pool.map_async(__start_process, calls)
        while not data.ready():
            sleep(0.1)
        data = data.get()
        pool.close()
        #data = pool.map(__start_process, calls) # ignores my smart Ctrl+C handling
        #pool.close()
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
        results = reduce(lambda x, y: x + y, data)
        #results = [results for log, err, results in data if len(results) > 0]
        #log = "\n".join([log for log, err,results in data])
        #err = "\n".join([err for log, err,results in data])
        #print [results for log, err, results in data]
        return ExperimentalData(results)
    
