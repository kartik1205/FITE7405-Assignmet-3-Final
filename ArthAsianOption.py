##4. Monte Carlo with control variate technique for arithmetic Asian call/put option

import numpy as np
from scipy.stats import norm

np.random.seed(1000)


class ArithmaticAsianOption:
    def __init__(self, S=None, K=None, sigma=None, r=0, T=0, N=100, option_type=None, M=1000, cv_method=None):
        assert option_type.lower() == 'call' or option_type.lower() == 'put'
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r
        self.N = N
        self.M = M
        self.option_type = option_type
        self.cv_method = cv_method

    def mc_ariasian(self):
        S, sigma, r, T, K, N, M, option_type, cv_method = self.S, self.sigma, self.r, self.T, self.K, self.N, self.M, self.option_type, self.cv_method
        Dt = 1e-2
        sigsqT = sigma ** 2 * T * (N + 1) * (2 * N + 1) / (6 * N ** 2)
        muT = 0.5 * sigsqT + (r - 0.5 * sigma ** 2) * T * (N + 1) / (2 * N)

        d1 = (np.log(S / K) + (muT + 0.5 * sigsqT)) / np.sqrt(sigsqT)
        d2 = d1 - np.sqrt(sigsqT)

        N1_call = norm.cdf(d1)
        N2_call = norm.cdf(d2)

        N1_put = norm.cdf(-d1)
        N2_put = norm.cdf(-d2)

        if option_type == "call":
            geo = np.exp(-r * T) * (S * np.exp(muT) * N1_call - K * N2_call)
        elif option_type == "put":
            geo = np.exp(-r * T) * (K * N2_put - S * np.exp(muT) * N1_put)

        drift = np.exp((r - 0.5 * sigma ** 2) * 0.01)

        arithPayoff = np.zeros(M)
        geoPayoff = np.zeros(M)

        for i in range(M):
            growthFactor = drift * np.exp(sigma * np.sqrt(Dt) * np.random.randn())
            Spath = np.zeros(N + 1)
            Spath[0] = S * growthFactor
            for j in range(1, N + 1):
                growthFactor = drift * np.exp(sigma * np.sqrt(Dt) * np.random.randn())
                Spath[j] = Spath[j - 1] * growthFactor

            arithMean = np.mean(Spath)
            arithPayoff[i] = np.exp(-r * T) * max(arithMean - K, 0)

            geoMean = np.exp((1 / N) * np.sum(np.log(Spath)))
            geoPayoff[i] = np.exp(-r * T) * max(geoMean - K, 0)

        Pmean = np.mean(arithPayoff)
        Pstd = np.std(arithPayoff)
        confmc = [Pmean - 1.96 * Pstd / np.sqrt(M), Pmean + 1.96 * Pstd / np.sqrt(M)]

        covXY = np.mean(arithPayoff * geoPayoff) - np.mean(arithPayoff) * np.mean(geoPayoff)
        theta = covXY / np.var(geoPayoff)

        Z = arithPayoff + theta * (geo - geoPayoff)
        Zmean = np.mean(Z)
        Zstd = np.std(Z)
        confcv = [Zmean - 1.96 * Zstd / np.sqrt(M), Zmean + 1.96 * Zstd / np.sqrt(M)]

        if cv_method == "none":
            return confmc
        elif cv_method == "geometric":
            return confcv
        else:
            return "Invalid Method, input either: none or geometric"



