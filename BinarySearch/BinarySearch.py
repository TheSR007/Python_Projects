def BinarySearch(list, target): #use (in keyword) for linear search
    left = 0
    right = len(list) - 1
    while left <= right:
        mid = (left + right) // 2
        if list[mid] == target:
            return mid
        elif list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None


def binary_search(list,target):
    return BinarySearch(list,target)

def bs(list,target):
    return BinarySearch(list,target)


def main():
    list = [-6, -2, 0, 1, 2, 6, 9, 30, 33]
    print("Test 1:", BinarySearch(list, 33))
    print("Test 2:", BinarySearch(list, 69))


if __name__ == "__main__":
    main()

