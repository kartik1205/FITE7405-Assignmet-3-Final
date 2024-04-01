from ArthMeanBasketMonteCarlo import MonteCarloArtBasket

S1 = 100  # Initial price of asset 1
S2 = 120  # Initial price of asset 2
sigma1 = 0.2  # Volatility of asset 1
sigma2 = 0.3  # Volatility of asset 2
r = 0.05  # Risk-free interest rate
T = 3  # Time to expiration

rho = 0.5  # Correlation between the assets
M = 100000  # Number of Monte Carlo simulations
N = 100
k_list = [100, 100, 100, 80, 120, 100, 100, 100, 100, 80, 120, 100]
sigma1_list = [0.3, 0.3, 0.1, 0.3, 0.3, 0.5, 0.3, 0.3, 0.1, 0.3, 0.3, 0.5]
sigma2_list = [0.3, 0.3, 0.3, 0.3, 0.3, 0.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.5]

rho_list = [0.5, 0.9, 0.5, 0.5, 0.5, 0.5, 0.5, 0.9, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

option_type_list = ['put', 'put', 'put', 'put', 'put', 'put', 'call', 'call', 'call', 'call', 'call', 'call']

for i in range(0, 12):
    a = MonteCarloArtBasket(100, 100, k_list[i], T, sigma1_list[i], sigma2_list[i], r, rho_list[i], N, M,
                            option_type_list[i], 'none')
    print(f"No Control Variate Basket {option_type_list[i]}: {a.mc_ariasian_basket()}")

for i in range(0, 12):
    a = MonteCarloArtBasket(100, 100, k_list[i], T, sigma1_list[i], sigma2_list[i], r, rho_list[i], N, M,
                            option_type_list[i], 'geometric')
    print(f"Geometric Asian Option Basket {option_type_list[i]} : {a.mc_ariasian_basket()}")
