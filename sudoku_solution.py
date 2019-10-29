from copy import deepcopy
import datetime
from visualization import plot_city


vertical = [
    (0, 17),
    (1, 16),
    (2, 15),
    (3, 14),
    (4, 13),
    (5, 12),
]

horizon = [
    (23, 6),
    (22, 7),
    (21, 8),
    (20, 9),
    (19, 10),
    (18, 11),
]


class Solutions:
    def __init__(self, child: list, parents: list):
        self.child = child
        self.parents = parents

    @property
    def variant(self):
        var = []
        var.clear()
        curr_variants = self.child
        pred_variants = self.parents
        for i in range(len(curr_variants)):
            for j in range(len(pred_variants)):
                if curr_variants[i] not in [int(el) for el in list(pred_variants[j])]:
                    var.append(''.join([str(curr_variants[i]), str(pred_variants[j])]))

        return sorted(var)


def seconds_from_start_till_now(start_time):
    return (datetime.datetime.now() - start_time).total_seconds()


def from_left(houses):
    seen = 1
    i = 0
    max = houses[i]
    while houses[i] != 6:
        if houses[i] > max:
            max = houses[i]
        if houses[i] <= houses[i + 1] and houses[i + 1] >= max:
            seen += 1
        i += 1
    return seen


def from_right(houses):
    houses = houses[::-1]
    seen = 1
    i = 0
    max = houses[i]
    while houses[i] != 6:
        if houses[i] > max:
            max = houses[i]
        if houses[i] <= houses[i + 1] and houses[i + 1] >= max:
            seen += 1
        i += 1
    return seen


def check_horizon(solution, condition):
    for i in range(6):
        i_l, i_r = horizon[i]
        street = [int(el) for el in solution[i * 6:(i + 1) * 6]]
        condition_l = condition[i_l]
        condition_r = condition[i_r]
        if condition[i_l] == 0:
            condition_l = from_left(street)
        if condition[i_r] == 0:
            condition_r = from_right(street)

        if from_left(street) != condition_l or from_right(street) != condition_r:
            return False

    return True


def check_vertical(solution, condition):
    for j in range(6):
        i_up, i_down = vertical[j]
        col = column(solution, j)
        street = [int(el) for el in col]
        condition_up = condition[i_up]
        condition_down = condition[i_down]
        if condition[i_up] == 0:
            condition_up = from_left(street)
        if condition[i_down] == 0:
            condition_down = from_right(street)
        if from_left(street) != condition_up or from_right(street) != condition_down:
            return False
    return True


def init_solve(condition, solve):
    for i in range(6):
        i_l, i_r = horizon[i]
        for j in range(6):
            i_up, i_down = vertical[j]
            # solve.append(f'по горизонтали:{condition[i_l],condition[i_r]}, по вертикали {condition[i_up], condition[i_down]}')
            if condition[i_l] == 1:
                solve[i * 6 + 0] = 6
            elif condition[i_r] == 1:
                solve[i * 6 + 5] = 6
            if condition[i_up] == 1:
                solve[0 * 6 + j] = 6
            elif condition[i_down] == 1:
                solve[5 * 6 + j] = 6
            if condition[i_l] == 6:
                solve[i * 6 + j] = j + 1
            elif condition[i_r] == 6:
                solve[i * 6 + j] = 6 - j
            if condition[i_up] == 6:
                solve[i * 6 + j] = i + 1
            elif condition[i_down] == 6:
                solve[i * 6 + j] = 6 - i

    return solve


def choose(solve, matrix, number, i, j):
    for k in range(6):
        matrix[k * 6 + j] = solve[k * 6 + j]
    for w in range(6):
        matrix[i * 6 + w] = solve[i * 6 + w]
    matrix[i * 6 + j] = number
    # return matrix


def column(matrix, j):
    col = []
    col.clear()
    for i in range(6):
        col.append(matrix[i * 6 + j])

    return col


def six(condition, solve):
    new_solve_v = deepcopy(solve)
    new_solve_h = deepcopy(solve)
    new_solve = deepcopy(solve)

    for i in range(6):
        i_up, i_down = vertical[i]
        col = column(solve, i)
        if 6 not in col:
            for j in range(6):
                if j >= (condition[i_up] - 1) and j <= (6 - condition[i_down]):
                    new_solve_v[j * 6 + i] = 6

    for i in range(6):
        i_l, i_r = horizon[i]
        if 6 not in solve[i * 6:(i + 1) * 6]:
            for j in range(6):
                if j >= condition[i_l] - 1 and j <= (6 - condition[i_r]):
                    new_solve_h[i * 6 + j] = 6

    for i in range(6):
        for j in range(6):
            if new_solve_v[i * 6 + j] == new_solve_h[i * 6 + j]:
                new_solve[i * 6 + j] = new_solve_v[i * 6 + j]

    return new_solve


def five(condition, solve):
    new_solve_v = deepcopy(solve)
    new_solve_h = deepcopy(solve)
    new_solve = deepcopy(solve)

    for i in range(6):
        i_up, i_down = vertical[i]
        col = column(solve, i)
        if 5 not in col:
            for j in range(6):
                if j >= (condition[i_up] - 2) and j <= (6 - condition[i_down] + 1) and solve[j * 6 + i] == 0:
                    new_solve_v[j * 6 + i] = 5
                # else:
                #     new_solve_v[j * 6 + i] = solve[j * 6 + i]

    for i in range(6):
        i_l, i_r = horizon[i]
        if 5 not in solve[i * 6:(i + 1) * 6]:
            for j in range(6):
                if j >= condition[i_l] - 2 and j <= (6 - condition[i_r] + 1) and solve[i * 6 + j] == 0:
                    new_solve_h[i * 6 + j] = 5
                # else:
                #     new_solve_h[i * 6 + j] = solve[j]

    for i in range(6):
        for j in range(6):
            if new_solve_v[i * 6 + j] == new_solve_h[i * 6 + j]:
                new_solve[i * 6 + j] = new_solve_v[i * 6 + j]

    return new_solve


def four(condition, solve):
    new_solve_v = deepcopy(solve)
    new_solve_h = deepcopy(solve)
    new_solve = deepcopy(solve)

    for i in range(6):
        i_up, i_down = vertical[i]
        col = column(solve, i)
        if 4 not in col:
            for j in range(6):
                if j >= (condition[i_up] - 3) and j <= (6 - condition[i_down] + 2) and solve[j * 6 + i] == 0:
                    new_solve_v[j * 6 + i] = 4
                # else:
                #     new_solve_v[j * 6 + i] = solve[j * 6 + i]

    for i in range(6):
        i_l, i_r = horizon[i]
        if 4 not in solve[i * 6:(i + 1) * 6]:
            for j in range(6):
                if j >= condition[i_l] - 3 and j <= (6 - condition[i_r] + 2) and solve[i * 6 + j] == 0:
                    new_solve_h[i * 6 + j] = 4
                # else:
                #     new_solve_h[i * 6 + j] = solve[j]

    for i in range(6):
        for j in range(6):
            if new_solve_v[i * 6 + j] == new_solve_h[i * 6 + j]:
                new_solve[i * 6 + j] = new_solve_v[i * 6 + j]

    return new_solve


def three(condition, solve):
    new_solve_v = deepcopy(solve)
    new_solve_h = deepcopy(solve)
    new_solve = deepcopy(solve)

    for i in range(6):
        i_up, i_down = vertical[i]
        col = column(solve, i)
        if 3 not in col:
            for j in range(6):
                if j >= (condition[i_up] - 4) and j <= (6 - condition[i_down] + 3) and solve[j * 6 + i] == 0:
                    new_solve_v[j * 6 + i] = 3

    for i in range(6):
        i_l, i_r = horizon[i]
        if 3 not in solve[i * 6:(i + 1) * 6]:
            for j in range(6):
                if j >= condition[i_l] - 4 and j <= (6 - condition[i_r] + 3) and solve[i * 6 + j] == 0:
                    new_solve_h[i * 6 + j] = 3

    for i in range(6):
        for j in range(6):
            if new_solve_v[i * 6 + j] == new_solve_h[i * 6 + j]:
                new_solve[i * 6 + j] = new_solve_v[i * 6 + j]

    return new_solve


def two(solve):
    new_solve = deepcopy(solve)

    for i in range(6):
        for j in range(6):
            if solve[j * 6 + i] == 0:
                new_solve[j * 6 + i] = 2

    return new_solve


def fill_one(solve):
    new_solve = solve
    for i in range(6):
        for j in range(6):
            if solve[i * 6 + j] == 0:
                new_solve[i * 6 + j] = 1
    return new_solve


def del_non_suitable(index_massive, condition):
    for el in index_massive:
        if check_horizon(el, condition) and check_vertical(el, condition):
            return [el]
    return []


def check_horizon_6(solution, condition):
    for i in range(6):
        i_l, i_r = horizon[i]
        street = [int(el) for el in solution[i * 6:(i + 1) * 6]]
        condition_l = condition[i_l]
        condition_r = condition[i_r]
        if condition_l == 0 and condition_r == 0:
            pass
        else:
            if condition[i_l] == 0:
                condition_l = from_left(street)
            if condition[i_r] == 0:
                condition_r = from_right(street)

            if from_left(street) != condition_l and from_right(street) != condition_r:
                return False

    return True


def check_vertical_6(solution, condition):
    for j in range(6):
        i_up, i_down = vertical[j]
        col = column(solution, j)
        street = [int(el) for el in col]
        condition_up = condition[i_up]
        condition_down = condition[i_down]
        if condition_down == 0 and condition_up == 0:
            pass
        else:
            if condition[i_up] == 0:
                condition_up = from_left(street)
            if condition[i_down] == 0:
                condition_down = from_right(street)
            if from_left(street) != condition_up and from_right(street) != condition_down:
                return False
    return True


def del_non_suitable_6(index_massive, condition):
    suitable = []
    for el in index_massive:
        if check_horizon_6(el, condition) and check_vertical_6(el, condition):
            suitable.append(el)
    return suitable


def make_solve(index_str: str, solve: list, number: int):
    new_solve = deepcopy(solve)
    index = list(index_str)
    for i in range(6):
        for j in range(6):
            if solve[i * 6 + j] != number:
                new_solve[i * 6 + j] = solve[i * 6 + j]
            elif solve[i * 6 + j] == number and i != int(index[j]):
                new_solve[i * 6 + j] = 0

    return new_solve


def variants(solve, number):
    index_massive = []
    variants_massive = []
    for j in range(6):
        index = []
        index.clear()
        for i in range(6):
            if solve[i * 6 + j] == number:
                index.append(i)
        index_massive.append(index)

    index_massive = index_massive[::-1]
    for i in range(6):
        if i == 0:
            parents = [str(el) for el in index_massive[0]]
        else:
            curr_digit = Solutions(index_massive[i], parents)
            parents = curr_digit.variant

    for i in range(len(parents)):
        variants_massive.append(make_solve(parents[i], solve, number))
    return variants_massive


def len_without_missing(cond):
    i = 0
    for el in cond:
        if el != 0:
            i += 1
    return i


def decision(cond_input):
    # print('===== solving (seconds) ======')
    # start_time = datetime.datetime.now()

    cond_list = cond_input.split(',')
    condition = [int(x) for x in cond_list]
    len_cond = len_without_missing(condition)
    # print(condition)
    index = []
    j = 0
    solve_0 = []
    for i in range(6):
        for j in range(6):
            solve_0.append(0)
    solve_init = init_solve(condition, solve_0)
    solve = six(condition, solve_init)
    index_6 = variants(solve, 6)
    if len_cond <= 3:
        index_6 = [index_6[0]]

    # index_6 = del_non_suitable_6(index_6, condition)

    # print('6: ' + str(seconds_from_start_till_now(start_time)))
    # start_time = datetime.datetime.now()

    index_5 = []
    for i in range(len(index_6)):
        solve_5 = five(condition, index_6[i])
        index.clear()
        index = variants(solve_5, 5)
        index_5.extend(index)
    if len_cond <= 3:
        index_5 = [index_5[0]]
    # index_5 = del_non_suitable_6(index_5, condition)

    # print('5: ' + str(seconds_from_start_till_now(start_time)))
    # start_time = datetime.datetime.now()

    index_4 = []
    for i in range(len(index_5)):
        solve_4 = four(condition, index_5[i])
        index.clear()
        index = variants(solve_4, 4)
        index_4.extend(index)
    index_4 = del_non_suitable_6(index_4, condition)
    if len_cond <= 3:
        index_4 = [index_4[0]]

    # print('4: ' + str(seconds_from_start_till_now(start_time)))
    # start_time = datetime.datetime.now()

    index_3 = []
    for i in range(len(index_4)):
        solve_3 = three(condition, index_4[i])
        index.clear()
        index = variants(solve_3, 3)
        index = del_non_suitable_6(index, condition)
        index_3.extend(index)

    index_3 = del_non_suitable_6(index_3, condition)
    if len_cond <= 3:
        index_3 = [index_3[0]]

    # print('3: ' + str(seconds_from_start_till_now(start_time)))
    # start_time = datetime.datetime.now()

    index_2 = []
    for i in range(len(index_3)):
        solve_2 = two(index_3[i])
        index.clear()
        index = variants(solve_2, 2)
        index_2.extend(index)

    index_2 = del_non_suitable(index_2, condition)

    # print('2: ' + str(seconds_from_start_till_now(start_time)))

    if len(index_2) == 0:
        index_1 = [0]
    else:
        index_1 = fill_one(index_2[0])


    # answer = [str(el) for el in index_1]
    # return ','.join(answer)
    return index_1


def main():
    cond_input = input()
    solution = decision(cond_input)
    plot_city(solution)
    print(solution)


if __name__ == '__main__':
    main()
