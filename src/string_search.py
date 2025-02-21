import tracemalloc
import time
import numpy as np
import random
import argparse
import matplotlib.pyplot as plt
import naive_search
import boyer_moore

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text_range',
                        type=int,
                        required=True,
                        nargs=3,
                        help='Text size parameters (start stop step) -- all same value for constant text size')
    parser.add_argument('--pattern_range',
                        type=int,
                        required=True,
                        nargs = 3,
                        help='Pattern size parameters (start stop step) -- all same value for constant pattern size')
    parser.add_argument('--rounds',
                        type=int,
                        default=10,
                        help='Number of rounds to run each algorithm ' \
                             + '(default: 10)')
    parser.add_argument('--out_file',
                        type=str,
                        required=True,
                        help='File to save plot to')
    parser.add_argument('--width',
                        type=float,
                        default=8,
                        help='Width of plot in inches (default: 8)')
    parser.add_argument('--height',
                        type=float,
                        default=5,
                        help='Height of plot in inches (default: 5)')
    return parser.parse_args()

def get_random_string(alphabet, length):
    return ''.join(random.choice(alphabet) for i in range(length))

def get_random_substring(string, length):
    if length > len(string):
        raise ValueError("Length of substring is longer than the string.")

    start_index = random.randint(0, len(string) - length)
    return string[start_index:start_index + length]

def run_test(test_function, T, P):
    start = time.monotonic_ns()
    r = test_function(T, P)
    stop = time.monotonic_ns()

    tracemalloc.start()
    r = test_function(T, P)
    mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return stop - start, mem[1] - mem[0]

def test_harness(test_functions,
                 text_range,
                 pattern_range,
                 rounds):

    run_times = [ [] for _ in range(len(test_functions))]
    mem_usages = [ [] for _ in range(len(test_functions))]

    if pattern_range[0] == pattern_range[1]:
        pattern_size = pattern_range[0]

        for text_size in range(text_range[0], text_range[1], text_range[2]):

            _run_times = [ [] for _ in range(len(test_functions))]
            _mem_usages = [ [] for _ in range(len(test_functions))]

            for i in range(rounds):
                T = get_random_string(['A', 'C', 'T', 'G'], text_size)
                P = get_random_substring(T, pattern_size)

                for j, test_function in enumerate(test_functions):
                    run_time, mem_usage = run_test(test_function, T, P)
                    _run_times[j].append(run_time)
                    _mem_usages[j].append(mem_usage)

            for j, test_function in enumerate(test_functions):
                run_times[j].append(np.mean(_run_times[j]))
                mem_usages[j].append(np.mean(_mem_usages[j]))

    else:
        text_size = text_range[0]
        
        for pattern_size in range(pattern_range[0], pattern_range[1], pattern_range[2]):

            _run_times = [ [] for _ in range(len(test_functions))]
            _mem_usages = [ [] for _ in range(len(test_functions))]

            for i in range(rounds):
                T = get_random_string(['A', 'C', 'T', 'G'], text_size)
                P = get_random_substring(T, pattern_size)

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

    run_times, mem_usages = test_harness(test_functions,
                                        args.text_range,
                                        args.pattern_range,
                                        args.rounds)


    fig, axs = plt.subplots(2,1, figsize=(args.width, args.height))

    text_size_range =  range(args.text_range[0],
                             args.text_range[1],
                             args.text_range[2])

    pattern_size_range =  range(args.pattern_range[0],
                             args.pattern_range[1],
                             args.pattern_range[2])

    fig.tight_layout(pad=3.0)
    ax = axs[0]
    
    if args.pattern_range[0] == args.pattern_range[1]:
        ax.plot(text_size_range, run_times[0], label='Naive')
        ax.plot(text_size_range, run_times[1], label='Boyer-Moore')
        ax.set_title(f'String Search Performance(|P|= {args.pattern_range[0]})')
        ax.set_xlabel('Text size')
    else:
        ax.plot(pattern_size_range, run_times[0], label='Naive')
        ax.plot(pattern_size_range, run_times[1], label='Boyer-Moore')
        ax.set_title(f'String Search Performance(|T|= {args.text_range[0]})')
        ax.set_xlabel('Pattern size')
    ax.set_ylabel('Run time (ns)')
    ax.legend(loc='best', frameon=False, ncol=3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax = axs[1]
    if args.pattern_range[0] == args.pattern_range[1]:
        ax.plot(text_size_range, mem_usages[0], label='Naive')
        ax.plot(text_size_range, mem_usages[1], label='Boyer-Moore')
        ax.set_xlabel('Text size')
    else:
        ax.plot(pattern_size_range, mem_usages[0], label='Naive')
        ax.plot(pattern_size_range, mem_usages[1], label='Boyer-Moore')
        ax.set_xlabel('Pattern size')
    ax.set_ylabel('Memory (bytes)')
    ax.legend(loc='best', frameon=False, ncol=3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()

    plt.savefig(args.out_file)

if __name__ == '__main__':
    main()
