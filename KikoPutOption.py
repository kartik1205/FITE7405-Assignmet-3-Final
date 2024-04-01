import math
import numpy as np
import pandas as pd
from scipy.stats import norm, qmc


class KIKOOptionPricer:
    def __init__(self, r, sigma, T, s, K, barrier_lower, barrier_upper, N, R, M, seed=1000):
        self.r = r
        self.sigma = sigma
        self.T = T
        self.s = s
        self.K = K
        self.barrier_lower = barrier_lower
        self.barrier_upper = barrier_upper
        self.N = N
        self.R = R
        self.M = M
        self.seed = seed
        self.deltaT = T / N
        np.random.seed(seed)

    def generate_paths(self, s):
        sequencer = qmc.Sobol(d=self.N, seed=self.seed)
        X = np.array(sequencer.random(n=self.M))
        Z = norm.ppf(X)
        samples = (self.r - 0.5 * self.sigma ** 2) * self.deltaT + self.sigma * math.sqrt(self.deltaT) * Z
        df_samples = pd.DataFrame(samples)
        df_samples_cumsum = df_samples.cumsum(axis=1)
        return s * np.exp(df_samples_cumsum)

    def calculate_option_price(self, s):
        df_stocks = self.generate_paths(s)
        values = []
        for ipath in df_stocks.index.to_list():
            ds_path_local = df_stocks.loc[ipath, :]
            price_max = ds_path_local.max()
            price_min = ds_path_local.min()
            if price_max >= self.barrier_upper:
                knockout_time = ds_path_local[ds_path_local >= self.barrier_upper].index.to_list()[0]
                payoff = self.R * np.exp(-knockout_time * self.r * self.deltaT)
                values.append(payoff)
            elif price_min <= self.barrier_lower:
                final_price = ds_path_local.iloc[-1]
                payoff = np.exp(-self.r * self.T) * max(self.K - final_price, 0)
                values.append(payoff)
            else:
                values.append(0)

        value = np.mean(values)
        std = np.std(values)
        conf_interval_lower = value - 1.96 * std / math.sqrt(self.M)
        conf_interval_upper = value + 1.96 * std / math.sqrt(self.M)
        return value, conf_interval_lower, conf_interval_upper

    def calculate_delta(self, epsilon=1.0):
        original_price, _, _ = self.calculate_option_price(self.s)
        new_price, _, _ = self.calculate_option_price(self.s + epsilon)
        delta = (new_price - original_price) / epsilon
        return delta


