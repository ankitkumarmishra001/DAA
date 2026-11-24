"""Sorting algorithms used to prioritise parcels.

merge_sort : main algorithm in the pipeline (stable, guaranteed O(n log n))
quick_sort : used for comparison in the performance phase
"""
import random


def parcel_sort_key(p):
    """Most urgent first (small deadline); ties -> higher priority first."""
    return (p.deadline, -p.priority)


# ---------------------------------------------------------------- Merge Sort
def merge_sort(arr, key=lambda x: x):
    """Stable top-down merge sort. Returns a NEW sorted list.

    Time : O(n log n) in best, average and worst case
    Space: O(n) for the temporary lists
    """
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return _merge(left, right, key)


def _merge(left, right, key):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        # "<=" takes from the left on ties -> this is what makes it STABLE
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# ---------------------------------------------------------------- Quick Sort
def quick_sort(arr, key=lambda x: x):
    """In-place randomised quick sort on a COPY of the input.

    Time : O(n log n) average, O(n^2) worst case (very unlikely with a random pivot)
    Space: O(log n) recursion stack. Not stable.
    """
    a = list(arr)
    _quick_sort(a, 0, len(a) - 1, key)
    return a


def _quick_sort(a, lo, hi, key):
    while lo < hi:
        p = _partition(a, lo, hi, key)
        # recurse into the smaller half, loop on the larger -> stack stays O(log n)
        if p - lo < hi - p:
            _quick_sort(a, lo, p - 1, key)
            lo = p + 1
        else:
            _quick_sort(a, p + 1, hi, key)
            hi = p - 1


def _partition(a, lo, hi, key):
    r = random.randint(lo, hi)            # random pivot
    a[r], a[hi] = a[hi], a[r]
    pivot = key(a[hi])
    i = lo - 1
    for j in range(lo, hi):
        if key(a[j]) <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1
