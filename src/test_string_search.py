import tracemalloc
import time
import numpy as np
import random
import argparse
import matplotlib.pyplot as plt
import unittest
import string_search
import naive_search
import boyer_moore

class TestStringSearch(unittest.TestCase):
    def test_string_search(self):
        self.assertEqual(boyer_moore.boyer_moore_search('abc', 'abc'), [0])
        self.assertEqual(boyer_moore.boyer_moore_search('abcabc', 'abc'), [0,3])
        self.assertEqual(boyer_moore.boyer_moore_search('abc', 'bc'), [1])
        self.assertEqual(boyer_moore.boyer_moore_search('abc', 'c'), [2])
        self.assertEqual(boyer_moore.boyer_moore_search('abc', 'x'), [])

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text',
                        type=str,
                        required=True,
                        help='Reference text string')
    parser.add_argument('--pattern',
                        type=str,
                        required=True,
                        help='Pattern string to be searched for')
    parser.add_argument('--rounds',
                        type=int,
                        default=10,
                        help='Number of rounds to run each algorithm ' \
                             + '(default: 10)')
    return parser.parse_args()

def run_test(test_function, T, P):
    start = time.monotonic_ns()
    r = test_function(T, P)
    stop = time.monotonic_ns()

    tracemalloc.start()
    r = test_function(T, P)
    mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return stop - start, mem[1] - mem[0]

def test_harness(test_functions, text, pattern, rounds):
    run_times = [ [] for _ in range(len(test_functions))]
    mem_usages = [ [] for _ in range(len(test_functions))]

    _run_times = [ [] for _ in range(len(test_functions))]
    _mem_usages = [ [] for _ in range(len(test_functions))]

    for i in range(rounds):
        T = text
        P = pattern

        for j, test_function in enumerate(test_functions):
            run_time, mem_usage = run_test(test_function, T, P)
            _run_times[j].append(run_time)
            _mem_usages[j].append(mem_usage)

    for j, test_function in enumerate(test_functions):
        run_times[j].append(np.mean(_run_times[j]))
        mem_usages[j].append(np.mean(_mem_usages[j]))

    return run_times, mem_usages

def main():
    args = get_args()

    test_functions = [naive_search.naive_search, boyer_moore.boyer_moore_search]

    func_names = ["Naive Search", "Boyer-Moore"]

    run_times, mem_usages = test_harness(test_functions,
                                        args.text,
                                        args.pattern,
                                        args.rounds)

    for i in range(len(func_names)):
        print(func_names[i], "average runtime:", run_times[i])
        print(func_names[i], "average memory usage:", mem_usages[i])



if __name__ == '__main__':
    # unittest.main()
    main()
