
def mac(rows: int, columns: int) -> None:
    n = rows
    count = 0

    for r in range(rows):
        for c in range(columns):
            count += 1
    print(f"{n}x{n} calculations: {count}")

if __name__ == '__main__':
    mac(3,3)
    mac(5,5)
    mac(13,13)
    mac(25,25)






