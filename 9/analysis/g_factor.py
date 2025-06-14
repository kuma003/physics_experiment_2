"""'
g_factor.py
# Calculate the Lande g-factor from the fitted parameters of a lifetime measurement.
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as const
from uncertainties import ufloat


def R(t, a, b, omega_L):
    return a + b * np.cos(omega_L * t)


if __name__ == "__main__":
    original = "two_week_measure.txt"
    histgram = "time_histgram_two_week_measure.txt"

    # get total count (number of lines of the original file)
    with open(original, "r") as f:
        total_count = sum(1 for line in f if not line.startswith("#") or line == "\n")
    print(f"Total count: {total_count}")

    # plot histogram
    data = pd.read_csv(
        histgram,
        delimiter=" ",
        header=None,
        names=["lifetime", "U(t)", "D(t)"],
        engine="python",
        comment="#",
    )

    # estimate accidental coincidence
    # accidental coincidence rate
    n_2 = 5253 / 60.0  # count rate [count/sec]
    n_3 = 2687 / 60.0  # count rate [count/sec]

    # Delta T (bin width)
    
    delta_t = data["lifetime"].diff().mean()
    print(f"Delta T: {delta_t} us")
    # number of accidental coincidence
    C_U = delta_t * 1e-6 * n_2 * total_count
    C_D = delta_t * 1e-6 * n_3 * total_count
    print(C_U, C_D)

    data["U_calb(t)"] = data["U(t)"] - C_U
    data["D_calb(t)"] = data["D(t)"] - C_D

    # calclulate R(t) (unsymmetric ratio)
    data["R(t)"] = (data["U_calb(t)"] - data["D_calb(t)"]) / (
        data["U_calb(t)"] + data["D_calb(t)"]
    )

    # fitting R(t)
    # fitting are applied to only for the time > 5 us
    popt, pcov = curve_fit(
        R,
        data.loc[(data["lifetime"] >= 5.5) & (data["lifetime"] <= 8), "lifetime"],
        data.loc[(data["lifetime"] >= 5.5) & (data["lifetime"] <= 8), "R(t)"],
        p0=[0, 4, 1.3 * np.pi],  # initial guess
    )
    perr = np.sqrt(np.diag(pcov))
    print("Fitted parameters:", popt)
    print("Parameter errors:", perr)
    data["R_fit(t)"] = R(data["lifetime"], *popt)

    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(data["lifetime"], data["U_calb(t)"], label="U_calb(t)")
    ax1.plot(data["lifetime"], data["D_calb(t)"], label="D_calb(t)")
    ax1.set_xlabel("time (us)")
    ax1.set_ylabel("counts")
    ax1.set_title("Time Histogram")
    ax1.legend()

    # plot R(t)
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(data["lifetime"], data["R(t)"], label="R(t)")
    ax2.plot(
        data.loc[(data["lifetime"] >= 5.5) & (data["lifetime"] <= 8), "lifetime"],
        data.loc[(data["lifetime"] >= 5.5) & (data["lifetime"] <= 8), "R_fit(t)"],
        label="Fitted R(t)",
        linestyle="--",
    )
    ax2.set_xlabel("time (us)")
    ax2.set_ylabel("R(t)")
    ax2.set_title("Unsymmetric Ratio R(t)")
    ax2.legend()

    # calculate g-factor
    omega_L = ufloat(popt[2], perr[2]) * 1e6  # angular frequency
    B = ufloat(49.86875, 0.6017877013532266) * 1e-4
    m_mu = 105.66e6  # muon mass in eV/c^2
    # convet to SI units
    m_mu = m_mu * const.e / (const.c**2)  # convert to J
    g_factor = omega_L / (const.e * B / (2 * m_mu))
    print(f"g-factor: {g_factor}")

    # estimate polarization
    P_0 = 3 * ufloat(popt[1], perr[1])
    print(f"Polarization P_0: {P_0}")

    plt.show()
