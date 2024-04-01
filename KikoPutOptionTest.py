from KikoPutOption import KIKOOptionPricer
import pandas as pd
# Parameters
r = 0.05
sigma = 0.20
T = 2.0
s = 100
K = 100
barrier_lower = 80
barrier_upper = 125
N = 24
R = 1.5
M = int(1e2)
seed = 1000


test_cases_basket = {'K':[100, 100, 100, 80, 120, 100, 100, 100, 100, 80, 120, 100],
                     'sigma1': [0.3, 0.3, 0.1, 0.3, 0.3, 0.5, 0.3, 0.3, 0.1, 0.3, 0.3, 0.5],
                     'sigma2': [0.3, 0.3, 0.3, 0.3, 0.3, 0.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.5],
                     'rho': [0.5, 0.9, 0.5, 0.5, 0.5, 0.5, 0.5, 0.9, 0.5, 0.5, 0.5, 0.5]}
TC_basket = pd.DataFrame(test_cases_basket)

for index, row in TC_basket.iterrows():
    sigma = row['sigma1']
    K = row['K']
    # Create an instance of the KIKOOptionPricer class
    pricer = KIKOOptionPricer(r, sigma, T, s, K, barrier_lower, barrier_upper, N, R, M, seed)

    # Calculate the option price and its Delta
    option_price, conf_lower, conf_upper = pricer.calculate_option_price(s)
    delta = pricer.calculate_delta()

    # Print the results
    print(f'The option price: {option_price:.4f}')
    print(f'95% confidence interval: [{conf_lower:.4f}, {conf_upper:.4f}]')
    print(f'The Delta of the option: {delta:.4f}')



