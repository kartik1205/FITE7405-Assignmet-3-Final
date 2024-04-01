
from BlackScholes import BlackScholes
from AsianOptionGeo import GeomAsian


S = 100
K = 100
r = 0.05
T = 3
sigma = 0.3
n=50
optionType ="put"

bs = BlackScholes()


parameter = [
    {"sigma":0.3, "n":50, "optionType":"put"},
    {"sigma":0.3, "n":100, "optionType":"put"},
    {"sigma":0.4, "n":50, "optionType":"put"},
    {"sigma":0.3, "n":50, "optionType":"call"},
    {"sigma":0.3, "n":100, "optionType":"call"},
    {"sigma":0.4, "n":50, "optionType":"call"}
]

for params in parameter:
    sigma = params["sigma"]
    n = params["n"]
    optionType = params["optionType"]
    ga = GeomAsian(S,K, T,sigma,r,n,optionType)
    geoAsian_px = ga.closed_form_solution_price()
    print("sigma = %.2f; n = %d; options type = %s; geometric asian option price is %.3f" %(sigma, n, optionType, geoAsian_px))
    vanilla_px = bs.euro_extended(S, K, T, r, 0, sigma, optionType)
    print("Black-Scholes price: %.3f" %vanilla_px)

