import itertools
import json
import re
from fractions import Fraction
from pathlib import Path


def identity(order):
    return [[int(row == column) for column in range(order)] for row in range(order)]


def multiply(left, right):
    order = len(left)
    return [
        [sum(left[row][index] * right[index][column] for index in range(order))
         for column in range(order)]
        for row in range(order)
    ]


def determinant(matrix):
    order = len(matrix)
    reduced = [[Fraction(entry) for entry in row] for row in matrix]
    value = Fraction(1)
    for column in range(order):
        pivot = next((row for row in range(column, order) if reduced[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            reduced[column], reduced[pivot] = reduced[pivot], reduced[column]
            value = -value
        diagonal = reduced[column][column]
        value *= diagonal
        for row in range(column + 1, order):
            factor = reduced[row][column] / diagonal
            for index in range(column + 1, order):
                reduced[row][index] -= factor * reduced[column][index]
            reduced[row][column] = Fraction(0)
    return value


def inverse(matrix):
    order = len(matrix)
    reduced = [
        [Fraction(entry) for entry in row + identity(order)[index]]
        for index, row in enumerate(matrix)
    ]
    for column in range(order):
        pivot = next(row for row in range(column, order) if reduced[row][column])
        reduced[column], reduced[pivot] = reduced[pivot], reduced[column]
        diagonal = reduced[column][column]
        reduced[column] = [entry / diagonal for entry in reduced[column]]
        for row in range(order):
            if row == column:
                continue
            factor = reduced[row][column]
            reduced[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(reduced[row], reduced[column])
            ]
    return [row[order:] for row in reduced]


def maximum(matrix):
    return max(abs(entry) for row in matrix for entry in row)


def check(condition, label):
    if not condition:
        raise ValueError(label)


def family(signs, constant):
    return [
        [constant + (signs[row] if row == column else 0)
         for column in range(len(signs))]
        for row in range(len(signs))
    ]


def check_family(signs, constant):
    order = len(signs)
    delta = sum(signs)
    matrix = family(signs, constant)
    expected = (-1) ** signs.count(-1) * (1 + constant * delta)
    actual = determinant(matrix)
    check(actual == expected, 'family determinant')
    admissible = delta == 0 or (constant == 2 and delta == -1)
    check((abs(actual) == 1) == admissible, 'unimodularity alternatives')
    denominator = 1 + constant * delta
    candidate = [
        [(signs[row] if row == column else 0)
         - Fraction(constant * signs[row] * signs[column], denominator)
         for column in range(order)]
        for row in range(order)
    ]
    check(multiply(matrix, candidate) == identity(order), 'family right inverse')
    check(multiply(candidate, matrix) == identity(order), 'family left inverse')
    if admissible:
        check(inverse(matrix) == candidate, 'independent elimination inverse')
        check(all(entry.denominator == 1 for row in candidate for entry in row), 'integrality')
        check(all(entry > 0 for row in matrix for entry in row), 'positivity')
        check(all(entry != 0 for row in candidate for entry in row), 'zerofreeness')
        check(maximum(matrix) == maximum(candidate) == constant + 1, 'balanced maximum')
    return int(admissible)


def main():
    data = json.loads(Path(__file__).with_name('witness.json').read_text())
    matrix, candidate = data['A'], data['B']
    check(len(matrix) == len(candidate) == 6, 'order six')
    check(all(len(row) == 6 for row in matrix + candidate), 'six columns')
    check(all(isinstance(entry, int) for row in matrix + candidate for entry in row), 'integer entries')
    check(multiply(matrix, candidate) == identity(6), 'displayed right inverse')
    check(multiply(candidate, matrix) == identity(6), 'displayed left inverse')
    check(determinant(matrix) == determinant(candidate) == -1, 'displayed determinants')
    check(inverse(matrix) == candidate, 'displayed elimination inverse')
    check(all(entry != 0 for row in matrix + candidate for entry in row), 'displayed zerofreeness')
    check(maximum(matrix) == maximum(candidate) == 3, 'displayed maxima')
    check(matrix == family([1, 1, 1, -1, -1, -1], 2), 'displayed family instance')
    source = Path(__file__).with_name('note.tex').read_text()
    pairs = {'A': matrix, 'B': candidate}
    neighbours = json.loads(Path(__file__).with_name('sibling-witnesses.json').read_text())
    neighbour_output = []
    for height in [4, 5]:
        item = neighbours[str(height)]
        first, second = item['matrix'], item['inverse']
        check(len(first) == len(second) == 6, 'neighbour order')
        check(all(len(row) == 6 for row in first + second), 'neighbour columns')
        check(all(isinstance(entry, int) for row in first + second for entry in row), 'neighbour integer entries')
        check(multiply(first, second) == multiply(second, first) == identity(6), 'neighbour inverse products')
        check(determinant(first) == determinant(second) == 1, 'neighbour determinants')
        check(inverse(first) == second, 'neighbour elimination inverse')
        check(all(entry > 0 for row in first for entry in row), 'neighbour positivity')
        check(all(entry != 0 for row in second for entry in row), 'neighbour inverse zerofreeness')
        check(maximum(first) == 3 and maximum(second) == height, 'neighbour maxima')
        pairs[f'C_{height}'], pairs[f'E_{height}'] = first, second
        neighbour_output.append({'order': 6, 'det_matrix': 1, 'det_inverse': 1,
                                 'alpha': 3, 'beta': height, 'zero_entries': 0,
                                 'products': 'Both I_6', 'inverse_by_elimination': 'Matches displayed inverse'})
    for label, expected_matrix in pairs.items():
        match = re.search(re.escape(label) + r'&=\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}', source, re.S)
        check(match is not None, 'matrix present in LaTeX: ' + label)
        displayed = [[int(entry.strip()) for entry in row.strip().split('&')]
                     for row in match.group(1).strip().split('\\\\')]
        check(displayed == expected_matrix, 'LaTeX entries: ' + label)
    cited_cases = 0
    for height in range(3, 21):
        small = [[1, 2, 3], [height, 1, -height], [height, height, height - 1]]
        large = [[1, height, height, height],
                 [height - 2, height, -height + 1, -height],
                 [height, 3, 2, -height + 1],
                 [height, -height + 1, height, -height]]
        for cited, expected_maximum in [(small, height * (2 * height - 1)),
                                        (large, height * (2 * height - 1) * (2 * height + 1))]:
            check(abs(determinant(cited)) == 1, 'cited extremal determinant')
            cited_inverse = inverse(cited)
            check(all(entry != 0 for row in cited + cited_inverse for entry in row), 'cited extremal zerofreeness')
            check(maximum(cited) == height, 'cited extremal matrix maximum')
            check(maximum(cited_inverse) == expected_maximum, 'cited extremal inverse maximum')
            cited_cases += 1
    representative_cases = 0
    representative_unit_cases = 0
    for order in range(2, 13):
        for positive_count in range(order + 1):
            signs = [1] * positive_count + [-1] * (order - positive_count)
            for constant in range(2, 9):
                representative_unit_cases += check_family(signs, constant)
                representative_cases += 1
    sign_cases = 0
    sign_unit_cases = 0
    for order in range(2, 9):
        for signs in itertools.product([-1, 1], repeat=order):
            for constant in range(2, 5):
                sign_unit_cases += check_family(list(signs), constant)
                sign_cases += 1
    output = {
        'status': 'pass',
        'arithmetic': 'Exact integers and fractions.Fraction; no floating-point operations.',
        'displayed_example': {
            'order': 6, 'det_A': -1, 'det_B': -1, 'alpha': 3, 'beta': 3,
            'zero_entries_A': 0, 'zero_entries_B': 0,
            'AB': 'I_6', 'BA': 'I_6', 'inverse_by_elimination': 'B',
        },
        'neighbouring_examples': neighbour_output,
        'latex_matrix_data': 'All six displayed matrices agree entrywise with the witness data.',
        'cited_extremal_families': {'source': 'Finch, arXiv:2605.03691v4, Section 9, page 12, matrices U and V.',
                                  'heights_inclusive': [3, 20], 'cases': cited_cases,
                                  'scope': 'Exact finite checks of the cited lower-bound examples; upper bounds are the cited theorems.'},
        'family_sign_count_cases': {
            'orders_inclusive': [2, 12], 'constants_inclusive': [2, 8],
            'sign_counts': 'Every positive-sign count from 0 through n; positive signs first.',
            'cases': representative_cases, 'unimodular_cases': representative_unit_cases,
        },
        'family_all_sign_cases': {
            'orders_inclusive': [2, 8], 'constants_inclusive': [2, 4],
            'sign_vectors': 'Every element of {-1,1}^n.',
            'cases': sign_cases, 'unimodular_cases': sign_unit_cases,
        },
        'scope': 'Finite exact checks of the displayed matrices and stated ranges. '
                 'The all-order result follows from the written determinant and inverse identities.',
    }
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
