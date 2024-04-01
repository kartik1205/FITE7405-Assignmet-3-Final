from tkinter import *
import tkinter.font as tkFont
from tkinter import scrolledtext
import KikoPutOption
from BlackScholes import BlackScholes
from GeoBasketAsianOption import GeomBasket
from ArthAsianOption import ArithmaticAsianOption
from ArthMeanBasketMonteCarlo import MonteCarloArtBasket
from BinomialTreeAmericanOption import AmericanOption
from AsianOptionGeo import GeomAsian


class OptionPricer:
    def __init__(self):
        self.s = None
        self.R = None
        self.seed = None
        self.barrier_upper = None
        self.barrier_lower = None
        self.q = None
        self.O_fair = None
        self.control_variate = None
        self.S2 = None
        self.S1 = None
        self.sigma2 = None
        self.M = None
        self.rho = None
        self.sigma1 = None
        self.N = None
        self.output = None
        self.option_type = None
        self.n = None
        self.T = None
        self.r = None
        self.sigma = None
        self.K = None
        self.S = None
        self.gui = Tk()
        self.gui.title("Option models")
        self.gui.geometry('%dx%d' % (1000, 600))
        self.menu = Menu(self.gui)
        self.gui.config(menu=self.menu)
        self.gui.configure(bg="black")
        self.mainPage()
        self.CreateOptionMenu()
        self.mainPage = Frame(self.gui)
        self.info = Frame(self.gui)
        self.kikoGui = Frame(self.gui)
        self.blackScholesGui = Frame(self.gui)
        self.geoAsianGui = Frame(self.gui)
        self.geoBasketGui = Frame(self.gui)
        self.arthAsian = Frame(self.gui)
        self.arthBasket = Frame(self.gui)
        self.american = Frame(self.gui)
        self.impVol = Frame(self.gui)
        self.tearDown()
        self.mainPage.pack()

        # Main page
        Label(self.mainPage, text="FITE7405: Assignment 3", bg="black", fg="white",
              font=tkFont.Font(weight='bold', size=50), height=6).pack()
        Label(self.mainPage, text='Option Pricer',
              font=tkFont.Font(weight='bold', size=25)).pack()

        Label(self.info, text="Info", font=tkFont.Font(weight='bold', size=50), height=5).pack()
        Label(self.info, text="Authors: Kartikeya Misra, Leo, Keith", font=tkFont.Font(weight='bold', size=30),
              height=5).pack()

        self.gui.mainloop()

    def CreateOptionMenu(self):
        dropdownItems = Menu(self.menu, tearoff=0)
        dropdownItems.add_command(label="Black Scholes", command=self.blackScholesUI)
        dropdownItems.add_command(label="Geometric Asian", command=self.calc_asian_option_geo)
        dropdownItems.add_command(label="Geometric Basket", command=self.AsianGeoBasket)
        dropdownItems.add_command(label="Arithmetic Asian", command=self.ArthAsianOption)
        dropdownItems.add_command(label="Arithmetic Basket", command=self.calc_arth_basket_monte_carlo)
        dropdownItems.add_command(label="American", command=self.calc_binomial_american_option)
        dropdownItems.add_command(label="Implied Volatility", command=self.implied_volatility_gui)
        dropdownItems.add_command(label="KIKO Put", command=self.kikoPut)
        self.menu.add_cascade(label='Pricing Models', menu=dropdownItems)

    def mainPage(self):
        homemenu = Menu(self.menu, tearoff=0)
        homemenu.add_command(label="Load Homepage", command=self.loadMainPage)
        homemenu.add_command(label="Info", command=self.infoPage)
        homemenu.add_command(label="Exit", command=self.exit)
        self.menu.add_cascade(label='Menu', menu=homemenu)

    def infoPage(self):
        self.tearDown()
        self.info.pack()

    def loadMainPage(self):
        self.tearDown()
        self.mainPage.pack()

    def exit(self):
        self.gui.destroy()

    def tearDown(self):
        self.mainPage.pack_forget()
        self.impVol.pack_forget()
        self.info.pack_forget()
        self.kikoGui.pack_forget()
        self.blackScholesGui.pack_forget()
        self.geoAsianGui.pack_forget()
        self.geoBasketGui.pack_forget()
        self.arthAsian.pack_forget()
        self.arthBasket.pack_forget()
        self.american.pack_forget()

    def calc_asian_option_geo(self):
        self.tearDown()
        screen = self.geoAsianGui
        screen.pack()
        # preare the UI
        Label(screen, text="Geometric Asian Call or Put Option Pricer",
              font=tkFont.Font(size=11, weight='bold')).grid(row=1, column=1, sticky=W)
        Label(screen, text='Spot:').grid(row=2, column=1, sticky=W)
        Label(screen, text='Strike:').grid(row=3, column=1, sticky=W)
        Label(screen, text='Volatility:').grid(row=4, column=1, sticky=W)
        Label(screen, text='Risk Free Rate:').grid(row=5, column=1, sticky=W)
        Label(screen, text='Time to Maturity:').grid(row=6, column=1, sticky=W)
        Label(screen, text='Value of N:').grid(row=7, column=1, sticky=W)
        Label(screen, text='Option Type: Call or Put').grid(row=8, column=1, sticky=W)

        self.S = StringVar()
        self.K = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.n = StringVar()
        self.option_type = StringVar()

        Entry(screen, textvariable=self.S).grid(row=2, column=2, sticky=W)
        Entry(screen, textvariable=self.K).grid(row=3, column=2, sticky=W)
        Entry(screen, textvariable=self.sigma).grid(row=4, column=2, sticky=W)
        Entry(screen, textvariable=self.r).grid(row=5, column=2, sticky=W)
        Entry(screen, textvariable=self.T).grid(row=6, column=2, sticky=W)
        Entry(screen, textvariable=self.n).grid(row=7, column=2, sticky=W)
        # select either Put or Call
        Radiobutton(screen, text="Put", variable=self.option_type, value='put').grid(row=8, column=2, sticky=E)
        Radiobutton(screen, text="Call", variable=self.option_type, value='call').grid(row=8, column=2, sticky=W)

        Button(screen, width=20, text="Reset", command=self.reset_asian_option_geo).grid(row=10, column=1,
                                                                                         columnspan=1,
                                                                                         sticky=E)
        Button(screen, width=20, text="Compute", command=self.get_asian_option_geo).grid(row=10, column=2,
                                                                                         columnspan=1,
                                                                                         sticky=W)

        self.output = scrolledtext.ScrolledText(screen, width=74, height=8)
        self.output.grid(row=11, column=1, rowspan=4, columnspan=2, sticky=W)

    def reset_asian_option_geo(self):
        self.S = 0
        self.K = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.n = 0
        self.calc_asian_option_geo()

    # get the asian option price after computing the result
    def get_asian_option_geo(self):
        try:
            bs = BlackScholes()

            option = GeomAsian(float(self.S.get()), float(self.K.get()), float(self.T.get()), float(self.sigma.get()),
                               float(self.r.get()), int(self.n.get()), self.option_type.get())
            result = option.closed_form_solution_price()

            bsResult = bs.euro_extended(float(self.S.get()), float(self.K.get()), float(self.T.get()),
                                        float(self.r.get()), 0, float(self.sigma.get()), self.option_type.get())
            self.output.insert(END, "Geometric asian option price is: {}\n".format(result))
            self.output.insert(END, "Black-Scholes price:  {}\n".format(bsResult))

        except Exception as e:
            self.output.insert(END, "Error in calculating the price\n")
            self.output.insert(END, repr(e))

            print('Error %s', repr(e))

    def calc_binomial_american_option(self):
        self.tearDown()
        frame = self.american
        frame.pack()

        Label(frame, text="The Binomial Tree method for American call/put options.",
              font=tkFont.Font(size=11, weight='bold')).grid(row=1, column=1, sticky=W)
        Label(frame, text='Spot').grid(row=2, column=1, sticky=W)
        Label(frame, text='Strike ').grid(row=3, column=1, sticky=W)
        Label(frame, text='Volatility').grid(row=4, column=1, sticky=W)
        Label(frame, text='Risk Free Rate (r)').grid(row=5, column=1, sticky=W)
        Label(frame, text='Time to Maturity').grid(row=6, column=1, sticky=W)
        Label(frame, text='Number of Steps').grid(row=7, column=1, sticky=W)
        Label(frame, text='Option Type: Call or Put').grid(row=8, column=1, sticky=W)

        self.S = StringVar()
        self.K = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.N = StringVar()
        self.option_type = StringVar()

        Entry(frame, textvariable=self.S).grid(row=2, column=2, sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3, column=2, sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=4, column=2, sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5, column=2, sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6, column=2, sticky=W)
        Entry(frame, textvariable=self.N).grid(row=7, column=2, sticky=W)

        Radiobutton(frame, text="Put", variable=self.option_type, value='put').grid(row=8, column=2, sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='call').grid(row=8, column=2, sticky=W)

        Button(frame, width=20, text="Reset", command=self.reset_binomial).grid(row=10, column=1, columnspan=1,
                                                                                sticky=E)

        Button(frame, width=20, text="Compute", command=self.get_binomial_american).grid(row=10, column=2,
                                                                                         columnspan=1,
                                                                                         sticky=W)
        self.output = scrolledtext.ScrolledText(frame, width=74, height=8)
        self.output.grid(row=11, column=1, rowspan=4, columnspan=2, sticky=W)

    def reset_binomial(self):
        self.S = 0
        self.K = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.N = 0
        self.calc_binomial_american_option()

    def get_binomial_american(self):
        try:
            option = AmericanOption(float(self.S.get()), float(self.K.get()), float(self.T.get()),
                                    float(self.sigma.get()),
                                    float(self.r.get()), int(self.N.get()), self.option_type.get())
            result = option.bi_tree_pricing()
            self.output.insert(END, "Result: {}\n".format(result))
        except Exception as e:
            self.output.insert(END, "Error in calculating the price\n")
            self.output.insert(END, repr(e))

            print('Error %s', repr(e))

    def calc_arth_basket_monte_carlo(self):
        self.tearDown()
        frame = self.arthBasket
        frame.pack()

        Label(frame,
              text="Monte Carlo method with control variate technique for arithmetic mean basket call/put options",
              font=tkFont.Font(size=11, weight='bold')).grid(row=1, column=1, sticky=W)
        Label(frame, text='Spot Price of 1st Asset').grid(row=2, column=1, sticky=W)
        Label(frame, text='Spot Price of 2nd Asset').grid(row=3, column=1, sticky=W)
        Label(frame, text='Strike Price').grid(row=4, column=1, sticky=W)
        Label(frame, text='Volatility of 1st asset').grid(row=5, column=1, sticky=W)
        Label(frame, text='Volatility of 2nd asset').grid(row=6, column=1, sticky=W)
        Label(frame, text='Risk Free Rate').grid(row=7, column=1, sticky=W)
        Label(frame, text='Time to Maturity (in years)').grid(row=8, column=1, sticky=W)
        Label(frame, text='Correlation between Assets').grid(row=9, column=1, sticky=W)
        Label(frame, text='Number of Paths in Monte Carlo').grid(row=10, column=1, sticky=W)
        Label(frame, text='Number of Observation Times').grid(row=11, column=1, sticky=W)
        Label(frame, text='Use Control Variate').grid(row=12, column=1, sticky=W)
        Label(frame, text='Option Type: Call or Put').grid(row=13, column=1, sticky=W)

        self.S1 = StringVar()
        self.S2 = StringVar()
        self.K = StringVar()
        self.sigma1 = StringVar()
        self.sigma2 = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.rho = StringVar()
        self.M = StringVar()
        self.N = StringVar()
        self.control_variate = StringVar()
        self.option_type = StringVar()

        Entry(frame, textvariable=self.S1).grid(row=2, column=2, sticky=W)
        Entry(frame, textvariable=self.S2).grid(row=3, column=2, sticky=W)
        Entry(frame, textvariable=self.K).grid(row=4, column=2, sticky=W)
        Entry(frame, textvariable=self.sigma1).grid(row=5, column=2, sticky=W)
        Entry(frame, textvariable=self.sigma2).grid(row=6, column=2, sticky=W)
        Entry(frame, textvariable=self.r).grid(row=7, column=2, sticky=W)
        Entry(frame, textvariable=self.T).grid(row=8, column=2, sticky=W)
        Entry(frame, textvariable=self.rho).grid(row=9, column=2, sticky=W)
        Entry(frame, textvariable=self.M).grid(row=10, column=2, sticky=W)
        Entry(frame, textvariable=self.N).grid(row=11, column=2, sticky=W)

        Radiobutton(frame, text="None", variable=self.control_variate, value='none').grid(row=12, column=2, sticky=E)
        Radiobutton(frame, text="Geometric", variable=self.control_variate, value='geometric').grid(row=12, column=2,
                                                                                                    sticky=W)

        Radiobutton(frame, text="Put", variable=self.option_type, value='put').grid(row=13, column=2, sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='call').grid(row=13, column=2, sticky=W)

        Button(frame, width=20, text="Reset", command=self.reset_mean_basket_monte_carlo).grid(row=14, column=1,
                                                                                                      columnspan=1,
                                                                                                      sticky=E)

        Button(frame, width=20, text="Compute", command=self.get_arth_mean_basket_monte_carlo).grid(row=14, column=2,
                                                                                                      columnspan=1,
                                                                                                      sticky=W)

        self.output = scrolledtext.ScrolledText(frame, width=74, height=8)
        self.output.grid(row=15, column=1, rowspan=4, columnspan=2, sticky=W)

    def reset_mean_basket_monte_carlo(self):
        self.S1 = 0
        self.S2 = 0
        self.K = 0
        self.sigma1 = 0
        self.sigma2 = 0
        self.r = 0
        self.T = 0
        self.rho = 0
        self.M = 0
        self.N = 0
        self.calc_arth_basket_monte_carlo()

    def get_arth_mean_basket_monte_carlo(self):
        try:
            option = MonteCarloArtBasket(float(self.S1.get()), float(self.S2.get()), float(self.K.get()),
                                         float(self.T.get()),
                                         float(self.sigma1.get()), float(self.sigma2.get()), float(self.r.get()),
                                         float(self.rho.get()), int(self.N.get()), int(self.M.get()),
                                         self.option_type.get(),
                                         self.control_variate.get())
            result = option.mc_ariasian_basket()

            self.output.insert(END, "The Option Price is: {}\n".format(result))
        except Exception as e:
            self.output.insert(END, "Error in calculating the price\n")
            self.output.insert(END, repr(e))

            print('Error %s', repr(e))

    def ArthAsianOption(self):
        self.tearDown()
        frame = self.arthAsian
        frame.pack()

        Label(frame, text="Price for Arithmetic Asian Call/Put Options", font=tkFont.Font(size=11, weight='bold')).grid(
            row=1, column=1, sticky=W)
        Label(frame, text="Standard Monte Carlo or Control Variate Method").grid(row=1, column=2)
        Label(frame, text='Spot Price').grid(row=2, column=1, sticky=W)
        Label(frame, text='Strike Price').grid(row=3, column=1, sticky=W)
        Label(frame, text='Volatility').grid(row=4, column=1, sticky=W)
        Label(frame, text='Risk Free Rate').grid(row=5, column=1, sticky=W)
        Label(frame, text='Time to Maturity (in years)').grid(row=6, column=1, sticky=W)
        Label(frame, text='Number of Observation Times').grid(row=7, column=1, sticky=W)
        Label(frame, text='Number of Paths in Monte Carlo').grid(row=8, column=1, sticky=W)
        Label(frame, text='Use Control Variate').grid(row=9, column=1, sticky=W)
        Label(frame, text='Option Type: Call or Put').grid(row=10, column=1, sticky=W)

        self.S = StringVar()
        self.K = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.n = StringVar()
        self.M = StringVar()
        self.control_variate = StringVar()
        self.option_type = StringVar()

        Entry(frame, textvariable=self.S).grid(row=2, column=2, sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3, column=2, sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=4, column=2, sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5, column=2, sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6, column=2, sticky=W)
        Entry(frame, textvariable=self.n).grid(row=7, column=2, sticky=W)
        Entry(frame, textvariable=self.M).grid(row=8, column=2, sticky=W)

        Radiobutton(frame, text="None", variable=self.control_variate, value='none').grid(row=9, column=2, sticky=E)
        Radiobutton(frame, text="Geometric", variable=self.control_variate, value='geometric').grid(row=9, column=2,
                                                                                                    sticky=W)
        Radiobutton(frame, text="Put", variable=self.option_type, value='put').grid(row=10, column=2, sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='call').grid(row=10, column=2, sticky=W)

        Button(frame, width=20, text="Reset Inputs", command=self.reset_arth_asian_option).grid(row=11, column=1,
                                                                                                columnspan=1,
                                                                                                sticky=E)

        Button(frame, width=20, text="Calculate", command=self.get_arth_asian_option).grid(row=11, column=2,
                                                                                           columnspan=1,
                                                                                           sticky=W)

        self.output = scrolledtext.ScrolledText(frame, width=74, height=8)
        self.output.grid(row=12, column=1, rowspan=4, columnspan=2, sticky=W)

    def reset_arth_asian_option(self):
        self.S = 0
        self.K = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.n = 0
        self.M = 0
        self.ArthAsianOption()

    def get_arth_asian_option(self):
        try:

            option = ArithmaticAsianOption(float(self.S.get()), float(self.K.get()), float(self.sigma.get()),
                                           float(self.r.get()), float(self.T.get()), int(self.n.get()),
                                           self.option_type.get(), int(self.M.get()),
                                           self.control_variate.get())
            result = option.mc_ariasian()

            self.output.insert(END, "Result: {}\n".format(result))
        except Exception as e:
            self.output.insert(END, "Error in calculating the price\n")
            self.output.insert(END, repr(e))

            print('Error %s', repr(e))

    def AsianGeoBasket(self):
        self.tearDown()
        frame = self.geoBasketGui
        frame.pack()

        Label(frame, text="Asian geometric basket",
              font=tkFont.Font(size=12, weight='bold')).grid(row=1, column=1, sticky=W)
        Label(frame, text='Spot Price of 1st Asset').grid(row=2, column=1, sticky=W)
        Label(frame, text='Spot Price of 2nd Asset').grid(row=3, column=1, sticky=W)
        Label(frame, text='Strike Price').grid(row=4, column=1, sticky=W)
        Label(frame, text='Volatility of 1st asset').grid(row=5, column=1, sticky=W)
        Label(frame, text='Volatility of 2nd asset').grid(row=6, column=1, sticky=W)
        Label(frame, text='Risk Free Rate').grid(row=7, column=1, sticky=W)
        Label(frame, text='Time to Maturity (in years)').grid(row=8, column=1, sticky=W)
        Label(frame, text='Correlation between Assets').grid(row=9, column=1, sticky=W)
        Label(frame, text='Option Type: Call or Put').grid(row=10, column=1, sticky=W)

        self.S1 = StringVar()
        self.S2 = StringVar()
        self.K = StringVar()
        self.sigma1 = StringVar()
        self.sigma2 = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.rho = StringVar()
        self.option_type = StringVar()

        Entry(frame, textvariable=self.S1).grid(row=2, column=2, sticky=W)
        Entry(frame, textvariable=self.S2).grid(row=3, column=2, sticky=W)
        Entry(frame, textvariable=self.K).grid(row=4, column=2, sticky=W)
        Entry(frame, textvariable=self.sigma1).grid(row=5, column=2, sticky=W)
        Entry(frame, textvariable=self.sigma2).grid(row=6, column=2, sticky=W)
        Entry(frame, textvariable=self.r).grid(row=7, column=2, sticky=W)
        Entry(frame, textvariable=self.T).grid(row=8, column=2, sticky=W)
        Entry(frame, textvariable=self.rho).grid(row=9, column=2, sticky=W)

        Radiobutton(frame, text="Put", variable=self.option_type, value='put').grid(row=10, column=2, sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='call').grid(row=10, column=2, sticky=W)

        Button(frame, width=20, text="Reset", command=self.reset_geo_basket_asian).grid(row=11, column=1,
                                                                                               columnspan=1,
                                                                                               sticky=E)

        Button(frame, width=20, text="Compute", command=self.get_asian_get_basket).grid(row=11, column=2,
                                                                                          columnspan=1,
                                                                                          sticky=W)

        self.output = scrolledtext.ScrolledText(frame, width=74, height=8)
        self.output.grid(row=13, column=1, rowspan=4, columnspan=2, sticky=W)

    def reset_geo_basket_asian(self):
        self.S1 = 0
        self.S2 = 0
        self.K = 0
        self.sigma1 = 0
        self.sigma2 = 0
        self.r = 0
        self.T = 0
        self.rho = 0
        self.AsianGeoBasket()

    def get_asian_get_basket(self):
        try:
            gb = GeomBasket
            result = gb.closed_form_solution_price(gb, float(self.S1.get()), float(self.S2.get()),
                                                   float(self.sigma1.get()),
                                                   float(self.sigma2.get()),
                                                   float(self.K.get()),
                                                   float(self.r.get()),
                                                   float(self.T.get()),
                                                   float(self.rho.get()),
                                                   self.option_type.get())
            self.output.insert(END, "Geometric basket option price: {}\n".format(result))
        except Exception as e:
            self.output.insert(END, "Error in calculating the price\n")
            self.output.insert(END, repr(e))

            print('Error %s', repr(e))

    def implied_volatility_gui(self):
        self.tearDown()
        frame = self.impVol
        frame.pack()

        Label(frame, text="Implied Volatility", font=tkFont.Font(size=11, weight='bold')).grid(row=1,
                                                                                               column=1,
                                                                                               sticky=W)
        Label(frame, text='Spot Price').grid(row=2, column=1, sticky=W)
        Label(frame, text='Strike Price').grid(row=3, column=1, sticky=W)
        Label(frame, text='Option Fair price').grid(row=4, column=1, sticky=W)
        Label(frame, text='Risk Free Rate').grid(row=5, column=1, sticky=W)
        Label(frame, text='Time to Maturity (in years)').grid(row=6, column=1, sticky=W)
        Label(frame, text='Repo Rate').grid(row=7, column=1, sticky=W)
        Label(frame, text='Option Type: Call or Put').grid(row=8, column=1, sticky=W)

        self.S = StringVar()
        self.K = StringVar()
        self.O_fair = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.q = StringVar()
        self.option_type = StringVar()

        Entry(frame, textvariable=self.S).grid(row=2, column=2, sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3, column=2, sticky=W)
        Entry(frame, textvariable=self.O_fair).grid(row=4, column=2, sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5, column=2, sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6, column=2, sticky=W)
        Entry(frame, textvariable=self.q).grid(row=7, column=2, sticky=W)

        Radiobutton(frame, text="Put", variable=self.option_type, value='Put').grid(row=8, column=2, sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='Call').grid(row=8, column=2, sticky=W)

        Button(frame, width=20, text="Reset", command=self.reset_implied_volatility).grid(row=10, column=1,
                                                                                                 columnspan=1,
                                                                                                 sticky=E)

        Button(frame, width=20, text="Compute", command=self.get_implied_volatility).grid(row=10, column=2,
                                                                                            columnspan=1,
                                                                                            sticky=W)

        self.output = scrolledtext.ScrolledText(frame, width=74, height=8)
        self.output.grid(row=11, column=1, rowspan=4, columnspan=2, sticky=W)

    def reset_implied_volatility(self):
        self.S = 0
        self.K = 0
        self.option_price = 0.0
        self.r = 0
        self.T = 0
        self.q = 0
        self.implied_volatility_gui()

    def get_implied_volatility(self):
        try:
            bs = BlackScholes()
            result = bs.get_implied_volatility(float(self.S.get()), float(self.K.get()), float(self.T.get()),
                                               float(self.r.get()), float(self.q.get()),
                                               self.option_type.get(), float(self.O_fair.get()))
            self.output.insert(END, "The Implied Volatility is: {}\n".format(result))
        except Exception as e:
            self.output.insert(END, "Error in calculating the price\n")
            self.output.insert(END, repr(e))
            print('Error %s', repr(e))

    def blackScholesUI(self):
        self.tearDown()
        frame = self.blackScholesGui
        frame.pack()

        Label(frame, text="Black Scholes Price for European Call/Put Options",
              font=tkFont.Font(size=11, weight='bold')).grid(row=1, column=1, sticky=W)
        Label(frame, text='Spot Price').grid(row=2, column=1, sticky=W)
        Label(frame, text='Strike Price').grid(row=3, column=1, sticky=W)
        Label(frame, text='Volatility').grid(row=4, column=1, sticky=W)
        Label(frame, text='Risk Free Rate').grid(row=5, column=1, sticky=W)
        Label(frame, text='Time to Maturity (in years)').grid(row=6, column=1, sticky=W)
        Label(frame, text='Repo Rate').grid(row=7, column=1, sticky=W)
        Label(frame, text='Option Type: Call or Put').grid(row=8, column=1, sticky=W)

        self.S = StringVar()
        self.K = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.q = StringVar()
        self.option_type = StringVar()

        Entry(frame, textvariable=self.S).grid(row=2, column=2, sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3, column=2, sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=4, column=2, sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5, column=2, sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6, column=2, sticky=W)
        Entry(frame, textvariable=self.q).grid(row=7, column=2, sticky=W)

        Radiobutton(frame, text="Put", variable=self.option_type, value='Put').grid(row=8, column=2, sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='Call').grid(row=8, column=2, sticky=W)

        Button(frame, width=20, text="Reset", command=self.reset_black_scholes).grid(row=10, column=1,
                                                                                            columnspan=1,
                                                                                            sticky=E)

        Button(frame, width=20, text="Compute", command=self.calculate_black_scholes).grid(row=10, column=2,
                                                                                             columnspan=1,
                                                                                             sticky=W)

        self.output = scrolledtext.ScrolledText(frame, width=74, height=8)
        self.output.grid(row=11, column=1, rowspan=4, columnspan=2, sticky=W)

    def reset_black_scholes(self):
        self.S = 0
        self.K = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.q = 0
        self.blackScholesUI()

    def calculate_black_scholes(self):
        try:
            option = BlackScholes()
            result = option.euro_extended(float(self.S.get()), float(self.K.get()), float(self.T.get()),
                                          float(self.r.get()), float(self.q.get()), float(self.sigma.get()),
                                          self.option_type.get())
            self.output.insert(END, "Result: {}\n".format(result))
        except Exception as e:
            self.output.insert(END, "Error in calculating the price\n")
            self.output.insert(END, repr(e))
            print('Error: ', repr(e))

    def kikoPut(self):
        self.tearDown()
        frame = self.kikoGui
        frame.pack()

        Label(frame, text="KIKO Calculator", font=tkFont.Font(size=15, weight='bold')).grid(row=1, column=1, sticky=W)

        Label(frame, text='Risk-free rate (r)').grid(row=2, column=1, sticky=W)
        Label(frame, text='Volatility (sigma)').grid(row=3, column=1, sticky=W)
        Label(frame, text='Time to maturity (T)').grid(row=4, column=1, sticky=W)
        Label(frame, text='Spot price (s)').grid(row=5, column=1, sticky=W)
        Label(frame, text='Strike price (K)').grid(row=6, column=1, sticky=W)
        Label(frame, text='Lower barrier').grid(row=7, column=1, sticky=W)
        Label(frame, text='Upper barrier').grid(row=8, column=1, sticky=W)
        Label(frame, text='Number of time steps (N)').grid(row=9, column=1, sticky=W)
        Label(frame, text='Rebate (R)').grid(row=10, column=1, sticky=W)
        Label(frame, text='Number of simulations (M)').grid(row=11, column=1, sticky=W)
        Label(frame, text='Random seed (optional)').grid(row=12, column=1, sticky=W)

        self.r = StringVar()
        self.sigma = StringVar()
        self.T = StringVar()
        self.s = StringVar()
        self.K = StringVar()
        self.barrier_lower = StringVar()
        self.barrier_upper = StringVar()
        self.N = StringVar()
        self.R = StringVar()
        self.M = StringVar()
        self.seed = StringVar()

        # Entry widgets to input values
        Entry(frame, textvariable=self.r).grid(row=2, column=2, sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=3, column=2, sticky=W)
        Entry(frame, textvariable=self.T).grid(row=4, column=2, sticky=W)
        Entry(frame, textvariable=self.s).grid(row=5, column=2, sticky=W)
        Entry(frame, textvariable=self.K).grid(row=6, column=2, sticky=W)
        Entry(frame, textvariable=self.barrier_lower).grid(row=7, column=2, sticky=W)
        Entry(frame, textvariable=self.barrier_upper).grid(row=8, column=2, sticky=W)
        Entry(frame, textvariable=self.N).grid(row=9, column=2, sticky=W)
        Entry(frame, textvariable=self.R).grid(row=10, column=2, sticky=W)
        Entry(frame, textvariable=self.M).grid(row=11, column=2, sticky=W)
        Entry(frame, textvariable=self.seed).grid(row=12, column=2, sticky=W)

        Button(frame, width=20, text="Reset", command=self.resetKiko).grid(row=13, column=1, columnspan=1,
                                                                                  sticky=E)

        Button(frame, width=20, text="Compute", command=self.get_KIKO_Put).grid(row=13, column=2,
                                                                                  columnspan=1,
                                                                                  sticky=W)

        self.output = scrolledtext.ScrolledText(frame, width=74, height=8)
        self.output.grid(row=15, column=1, rowspan=4, columnspan=2, sticky=W)

    def resetKiko(self):
        self.r = 0
        self.sigma = 0
        self.T = 0
        self.s = 0
        self.K = 0
        self.barrier_lower = 0
        self.barrier_upper = 0
        self.N = 0
        self.R = 0
        self.M = 0
        self.seed = 0
        self.kikoPut()

    def get_KIKO_Put(self):
        try:
            pricer = KikoPutOption.KIKOOptionPricer(float(self.r.get()), float(self.sigma.get()), float(self.T.get()),
                                                    float(self.s.get()), float(self.K.get()),
                                                    float(self.barrier_lower.get()),
                                                    float(self.barrier_upper.get()), int(self.N.get()),
                                                    float(self.R.get()), int(self.M.get()), int(self.seed.get()))
            option_price, conf_lower, conf_upper = pricer.calculate_option_price(float(self.s.get()))
            delta = pricer.calculate_delta()

            self.output.insert(END,
                             "The Option price is: {option_price}\n Delta: {delta}\n Conf Interval: [{conf_lower}, {conf_upper}]\n".format(
                                 option_price=option_price, delta=delta, conf_lower=conf_lower, conf_upper=conf_upper))
        except Exception as e:
            self.output.insert(END, "Error in calculating the price\n")
            self.output.insert(END, repr(e))
            print('Error %s', repr(e))


if __name__ == '__main__':
    OptionPricer()
