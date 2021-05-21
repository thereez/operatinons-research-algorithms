# 0-1 Knapsack Problem

## Results


|Benchmark        | Execution time (sec) | Best cost (True cost) | Best weight (True weight) |Items| Match |
|-----------------|------------|----------|------------|-----|------|
| 1               | 0.0066   | 309(309)      | 165(165)        | [1, 1, 1, 1, 0, 1, 0, 0, 0, 0] | True|
| 2               | 0.0050   | 51(51)      | 26(26)        | [0, 1, 1, 1, 0] | True |
| 3               | 0.0054   | 150(150)      | 190(190)        | [1, 1, 0, 0, 1, 0] | True |
| 4               | 0.0054   | 107(107)      | 50(50)        | [1, 0, 0, 1, 0, 0, 0] | True |
| 5               | 0.0299   | 900(900)      | 104(104)        | [1, 0, 1, 1, 1, 0, 1, 1] | True |
| 6               | 0.0126   | 1735(1735)   | 169(169)        | [0, 1, 0, 1, 0, 0, 1] | True |
| 7               | 0.0629   | 1447(1458)     | 750(749)        | [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1] | False |


# Traversal Salesman Problem

Optimal results are taken from http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf

## Results

|Benchmark  | Execution time (sec) | Min distance | Optimal distance |
|-----------|----------------------|--------------|------------------|
| fl417     | 136.28               | 126700.41    | 11861            |
| a280      | 63.767               | 11668.3936   | 2579             |
| ch150     | 29.796               | 17648.615    | 6528             |
| att48     | 11.639               | 11821        | 10628            |
| bays29    | 3.579                | 2097         | 2020             |
| gr17      | 0.603                | 2524         | 2085             |
