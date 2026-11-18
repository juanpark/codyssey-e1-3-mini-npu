from mac import mac
from judge import judge

# --- fixtures: clean 0/1 grids (exact in float, so == is safe here) ---
cross = [
    [0,1,0],
    [1,1,1],
    [0,1,0],
]

x = [
    [1,0,1],
    [0,1,0],
    [1,0,1],
]

# --- mac: a kernel against itself scores highest; against the opposite, low ---
assert mac(cross, cross) == 5.0, f"cross, cross: expect 5.0, got {mac(cross, cross)}"
assert mac(x, x) == 5.0, f"x, x: expect 5.0, got {mac(x, x)}"
assert mac(cross, x) == 1.0, f"cross, x: expect 1.0, got {mac(cross, x)}"
assert mac(x, cross) == 1.0, f"x, cross: expect 1.0, got {mac(x, cross)}"

# --- judge: higher wins; near-equal is a tie ---
assert judge(5.0, 1.0) == "a", "higher first arg -> a"
assert judge(1.0, 5.0) == "b", "higher second arg -> b"
assert judge(0.9, 0.9) == "tied", "exactly equal -> tied"
# epsilon bracket -- pick values FAR from the 1e-9 edge so the test can never flip:
# 0.8999999999999999 is the REAL data.json gap (~1e-16, ten-million x under 1e-9) -> must tie.
assert judge(0.9, 0.8999999999999999) == "tied", "within epsilon (real float noise) -> tied"
# 0.1 is a genuine difference (far OVER anything epsilon covers) -> must NOT tie.
assert judge(0.9, 0.8) == "a", "0.1 gap is real, not noise -> a wins"

# --- WHERE IT BREAKS: run once to SEE it fail, then comment this line out ---
# A 1e-9 gap LOOKS like a real difference, so you'd expect "a". But (0.9 - (0.9 - 1e-9))
# lands a hair UNDER 1e-9 in float, so judge ties it instead. This assert fails on purpose:
# proof that right ON the threshold, rounding -- not your intent -- decides the verdict.
# assert judge(0.9, 0.9 - 1e-9) == "a", f"razor's edge: expected a, got {judge(0.9, 0.9 - 1e-9)!r}"

print("all test passed")