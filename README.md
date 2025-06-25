# Summary
Hi Josh! I've put a few notes here just to explain how to use my implementation in the interest of making it as easy as possible for you to evaluate.

# Q1

## Total Time Weighted Return Calculator

To run the calculator:

```bash
python q1/main.py q1/test_data/sample_valuations.csv
```

As well as returning the pd.Series, the first and last 5 rows of the Series are printed to the terminal, i.e:

``` bash
2017-11-08    0.000000
2017-11-09    0.000000
2017-11-10    0.000000
2017-11-13    0.000000
2017-11-14    0.000000
                ...   
2018-01-30    0.014496
2018-01-31    0.010485
2018-02-01    0.006227
2018-02-02    0.001768
2018-02-05   -0.006563
Name: time_weighted_return, Length: 64, dtype: float64
```


## Unit tests

- `pytest q1` runs all unit and performance tests in the `q1/` folder.  
  - `test_utils.py`: file I/O and parsing validation  
  - `test_twr.py`: correctness on core and edge TWR cases  
  - `test_perf.py`: demonstrates a simple scalability performance test (1,000 vs 10,000 rows) to show that the TWR algorithm remains O(n)