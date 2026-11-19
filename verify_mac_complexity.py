
def count_mac_ops(n: int) -> int:
    count = 0
    for r in range(n):
        for c in range(n):
            count += 1
    return count

if __name__ == "__main__":
    for n in (3, 5, 13, 25):
        counted = count_mac_ops(n)
        print(f"{n:>2}x{n:<2}  counted={counted:>3}  n*n={n*n:>3}  match={counted == n*n}")






