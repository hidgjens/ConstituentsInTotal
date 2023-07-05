"""
Find unique combination of numbers that sum up to a list of totals.

Given a list of totals, and a list of potential constituents, find
which constituents contribute to each total where no constituent is used twice.

Constituents can be positive or negative.

Example:
    $ python find_solutions.py --values 1 2 3 4 5 6 --totals 12 9;

    [Found 5 unique solution(s)]:
        [Unique solution 1]:
            9   = (1 + 2 + 3 + 5);
            12  = (2 + 4 + 6);

        [Unique solution 2]:
            9   = (4 + 5);
            12  = (1 + 2 + 3 + 6);

        [Unique solution 3]:
            9   = (2 + 3 + 4);
            12  = (1 + 5 + 6);

        [Unique solution 4]:
            9   = (1 + 2 + 6);
            12  = (3 + 4 + 5);

        [Unique solution 5]:
            9   = (3 + 6);
            12  = (1 + 2 + 4 + 5);
"""
from __future__ import annotations

from collections.abc import Container
from collections.abc import Iterable
from collections.abc import Sequence

SOLUTION = tuple[int, ...]
"""The indices which sum to the desired total."""


def read_floats_from_file(path: str) -> list[float]:
    """
    Read a list of floats from file.

    :param path:
        Path contain values. Must have one float per line.
    :type path:
        str
    :return:
        Loaded floats.
    :rtype:
        list[float]
    """
    values = []
    with open(path, "r") as in_file:
        for line in in_file:
            values.append(float(line.strip()))
    return values


def find_constituents(
    constituents: Sequence[float],
    total: float,
    *,
    used_indices: Container[int] = ...,
    precision: int = 3,
    tol: float = 1e-4,
) -> set[SOLUTION]:
    """
    Find all possible combinations of values which sum to
    the given total.

    :param constituents:
        List of possible values that could sum to total.
    :type constituents:
        Sequence[float]
    :param total:
        Total value to make from constituents.
    :type total:
        float
    :param used_indices:
        Indices which should be excluded from consideration.
        Used for recursive calls, defaults to empty list.
    :type used_indices:
        Container[int], optional
    :param precision:
        Number of decimals with which to round floats to, defaults to 3.
    :type precision:
        int, optional
    :param tol:
        Acceptable tolerance for comparing floats, defaults to 1e-4.
    :type tol:
        float, optional
    :return:
        The set of possible solutions. Each element is a tuple of indices
        indicating which constituents can be summed to the total.
    :rtype:
        set[SOLUTION]
    """
    if used_indices is Ellipsis:
        used_indices = []

    if used_indices:
        last_index = used_indices[-1]
    else:
        last_index = -1
    start_index = last_index + 1
    total = round(total, precision)
    min_remaining = min(
        [c for i, c in enumerate(constituents) if i not in used_indices]
    )
    min_remaining = min(min_remaining, 0)
    all_solutions = set()
    for index, constituent in enumerate(constituents[start_index:]):
        constituent = round(constituent, precision)
        index += start_index
        if constituent > total + tol + abs(min_remaining):
            continue
        if index in used_indices:
            continue
        new_total = total - constituent
        if -tol <= new_total <= tol:
            all_solutions.add(tuple(sorted(used_indices + [index])))
            continue
        solutions = find_constituents(
            constituents,
            new_total,
            used_indices=used_indices + [index],
        )
        for solution in solutions:
            all_solutions.add(solution)
    return all_solutions


def filter_unique_solutions(
    solutions: Sequence[set(SOLUTION)],
    used_indices: Container[int] = ...,
) -> list[list[SOLUTION]]:
    """
    Given a list of solutions for multiple totals, and find
    the combinations of solutions which do not reuse indices.

    :param solutions:
        A list contain a set of solutions for each total.
    :type solutions:
        Sequence[set(SOLUTION)]
    :param used_indices:
        Indices which should be excluded from consideration.
        Used for recursive calls, defaults to empty list.
    :type used_indices:
        Container[int], optional
    :return:
        A list of unique solutions. Each element represents
        a unique solution. Each unique solution is a list
        of tuples containing the indices for each total.
    :rtype:
        list[list[SOLUTION]]
    """
    if used_indices is Ellipsis:
        used_indices = set()

    all_solutions = []
    for solution in solutions[0]:
        if any(i in used_indices for i in solution):
            continue
        if len(solutions) == 1:
            all_solutions.append([solution])
        else:
            new_solutions = filter_unique_solutions(
                solutions=solutions[1:],
                used_indices=set([*used_indices, *solution]),
            )
            new_solutions = [[solution, *sol] for sol in new_solutions]
            all_solutions.extend(new_solutions)
    return all_solutions


def print_unique_solutions(
    unique_solutions: Iterable[Iterable[SOLUTION]],
    constituents: Sequence[float],
    totals: Sequence[float],
) -> None:
    """
    Print out the solutions in a readable way.

    :param unique_solutions:
        The unique solutions to be printed.
    :type unique_solutions:
        Iterable[Iterable[SOLUTION]]
    :param constituents:
        List of possible values that could sum to total.
    :type constituents:
        Sequence[float]
    :param totals:
        The list of totals which the solutions belong to.
    :type totals:
        Sequence[float]
    """
    for sol_index, unique_sol in enumerate(unique_solutions):
        print(f"Unique solution {sol_index+1}")
        for total_index, indices in enumerate(unique_sol):
            print(f"\tInput total: {totals[total_index]}")
            calc_total = 0
            for index in indices:
                calc_total += constituents[index]
                print(f"\t\t{index}: {constituents[index]}")
            print(f"\tCalculated total: {calc_total:.2f}\n")


def find_unique_solutions(
    constituents: Sequence[float],
    totals: Sequence[float],
    *,
    tol: float = 1e-4,
    precision: int = 3,
    show: bool = False,
) -> list[list[SOLUTION]]:
    """
    For a given list of totals, find which values from
    `constituents` can be summed to make each total, without
    using a value from `constituents` more than once.

    :param constituents:
        List of possible values that could sum to total.
    :type constituents:
        Sequence[float]
    :param totals:
        List of possible values that could sum to total.
    :type totals:
        Sequence[float]
    :param tol:
        Acceptable tolerance for comparing floats, defaults to 1e-4.
    :type tol:
        float, optional
    :param precision:
        Number of decimals with which to round floats to, defaults to 3.
    :type precision:
        int, optional
    :param show:
        Whether to print the solutions to console, defaults to False
    :type show:
        bool, optional
    :return:
        A list of unique solutions. Each element represents
        a unique solution. Each unique solution is a list
        of tuples containing the indices for each total.
    :rtype:
        list[list[SOLUTION]]
    """
    all_solutions: list[set(SOLUTION)] = [set() for _ in totals]
    for index, total in enumerate(totals):
        solutions = find_constituents(
            constituents=constituents,
            total=total,
            tol=tol,
            precision=precision,
        )
        all_solutions[index] = solutions
    # Need to find the unique combination
    unique_solutions = filter_unique_solutions(all_solutions)
    n_unique = len(unique_solutions)
    print(f"Found {n_unique} unique solution(s)")
    if show:
        print_unique_solutions(
            unique_solutions=unique_solutions,
            constituents=constituents,
            totals=totals,
        )
    return unique_solutions


def _test():
    constituents = [
        435.0,
        1034.0,
        10.4,
        54.3,
        130.0,
        284.2,
        41.2,
        5.90,
        91.7,
        -20.5,
        1562.6,
        725.0,
        54.0,
        899.0,
        -420.0,
        341.2,
        666.0,
        -246.8,
        398.4,
        61.5,
    ]

    print("Constituents:", constituents)

    answer_indices = [
        [0, 6, 9],
        [4, 8],
        [10, 17, 3, 11],
    ]

    totals = []
    for answer in answer_indices:
        total = 0
        for index in answer:
            total += constituents[index]
        totals.append(total)

    print("Totals:", totals)
    print("True solution:", answer_indices)

    find_unique_solutions(constituents=constituents, totals=totals)


def _main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-vp",
        "--values-path",
        nargs="?",
        type=str,
        default="",
        dest="values_path",
        help="Path to values. File should contain one float per line.",
    )
    parser.add_argument(
        "-tp",
        "--totals-path",
        nargs="?",
        type=str,
        default="",
        dest="totals_path",
        help="Path to totals. File should contain one float per line.",
    )

    parser.add_argument(
        "-v",
        "--values",
        nargs="+",
        type=float,
        default=[],
        dest="values",
        help="List of values to use.",
    )
    parser.add_argument(
        "-t",
        "--totals",
        nargs="+",
        type=float,
        default=[],
        dest="totals",
        help="List of totals to use.",
    )
    parser.add_argument(
        "--tolerance",
        nargs="?",
        type=float,
        default=1e-4,
        dest="tol",
        help="Acceptable tolerance when comparing floats.",
    )
    parser.add_argument(
        "-p",
        "--precision",
        nargs="?",
        type=int,
        default=2,
        dest="precision",
        help="Number of decimal places to round output to.",
    )
    parser.add_argument(
        "-T",
        "--test",
        default=False,
        dest="test",
        help="Run test code.",
        action="store_true",
    )

    # Parse sys argv
    parsed = parser.parse_args(sys.argv[1:])

    # See if test code was requested
    if parsed.test:
        _test()
        return

    # Check if values were given (or a path to values).
    values_given = bool(parsed.values)
    values_path_given = bool(parsed.values_path)
    if values_given and values_path_given:
        print(
            "Both '--values' and '--values-path' "
            "were given, only one should be given."
        )
        sys.exit(1)
    if not (values_given or values_path_given):
        print(
            "Neither '--values' or '--values-path' "
            "were given, only one should be given."
        )
        sys.exit(1)

    # Get values.
    if values_path_given:
        values = read_floats_from_file(parsed.values_path)
    else:
        values = parsed.values

    # Check if totals were given (or a path to totals).
    totals_given = bool(parsed.totals)
    totals_path_given = bool(parsed.totals_path)
    if totals_given and totals_path_given:
        print(
            "Both '--totals' and '--totals-path' "
            "were given, only one should be given."
        )
        sys.exit(1)
    if not (totals_given or totals_path_given):
        print(
            "Both '--totals' and '--totals-path' "
            "were given, only one should be given."
        )
        sys.exit(1)

    # Get totals.
    if totals_path_given:
        totals = read_floats_from_file(parsed.totals_path)
    else:
        totals = parsed.totals

    find_unique_solutions(
        constituents=values,
        totals=totals,
        tol=parsed.tol,
        precision=parsed.precision,
        show=True,
    )


if __name__ == "__main__":
    _main()
