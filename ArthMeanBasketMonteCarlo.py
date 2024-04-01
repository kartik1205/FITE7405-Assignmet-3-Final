###m 5. Monte Carlo method with control variate technique for arithmetic mean basket call/put options
import numpy as np
from scipy.stats import norm


class MonteCarloArtBasket:

    def __init__(self, S1=None, S2=None, K=None, T=0.0, sigma1=None, sigma2=None, r=0.0, rho=None, N = None, M=10 ** 5,
                 optionType=None, cv_method=None):
        assert optionType.lower() == 'call' or optionType.lower() == 'put'
        self.S1 = S1
        self.S2 = S2
        self.K = K
        self.T = T
        self.sigma1 = sigma1
        self.sigma2 = sigma2
        self.r = r
        self.rho = rho
        self.M = M
        self.N = N
        self.optionType = optionType
        self.cv_method = cv_method

    def mc_ariasian_basket(self):
        S1, S2, sigma1, sigma2, r, T, K, N, M, rho, option_type, cv_method = self.S1, self.S2, self.sigma1, self.sigma2, self.r, self.T, self.K, self.N, self.M, self.rho, self.optionType, self.cv_method
        Dt = T / N

        sigma_B = np.sqrt(sigma1 ** 2 + 2 * sigma1 * sigma2 * rho + sigma2 ** 2) / 2
        muT = r - 0.5 * ((sigma1 ** 2 + sigma2 ** 2) / 2) + 0.5 * sigma_B ** 2
        Bg = np.sqrt(S1 * S2)
        d1 = (np.log(Bg / K) + (muT + 0.5 * sigma_B ** 2) * T) / (sigma_B * np.sqrt(T))
        d2 = d1 - sigma_B * np.sqrt(T)

        if (option_type.lower() == 'call'):
            geo_basket = np.exp(-r * T) * (Bg * np.exp(muT) * norm.cdf(d1) - K * norm.cdf(d2))

        elif option_type.lower() == "put":
            geo_basket = np.exp(-r * T) * (K * norm.cdf(-d2) - Bg * np.exp(muT) * norm.cdf(-d1))

        drift_1 = np.exp((r - 0.5 * sigma1 ** 2) * 0.01)
        drift_2 = np.exp((r - 0.5 * sigma2 ** 2) * 0.01)

        arithPayoff = np.zeros(M)
        geoPayoff = np.zeros(M)

        for i in range(M):
            growthFactor1 = drift_1 * np.exp(sigma1 * np.sqrt(Dt) * np.random.randn())
            growthFactor2 = drift_2 * np.exp(sigma2 * np.sqrt(Dt) * np.random.randn())

            Spath1 = np.zeros(N + 1)
            Spath2 = np.zeros(N + 1)

            Spath1[0] = S1 * growthFactor1
            Spath2[0] = S2 * growthFactor2

            for j in range(1, N + 1):
                growthFactor1 = drift_1 * np.exp(sigma1 * np.sqrt(Dt) * np.random.randn())
                growthFactor2 = drift_2 * np.exp(sigma2 * np.sqrt(Dt) * np.random.randn())

                Spath1[j] = Spath1[j - 1] * growthFactor1
                Spath2[j] = Spath2[j - 1] * growthFactor2

            arithMean = (np.mean(Spath1) + np.mean(Spath2)) / 2
            arithPayoff[i] = np.exp(-r * T) * max(arithMean - K, 0)

            geoMean = (np.exp((1 / N) * np.sum(np.log(Spath1))) + np.exp((1 / N) * np.sum(np.log(Spath2)))) / 2
            geoPayoff[i] = np.exp(-r * T) * max(geoMean - K, 0)

        Pmean = np.mean(arithPayoff)
        Pstd = np.std(arithPayoff)
        confmc = [Pmean - 1.96 * Pstd / np.sqrt(M), Pmean + 1.96 * Pstd / np.sqrt(M)]

        covXY = np.mean(arithPayoff * geoPayoff) - np.mean(arithPayoff) * np.mean(geoPayoff)
        theta = covXY / np.var(geoPayoff)

        Z = arithPayoff + theta * (geo_basket - geoPayoff)
        Zmean = np.mean(Z)
        Zstd = np.std(Z)
        confcv = [Zmean - 1.96 * Zstd / np.sqrt(M), Zmean + 1.96 * Zstd / np.sqrt(M)]

        if cv_method == "none":
            return confmc
        elif cv_method == "geometric":
            return confcv
        else:
            return "Invalid Method, input either: none or geometric"


S1 = 100  # Initial price of asset 1
S2 = 120  # Initial price of asset 2
sigma1 = 0.2  # Volatility of asset 1
sigma2 = 0.3  # Volatility of asset 2
r = 0.05  # Risk-free interest rate
T = 1.0  # Time to expiration
K = 110  # Strike price
rho = 0.5  # Correlation between the assets
M = 1000  # Number of Monte Carlo simulations
N = 100

a = MonteCarloArtBasket(100, 120, K, T, 0.2, 0.3, r, rho,N, M, 'call', 'none')

# print(f"No Control Variate Basket Call: {mc_ariasian_basket(S1, S2, sigma1, sigma2, r, T, K, N, M, rho, 'call', 'none')}")
# print(f"No Control Variate Basket Put: {mc_ariasian_basket(S1, S2, sigma1, sigma2, r, T, K, N, M, rho, 'put', 'none')}")
# print(f"Geometric Asian Option Basket Call : {mc_ariasian_basket(S1, S2, sigma1, sigma2, r, T, K, N, M, rho, 'call', 'geometric')}")
# print(f"Geometric Asian Option Basket Put: {mc_ariasian_basket(S1, S2, sigma1, sigma2, r, T, K, N, M, rho, 'put', 'geometric')}")
