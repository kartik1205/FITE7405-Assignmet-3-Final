import math
from math import sqrt, pi, pow
from scipy.stats import norm
from datetime import datetime
import numpy as np
from numpy import log as ln, exp, mean, std, var
import numpy as np
from numpy import log as ln, sqrt, exp
from math import fabs
import pandas as pd


def n_func(d):
    return norm.cdf(d)


def n_prime(d):
    return exp(-pow(d, 2) / 2) * (1 / sqrt(2 * pi))


# 1. Implement Black-Scholes Formulas for European call/put options.
class BlackScholes:
    def __init__(self):
        pass

    def cal_d1(self, S, K, T_t, r, q, sigma):
        return ((ln(S / K) + (r - q) * T_t) / (sigma * sqrt(T_t))) + ((1 / 2) * sigma * sqrt(T_t))

    def cal_d2(self, S, K, T_t, r, q, sigma):
        return ((ln(S / K) + (r - q) * T_t) / (sigma * sqrt(T_t))) - ((1 / 2) * sigma * sqrt(T_t))

    def c(self, S, K, T_t, r, q, sigma):
        d1 = self.cal_d1(S, K, T_t, r, q, sigma)
        d2 = self.cal_d2(S, K, T_t, r, q, sigma)
        return S * exp(-q * T_t) * n_func(d1) - K * exp(-r * T_t) * n_func(d2)

    def p(self, S, K, T_t, r, q, sigma):
        d1 = self.cal_d1(S, K, T_t, r, q, sigma)
        d2 = self.cal_d2(S, K, T_t, r, q, sigma)
        return -S * exp(-q * T_t) * n_func(-d1) + K * exp(-r * T_t) * n_func(-d2)

    def call_put_parity(self, S, K, T_t, r, q):
        return S * exp(-q * T_t) - K * exp(-r * T_t)

    def euro_extended(self, S, K, T_t, r, q, sigma, optionType):
        if optionType.lower() == 'call':
            return self.c(S, K, T_t, r, q, sigma)
        return self.p(S, K, T_t, r, q, sigma)

    def vega(self, S, K, T_t, r, q, sigma):
        d1 = self.cal_d1(S, K, T_t, r, q, sigma)
        return S * exp(-q * T_t) * sqrt(T_t) * n_prime(d1)

    def guess_initial_sigma(self, S, K, T_t, r, q):
        return sqrt(2*fabs((ln(S/K) + (r-q)*T_t)/T_t))

    def get_implied_volatility(self, S, K, T_t, r, q, optionType, O_fair):
        if optionType.lower() == 'call':
            lower_boundary = max(S*exp(-q*T_t) - K*exp(-r*T_t), 0)
            upper_boundary = S*exp(-q*T_t)
        else:
            lower_boundary = max(K*exp(-r*T_t) - S*exp(-q*T_t), 0)
            upper_boundary = K*exp(-r*T_t)

        if O_fair > upper_boundary or O_fair < lower_boundary:
            return np.NaN

        sigmahat = self.guess_initial_sigma(S, K, T_t, r, q)

        tol = 1e-8; nmax = 100
        sigmadiff = 1
        n = 1
        sigma = sigmahat
        bs = BlackScholes()

        while (sigmadiff >= tol and n < nmax):
            O = bs.euro_extended(S, K, T_t, r, q, sigma, optionType)
            Ovega = bs.vega(S, K, T_t, r, q, sigma)
            if(fabs(Ovega) < tol):
                return np.NaN
            increment = (O - O_fair) / Ovega
            sigma = sigma - increment
            n = n + 1
            sigmadiff = abs(increment)
        return sigma

# S = 100
# K = 100
# sigma = 0.3
# r = 0.05
# T_t = 3
# q = 0.00
# bs = BlackScholes()
# print(bs.euro_extended(S, K, T_t, r, q, sigma, "Call"))
