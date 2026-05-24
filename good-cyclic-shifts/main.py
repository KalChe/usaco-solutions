import sys

#define the merge function for inv counts
def merge(a, arr, left, right):
    middle = (left + right) // 2
    i, j, k = left, middle + 1, left
    inv = 0
    while (i <= middle and j <= right):
        if a[i] <= a[j]:
            arr[k] = a[i]
            i += 1
        else:
            arr[k] = a[j]
            inv += (middle - i + 1)
            j += 1
        k += 1
    while i <= middle:
        arr[k] = a[i]
        i += 1
        k += 1
    while j <= right:
        arr[k] = a[j]
        j += 1
        k += 1
    for i in range(left, right + 1):
        a[i] = arr[i]
    return inv

def sort(a, arr, left, right):
    inv = 0
    if (left < right):
        middle = (left + right) // 2
        inv += sort(a, arr, left, middle)
        inv += sort(a, arr, middle + 1, right)
        inv += merge(a, arr, left, right)
    return inv

#arr is a passed in array
def inversions(arr):
    length = len(arr)
    bit = [0] * (length + 1)

    inverse = 0
    seen_values = 0
    for value in arr:
        prefix_sum = 0
        index = value
        while index > 0:
            prefix_sum += bit[index]
            index -= index & (-index)

        inverse += seen_values - prefix_sum

        index = value
        while index <= length:
            bit[index] += 1
            index += index & (-index)

        seen_values += 1

    return inverse
    
def shifts(p):
    length = len(p)
    difference = [0] * (length + 1)
    for i in range(length):
        iterated_value = p[i]
        left = (i - iterated_value + 1) % length
        right = (i)
        if(left > right):
            difference[0] += 1
            difference[right + 1] -= 1
            difference[left] += 1
            difference[length] -= 1
        else:
            difference[left] += 1
            difference[right + 1] -= 1
        
    cumulative_sum = 0
    shift = []
    for i in range(length):
        cumulative_sum += difference[i]
        shift.append(cumulative_sum)
    
    return shift

# testcase solver
def testcase(N, p):
    counts = inversions(p)
    cost = 0
    num_shifts = shifts(p)
    answer_descending = []
    has_zero = 0
    for (i, c) in enumerate(p, start=1):
        if c >= i:
            cost += c - i
        else:
            cost += i - c
    
    left = 0
    while (left < N):
        if counts * 2 <= cost:
            right_shift = (-left) % N
            if right_shift == 0:
                has_zero = 1
            else:
                answer_descending.append(right_shift)

        if left < N - 1:
            counts += (N + 1 - 2 * p[left])
            cost += 2 * (num_shifts[left] - p[left])

        left += 1

    answer_descending.reverse()
    if has_zero:
        return [0] + answer_descending
    return answer_descending


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    T = data[0]
    idx = 1
    out = []

    for i in range(T):
        N = data[idx]
        idx += 1
        p = data[idx:idx+N]
        idx += N
        ANSWER = testcase(N, p)
        out.append(str(len(ANSWER)))
        out.append(' '.join(map(str, ANSWER)))
    sys.stdout.write('\n'.join(out) + '\n')

    #T = int(input())
    #for i in range(T):
    #    N = int(input())
    #    p = list(map(int, input().split()))
    #    ANSWER = testcase(N, p)
    #    print(len(ANSWER))
    #    print(*ANSWER)

solve()