from judge import judge
from mac import mac
from time import perf_counter

MARGIN = "=" * 50
MODE1_VERDICT = {"a":"A", "b":"B", "tied":"판정 불가 (|A - B| < 1e-9)"}
REPS = 10_000

def read_row(n: int, prompt: str) -> list[float]:
    while True:
        tokens = input(prompt).split()
        if len(tokens) != n:
            print(f"숫자를 공백으로 구분해 {n}개 입력하세요.")
            continue
        try:
            return [float(t) for t in tokens]
        except ValueError:
            print(f"숫자만 입력 가능합니다.")

def read_grid(n: int, label: str) -> list[list[float]]:
    grid = []
    for i in range(n):
        grid.append(read_row(n, f"[{label}] {i + 1}행 숫자 {n}개를 입력하세요: "))
    return grid

def print_header(title: str) -> None:
    print(MARGIN)
    print(title)
    print(MARGIN)

def benchmark_mac(kernel: list[list[float]], pattern: list[list[float]], reps: int) -> float:
    """Return the average time per mac() call, in milliseconds."""
    start = perf_counter()
    for _ in range(reps):
        mac(kernel, pattern)
    end = perf_counter()
    return ((end - start) / reps) * 1000

def run_mode1() -> None:
    print_header("[1] 필터 입력")
    print("필터 A (3줄 입력, 공백 구분)")
    filter_a = read_grid(3, "Filter A")
    print()

    print("필터 B (3줄 입력, 공백 구분)")
    filter_b = read_grid(3, "Filter B")
    print()

    print_header("[2] 패턴 입력")
    print("패턴 (3줄 입력, 공백 구분)")
    pattern = read_grid(3, "Pattern")
    print()

    # Result section
    score_a = mac(filter_a, pattern)
    score_b = mac(filter_b, pattern)
    result = judge(score_a, score_b)

    if result == "tied":
        print_header("[3] MAC 결과 (판정 불가)")
    else:
        print_header("[3] MAC 결과")

    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")

    # to match mission guideline example where computation is not printed when tied
    if result != "tied":
        ms = benchmark_mac(filter_a, pattern, REPS)
        print(f"연산 시간(평균/{REPS}회): {ms:.6f}ms")
    print(f"판정: {MODE1_VERDICT[result]}")

if __name__ == "__main__":
    # print(read_row(3, "숫자 3개 입력하세요: "))

    # label: str = "Filter A"
    # print(read_grid(3, label))

    run_mode1()