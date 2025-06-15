import read_datafile
import numpy as np
import os
import matplotlib.pyplot as plt

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
    channels = [1, 2]
    designed_delay = np.arange(0, 1000, 105)
    measured_delay = [
        [0 for __ in range(len(designed_delay))] for _ in range(len(channels))
    ]

    for channel in channels:
        for delay in designed_delay:
            file_path = f"ch{channel}_{delay}ns.txt"
            if not os.path.isfile(file_path):
                print(f"The file {file_path} does not exist.")
                continue
            # read data
            data = read_datafile.read_datafile(file_path)
            # calc average for each column
            avg = data.mean()[channel - 1]
            # print(f"Average for {channel} with delay {delay}:")
            # print(avg)
            measured_delay[channel - 1][delay // 105] = avg

    # convert ns to microseconds
    designed_delay = np.array(designed_delay) / 1000

    print("Measured delay:")
    print(measured_delay)

    # calc interpolation for each channel
    for channel in channels:
        # calc interpolation
        coeffs = np.polyfit(measured_delay[channel - 1], designed_delay, 1)

        print(f"channel {channel}: y = {coeffs[0]} * x + {coeffs[1]}")

        # calculate r value
        r = np.corrcoef(measured_delay[channel - 1], designed_delay)[0, 1]
        print(f"channel {channel}: r = {r}")

        fig, ax = plt.subplots(figsize=(8, 5))

        # plot
        ax.plot(
            measured_delay[channel - 1],
            designed_delay,
            "o",
            color="black",
            label=f"Channel {channel}",
        )
        ax.plot(
            measured_delay[channel - 1],
            np.polyval(coeffs, measured_delay[channel - 1]),
            color="black",
            label=f"Channel {channel} fit",
        )
        ax.set_xlabel("Measured delay (TDC channel)")
        ax.set_ylabel("Designed delay [us]")
        # ax.set_title("Delay calibration")
        # plt.xlim(0, 10)
        ax.legend()
        ax.grid()
        # save plot before showing
        plt.savefig(f"calibration_channel_{channel}.pdf")
