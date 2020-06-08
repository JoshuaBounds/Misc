
"""
Plots universal destabilization as `r` increases.
"""

r = 3.6
x = 0.4

for _ in range(100):
    print(x)
    x = r * x * (1.0 - x)
