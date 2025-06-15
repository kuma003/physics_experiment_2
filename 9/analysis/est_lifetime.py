import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

# 論文用フォントとスタイル設定
plt.rcParams.update(
    {
        "font.size": 12,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "axes.linewidth": 1.2,
        "axes.labelsize": 14,
        "axes.titlesize": 16,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 12,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.1,
    }
)


if __name__ == "__main__":
    # read command line arguments
    import sys

    if len(sys.argv) != 2:
        print("Usage: python calc_lifetime.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]

    # read data
    # Specify custom column headers
    headers = ["lifetime", "ch1", "ch2"]  # ここを必要なカラム名に変更してください
    data = pd.read_csv(
        file_path,
        delimiter=" ",
        header=None,
        names=headers,
        engine="python",
        comment="#",
    )
    print(data.head())

    # using data less than 11ns
    data = data[(data["lifetime"] > 1) & (data["lifetime"] < 10)]

    # fit data

    # plot
    fig, ax = plt.subplots(figsize=(8, 5))

    plt.plot(
        data["lifetime"],
        data["ch1"],
        "o",
        markersize=2,
        label="Channel 1",
        color="black",
    )
    plt.plot(
        data["lifetime"],
        data["ch2"],
        "^",
        markersize=2,
        label="Channel 2",
        color="black",
    )

    # fitting
    def single_exp(t, A, tau, C):
        return A * np.exp(-t / tau) + C

    popt, pcov = curve_fit(single_exp, data["lifetime"], data["ch1"], p0=[1, 1, 0])
    perr = np.sqrt(np.diag(pcov))
    fitted_data = single_exp(data["lifetime"], *popt)
    plt.plot(
        data["lifetime"],
        fitted_data,
        linestyle="--",
        label=(f"Fitted Channel 1 (τ={popt[1]:.2f}±{perr[1]:.2f} [us])"),
        color="#303030",  # dark gray
    )
    print("fitted parameters for channel 1:", popt, perr)

    popt, pcov = curve_fit(single_exp, data["lifetime"], data["ch2"], p0=[1, 1, 0])
    perr = np.sqrt(np.diag(pcov))
    fitted_data = single_exp(data["lifetime"], *popt)
    plt.plot(
        data["lifetime"],
        fitted_data,
        linestyle="-.",
        label=(f"Fitted Channel 2 (τ={popt[1]:.2f}±{perr[1]:.2f} [us])"),
        color="#303030",  # dark gray
    )
    print("fitted parameters for channel 2:", popt, perr)

    plt.xlabel("Time [us]")
    plt.ylabel("Counts")
    # plt.title("Lifetime Measurement")
    plt.legend()
    plt.grid()
    plt.savefig("lifetime_measurement.pdf")
    plt.show()
