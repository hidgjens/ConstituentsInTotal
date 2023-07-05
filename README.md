# Find Constituents to Total

For a given list of totals, find which values from a list of potential constituents can be summed to make each total, without using a constituent more than once.

A friend came to me with this problem for work. I thought it was interesting so I made a Python script which could
solve this problem fairly efficiently and provide all possible solutions.

## Example

    $ python find_solutions.py --values 1 2 3 4 5 6 --totals 12 9

    Found 5 unique solution(s)
    Unique solution 1
            Input total: 12.0
                    0: 1.0
                    1: 2.0
                    3: 4.0
                    4: 5.0
            Calculated total: 12.00

            Input total: 9.0
                    2: 3.0
                    5: 6.0
            Calculated total: 9.00

    Unique solution 2
            Input total: 12.0
                    1: 2.0
                    3: 4.0
                    5: 6.0
            Calculated total: 12.00

            Input total: 9.0
                    0: 1.0
                    2: 3.0
                    4: 5.0
            Calculated total: 9.00

    Unique solution 3
            Input total: 12.0
                    2: 3.0
                    3: 4.0
                    4: 5.0
            Calculated total: 12.00

            Input total: 9.0
                    0: 1.0
                    1: 2.0
                    5: 6.0
            Calculated total: 9.00

    Unique solution 4
            Input total: 12.0
                    0: 1.0
                    4: 5.0
                    5: 6.0
            Calculated total: 12.00

            Input total: 9.0
                    1: 2.0
                    2: 3.0
                    3: 4.0
            Calculated total: 9.00

    Unique solution 5
            Input total: 12.0
                    0: 1.0
                    1: 2.0
                    2: 3.0
                    5: 6.0
            Calculated total: 12.00

            Input total: 9.0
                    3: 4.0
                    4: 5.0
            Calculated total: 9.00