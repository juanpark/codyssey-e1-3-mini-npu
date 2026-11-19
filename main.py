import json
from judge import judge
from mac import mac, mac_1d, flatten
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

def benchmark_flat_mac(grid1: list[float], grid2: list[float], reps: int) -> float:
    """Return the average time per mac_1d() call, in milliseconds."""
    start = perf_counter()
    for _ in range(reps):
        mac_1d(grid1, grid2)
    end = perf_counter()
    return ((end - start) / reps) * 1000

def run_mode1() -> None:
    print_header("[1] 필터 입력")
    print("필터 A (3줄 입력, 공백 구분)")
    filter_a = read_grid(3, "Filter A")
    print("✓ 필터 A 저장 완료")
    print()

    print("필터 B (3줄 입력, 공백 구분)")
    filter_b = read_grid(3, "Filter B")
    print("✓ 필터 B 저장 완료")
    print()

    print_header("[2] 패턴 입력")
    print("패턴 (3줄 입력, 공백 구분)")
    pattern = read_grid(3, "Pattern")
    print("✓ 패턴 저장 완료")
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

NORM_EXPECTED = {"x":"X", "+":"Cross"}
NORM_VERDICT = {"a":"Cross", "b":"X", "tied":"UNDECIDED"}
GRID_SIZES = [3, 5, 13, 25]
def run_mode2(path: str = "data.json") -> None:
    print_header("[1] 필터 로드")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    filters = data["filters"]

    for filter_size in filters:
        print(f"✓ {filter_size} 필터 로드 완료 (Cross, X)")
    print()

    print_header("[2] 패턴 분석 (라벨 정규화 적용)")
    patterns = data["patterns"]
    total_test = total_passed = total_failed = 0
    failed_cases = []
    for key, pattern in patterns.items():
        total_test += 1
        print(f"--{key}--")

        try:
            size_name = key.rsplit("_", 1)[0]

            cross = filters[size_name]["cross"]
            x = filters[size_name]["x"]
            pattern_in = pattern["input"]

            # size validation — per-case FAIL on shape mismatch (mission: never crash)
            size = int(size_name.rsplit("_", 1)[1])
            bad_shape = [name for name, g in {"cross": cross, "x": x, "input": pattern_in}.items() if
                         not is_n_by_n(g, size)]

            if bad_shape:
                msg = f"{key}: 크기 불일치 ({', '.join(bad_shape)} != {size}x{size})"
                print(msg)
                failed_cases.append(msg)
                total_failed += 1
                continue

            score_a = mac(cross, pattern_in)
            score_b = mac(x, pattern_in)
            result = judge(score_a, score_b)

            print(f"Cross 점수: {score_a}")
            print(f"X 점수: {score_b}")
            verdict = NORM_VERDICT[result]
            expected = NORM_EXPECTED[pattern["expected"]]

        except (KeyError, ValueError, TypeError) as e:
            msg = f"{key}: 데이터 오류 ({type(e).__name__})"
            print(msg)
            failed_cases.append(msg)
            total_failed += 1
            continue


        passed = verdict == expected
        if passed:
            label = "PASS"
            total_passed += 1
        elif verdict == NORM_VERDICT["tied"]:
            label = "FAIL (epsilon 동점규칙)"
            failed_cases.append(f"{key}: 동점(UNDECIDED) 처리 규칙에 따른 FAIL")
            total_failed += 1
        else:
            label = "FAIL"
            failed_cases.append(f"{key}: 판정: {verdict} | expected: {expected} | {label}")
            total_failed += 1

        print(f"판정: {verdict} | expected: {expected} | {label}")
        print()

    print_header(f"[3] 성능 분석 (평균/{REPS}회)")
    print(f"{' 크기':<2}  {'평균시간(ms)':^10} {'1D평균(ms)':^9}  {'속도향상':^5}  {'연산횟수':>4}")
    print(MARGIN)
    for n in GRID_SIZES:
        grid = make_grid(n)
        benchmark = benchmark_mac(grid, grid, REPS)
        flat_grid = flatten(grid)
        flat_benchmark = benchmark_flat_mac(flat_grid, flat_grid, REPS)
        print(f"{n:>2}x{n:<4} {benchmark:<.6f} {flat_benchmark:>10.6f} "
              f"  +{(benchmark - flat_benchmark) / benchmark * 100:.1f}% {n*n:>8}")
    print()

    print_header(f"[4] 결과 요약")
    print(f"총 테스트: {total_test}개")
    print(f"통과:     {total_passed}개")
    print(f"실패:     {total_failed}개")
    print()
    print("실패 케이스:")
    for case in failed_cases:
        print(f"- {case}")

def make_grid(n: int) -> list[list[float]]:
    return [[1.0 for _ in range(n)] for _ in range(n)]

def is_n_by_n(grid: list[list[float]], size: int) -> bool:
    return len(grid) == size and all(len(row) == size for row in grid)


def _clear():
    """Clear the screen so the next menu renders at the top."""
    print("\033[H\033[J", end="")


def main() -> None:
    try:
        while True:
            print_header("Mini NPU Simulator")
            print()
            print("[모드 선택]")
            print()
            print("1. 사용자 입력 (3x3)")
            print("2. data.json 분석")
            print("0. 종료")
            run = input("선택: ")

            if run == "0":
                print("프로그램을 종료합니다...")
                return
            elif run == "1":
                run_mode1()
            elif run == "2":
                run_mode2()
            else:
                print("번호를 입력하세요.")
                input("\n계속하려면 Enter을 누르세요...")
                _clear()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다...")



if __name__ == "__main__":
    # print(read_row(3, "숫자 3개 입력하세요: "))

    # label: str = "Filter A"
    # print(read_grid(3, label))

    # make_grid(5)
    # run_mode1()
    run_mode2()
    # run_mode2("data_expected_mod.json")
    # run_mode2("data_error_mod.json")
    # main()

