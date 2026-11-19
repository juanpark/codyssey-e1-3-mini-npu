# In CNN/NPU work the little grid of weights you slide over an input is called a kernel (interchangeably with "filter")
def mac(kernel: list[list[float]], pattern: list[list[float]]) -> float:
    score = 0.0
    for r in range(len(kernel)):
        for c in range(len(kernel[r])):
            score += pattern[r][c] * kernel[r][c]
    return score

def mac_1d(kernel: list[float], pattern: list[float]) -> float:
    score = 0.0
    for i in range(len(kernel)):
        score += kernel[i] * pattern[i]
    return score

def flatten(grid: list[list[float]]) -> list[float]:
    return [num for sublist in grid for num in sublist]

if __name__ == '__main__':
    import json
    with open("data.json", "r") as f:
        data = json.load(f)

    size_5_filters = data["filters"]["size_5"]
    size_5_input = data["patterns"]["size_5_1"]["input"]

    for filter_name in data["filters"]["size_5"].keys():
        print(f"{filter_name}: {mac(size_5_filters[filter_name], size_5_input)}")

    flatten(data["patterns"]["size_5_1"]["input"])


