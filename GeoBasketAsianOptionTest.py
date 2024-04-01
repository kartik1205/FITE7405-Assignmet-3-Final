from GeoBasketAsianOption import GeomBasket
import pandas as pd

S1 = 100
S2 = 100
r = 0.05
T = 3

test_cases_basket = {'K':[100, 100, 100, 80, 120, 100, 100, 100, 100, 80, 120, 100],
                     'sigma1': [0.3, 0.3, 0.1, 0.3, 0.3, 0.5, 0.3, 0.3, 0.1, 0.3, 0.3, 0.5],
                     'sigma2': [0.3, 0.3, 0.3, 0.3, 0.3, 0.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.5],
                     'rho': [0.5, 0.9, 0.5, 0.5, 0.5, 0.5, 0.5, 0.9, 0.5, 0.5, 0.5, 0.5],
                     'optionType':['Put','Put','Put','Put','Put','Put','Call','Call','Call','Call','Call','Call']}

TC_basket = pd.DataFrame(test_cases_basket)
gb = GeomBasket()

for index, row in TC_basket.iterrows():
    sigma1 = row['sigma1']
    sigma2 = row['sigma2']
    K = row['K']
    rho = row['rho']
    optionType = row['optionType']
    geoBasket_px = gb.closed_form_solution_price(S1, S2, sigma1, sigma2, K, r, T, rho, optionType)
    print("If sigma1 = %.2f; sigma2 = %.2f; rho = %.2f; K = %d; options = %s; geometric basket option price = %.3f" % (sigma1, sigma2, rho, K, optionType, geoBasket_px))