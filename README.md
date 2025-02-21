[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/08twE9R9)
# string_search
Empirical comparison of string search methods.

## Usage
```
usage: string_search.py [-h] --text_range TEXT_RANGE TEXT_RANGE TEXT_RANGE
                        --pattern_range PATTERN_RANGE PATTERN_RANGE PATTERN_RANGE
                        [--rounds ROUNDS] --out_file OUT_FILE
                        [--width WIDTH] [--height HEIGHT]

optional arguments:
  -h, --help            show this help message and exit
  --text_range TEXT_RANGE TEXT_RANGE TEXT_RANGE
                        Text size parameters (start stop step) -- all same value for constant text size
  --pattern_range PATTERN_RANGE PATTERN_RANGE PATTERN_RANGE 
                        Pattern size parameters (start stop step) -- all same value for constant text size
  --rounds ROUNDS       Number of rounds to run each algorithm (default: 10)
  --out_file OUT_FILE   File to save plot to
  --width WIDTH         Width of plot in inches (default: 8)
  --height HEIGHT       Height of plot in inches (default: 5)
```

## Examples
```
python src/string_search.py \
    --text_range 1000 10000 100 \
    --pattern_range 1000 1000 1000 \
    --rounds 1 \
    --out_file doc/t-range_p-1000.png
```
<center><img src="/doc/t-range_p-1000.png" width="600"/></center>

# test_string_search
Comparison of string search methods for the worst case scenario

## Usage
```
usage: test_string_search.py [-h] --text TEXT --pattern PATTERN
                                  [--rounds ROUNDS]

optional arguments:
  -h, --help            show this help message and exit
  --text TEXT           Reference text string
  --pattern             Pattern to be searched for
  --rounds ROUNDS       Number of rounds to run each algorithm (default: 10)
```

## Examples
```
python src/test_string_search.py \
    --text 'AAAAAAAAAAAAAAAAAAAA' \
    --pattern 'AA' \
    --rounds 10 
```
# Output:
```
Naive Search average runtime: [6610.3]
Naive Search average memory usage: [144.0]
Boyer-Moore average runtime: [10306.9]
Boyer-Moore average memory usage: [0.0]
```


