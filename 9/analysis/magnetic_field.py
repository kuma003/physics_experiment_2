import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


measured_before = [
    50.7,
    49.7,
    49.6,
    50.0,
    51.5,
    50.3,
    50.3,
    50.7,
    50.2,
    50.2,
    50.2,
    50.4,
    49.0,
    49.0,
    49.2,
    50.0,
]
measured_before = np.array(measured_before).reshape(4, 4).T

measured_after = [
    50.2,
    49.1,
    49.0,
    49.6,
    51.0,
    50.3,
    50.2,
    50.4,
    50.1,
    50.0,
    50.1,
    50.5,
    49.0,
    49.0,
    49.3,
    50.1,
]
measured_after = np.array(measured_after).reshape(4, 4).T

measured_after_center = 49.6

dx = 0.5 / 4  ## difference between two points
measured_X, measured_Z = np.meshgrid(
    -np.arange(-0.25 + dx / 2, 0.25, dx), np.arange(-0.25 + dx / 2, 0.25, dx)
)
print(measured_X)
print(measured_Z)


if __name__ == "__main__":
    file_dir = "magnetic_field"
    file_name = "magnet_2025_2_B_20250522_3.out"
    # read data
    file_path = f"{file_dir}/{file_name}"

    data = pd.read_csv(file_path, sep="\s+", header=None, engine="python")
    data.iloc[:, 3:] *= 10000  # convert to Gauss
    # add new column: norm of each row
    data["norm"] = np.linalg.norm(data.iloc[:, 1:4], axis=1)

    # clamp
    data = data[(abs(data[0]) <= 0.20) & (abs(data[2]) <= 0.20)]

    x_vals = np.linspace(data[0].min(), data[0].max(), 100)
    z_vals = np.linspace(data[2].min(), data[2].max(), 100)
    grid_size = (x_vals, z_vals)

    # fig1 = plt.subplots(figsize=(12, 6))
    fig1, ax1 = plt.subplots(figsize=(12, 6))  # 最初のプロット (ヒートマップ)
    fig2, ax2 = plt.subplots(
        figsize=(12, 6), subplot_kw={"projection": "3d"}
    )  # 2番目のプロット (3D曲面)

    # at y = 0.085, B_y
    data = data[abs(data[1]) < 0.001].iloc[:, [0, 2, 3]].values
    X, Z = np.meshgrid(x_vals, z_vals)

    B_x = griddata(data[:, :2], data[:, 2], (X, Z), method="linear")

    # plot
    im = ax1.imshow(
        B_x,
        extent=[x_vals.min(), x_vals.max(), z_vals.min(), z_vals.max()],
        origin="lower",
        cmap="viridis",
        aspect="equal",
    )
    print(x_vals.min(), x_vals.max(), z_vals.min(), z_vals.max())
    # ax1.set_title("B_x at y=0")
    ax1.set_xlabel("x [m]")
    ax1.set_ylabel("z [m]")
    ax1.invert_yaxis()  # y軸を反転
    fig1.colorbar(im, ax=ax1, label="B_x [Gauss]")
    cs = ax1.contour(
        B_x,
        levels=np.arange(47, 52, 0.5),
        extent=[x_vals.min(), x_vals.max(), z_vals.min(), z_vals.max()],
        origin="lower",
        # cmap="viridis",
    )
    ax1.clabel(cs, inline=1, fontsize=10)

    s = ax2.plot_surface(
        X,
        Z,
        B_x,
        cmap="viridis",
        edgecolor="none",
    )
    # ax2.set_title("B_x at y=0")
    ax2.set_xlabel("x [m]")
    ax2.set_ylabel("z [m]")
    ax2.invert_yaxis()  # y軸を反転
    ax2.set_zlabel("B_x [Gauss]")
    ax2.set_zlim(0, np.nanmax(B_x))
    ax2.view_init(30, 30)
    cs = ax2.contour(X, Z, B_x, zdir="z", levels=np.arange(47, 52, 0.5), offset=0)
    print(cs)
    ax2.clabel(cs, inline=1, fontsize=10)
    fig2.colorbar(s, ax=ax2, label="B_x [Gauss]")

    # overwite by measured data
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    # plot only the 2d heatmap
    im = ax3.imshow(
        B_x,
        extent=[x_vals.min(), x_vals.max(), z_vals.min(), z_vals.max()],
        origin="lower",
        cmap="viridis",
        aspect="equal",
    )
    # overwrite the meassured data with circle markers witch color are followed by the heatmaps colorbar
    ax3.scatter(
        measured_X,
        measured_Z,
        c=measured_before.flatten(),
        cmap="viridis",
        edgecolor="black",
        s=100,
    )

    # calculate the theoretical B_x at the points of measured points
    theoritical_B_x = griddata(
        data[:, :2], data[:, 2], (measured_X, measured_Z), method="linear"
    )

    # calculate the difference
    difference = (measured_before - theoritical_B_x) / theoritical_B_x * 100

    print("Difference between measured and theoretical B_x:\n", difference)

    # ax3.set_title("Measured Magnetic Field Before")
    ax3.set_xlabel("x [m]")
    ax3.set_ylabel("z [m]")
    ax3.invert_yaxis()  # y軸を反転
    fig3.colorbar(im, ax=ax3, label="B [Gauss]")

    # plot the measured data after
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    # plot only the 2d heatmap
    im = ax4.imshow(
        B_x,
        extent=[x_vals.min(), x_vals.max(), z_vals.min(), z_vals.max()],
        origin="lower",
        cmap="viridis",
        aspect="equal",
    )

    # overwrite the meassured data with circle markers witch color are followed by the heatmaps colorbar
    ax4.scatter(
        measured_X,
        measured_Z,
        c=measured_after.flatten(),
        cmap="viridis",
        edgecolor="black",
        s=100,
    )
    ax4.scatter(0, 0, c=measured_after_center, cmap="viridis", edgecolor="black", s=100)
    # calculate the theoretical B_x at the points of measured points and its difference
    theoritical_center_B_x = griddata(data[:, :2], data[:, 2], (0, 0), method="linear")
    difference = (measured_after - theoritical_B_x) / theoritical_B_x * 100
    print("Difference between measured and theoretical B_x:\n", difference)
    print(
        "Difference on the center point:",
        (measured_after_center - theoritical_center_B_x) / theoritical_center_B_x * 100,
    )
    print("average difference:", np.mean(difference))
    print("average measured data:", np.mean(measured_after.flatten()))
    print("uncertanty of the measured data:", np.std(measured_after.flatten()))
    # ax4.set_title("Theoritical & Measured Magnetic Field")
    ax4.set_xlabel("x [m]")
    ax4.set_ylabel("z [m]")
    ax4.invert_yaxis()  # y軸を反転
    fig4.colorbar(im, ax=ax4, label="B [Gauss]")

    plt.show()
