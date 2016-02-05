import threading as th
import multiprocessing as mp
import time

from utils.csvdata import get_available_symbols


class BaseEvaluator(object):

    def __init__(self, start_date, end_date, symbols=None):
        """

        Parameters
        -----------
        start_date: string
        end_date: string
        symbols: list
            The symbols to evaluate.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.thread_number = mp.cpu_count()
        if symbols is None:
            self.symbols = get_available_symbols()
        else:
            self.symbols = symbols
        self.results = []
        self.report = "Not generated."
        self.thread_lock = th.Lock()

    def start(self):
        threads = []
        avg = len(self.symbols) / self.thread_number
        index = 0
        print "Start to evaluate {} symbols with {} threads.".format(len(self.symbols), self.thread_number)

        # Create threads and split the task to threads
        for i in range(self.thread_number):
            thread = WorkerThread("thread-{}".format(i), self.symbols[index: index + avg], self)
            thread.start()
            threads.append(thread)
            index += avg

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # Generate evaluation report
        self.generate_report()


    def evaluate(self, symbol):
        result = self.real_evaluate(symbol)

        self.thread_lock.acquire()
        if result is not None:
            self.results.append(result)
        self.thread_lock.release()


    def real_evaluate(self, symbol):
        """
        This method does the real evaluation job. It must be thread safe.
        """
        raise NotImplementedError


    def generate_report(self):
        raise NotImplementedError


    def dump_report(self):
        print self.report

class WorkerThread(th.Thread):

    def __init__(self, name, symbols, evaluator):
        th.Thread.__init__(self)
        self.name = name
        self.symbols = symbols
        self.evaluator = evaluator


    def run(self):
        for symbol in self.symbols:
            self.evaluator.evaluate(symbol)
            time.sleep(0.1)