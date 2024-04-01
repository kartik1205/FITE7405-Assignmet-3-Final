from ArthAsianOption import ArithmaticAsianOption

# Tests
S = 100
K = 100
sigma = 0.2
r = 0.05
T = 3
N = 100
M = 100000
sigma_list = [0.3, 0.3, 0.4, 0.3, 0.3, 0.4]
n_list = [50, 100, 50, 50, 100, 50]
option_type_list = ["put", "put", "put", "call", "call", "call", "call"]
for i in range(0, 6):
    a = ArithmaticAsianOption(S, 100, sigma_list[i], r, T, n_list[i], option_type_list[i], M, "none")
    print(a.mc_ariasian())
