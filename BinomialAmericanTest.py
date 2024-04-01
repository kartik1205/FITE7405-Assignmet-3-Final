from BinomialTreeAmericanOption import AmericanOption

S = 50
K = 40
sigma = 0.4
r = 0.1
T = 2
N = 200
optionType = "Put"

k_list = [100, 100, 100, 80, 120, 100, 100, 100, 100, 80, 120, 100]
sigma1_list = [0.3, 0.3, 0.1, 0.3, 0.3, 0.5, 0.3, 0.3, 0.1, 0.3, 0.3, 0.5]
option_type_list = ['put', 'put', 'put', 'put', 'put', 'put', 'call', 'call', 'call', 'call', 'call', 'call']

rho_list = [0.5, 0.9, 0.5, 0.5, 0.5, 0.5, 0.5, 0.9, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

for i in range(0, 12):
    a = AmericanOption(50, 40, 3, sigma1_list[i], 0.05, 200, option_type_list[i])
    american_px = a.bi_tree_pricing()
    print("American vanilla price is: %.5f" % american_px)
