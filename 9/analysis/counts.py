import pandas as pd
import numpy as np
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

# Excelファイルからデータを読み込み
file_path = "exp_data.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1", header=None)

print("データの最初の10行:")
print(df.head(10))


# データの抽出と整理
def clean_numeric(x):
    """カンマを除去して数値に変換"""
    if pd.isna(x):
        return np.nan
    return float(str(x).replace(",", ""))


# Plate1のデータ（行3-9, 0-indexedなので2-8）
plate1_data = {
    "HV": [clean_numeric(df.iloc[i, 0]) for i in range(3, 10)],
    "PMT1_count": [clean_numeric(df.iloc[i, 1]) for i in range(3, 10)],
    "PMT2_count": [clean_numeric(df.iloc[i, 2]) for i in range(3, 10)],
    "coincidence": [clean_numeric(df.iloc[i, 3]) for i in range(3, 10)],
    "plate": ["Plate1"] * 7,
}

# Plate2のデータ（行13-19, 0-indexedなので12-18）
plate2_data = {
    "HV": [clean_numeric(df.iloc[i, 0]) for i in range(13, 20)],
    "PMT1_count": [clean_numeric(df.iloc[i, 1]) for i in range(13, 20)],
    "PMT2_count": [clean_numeric(df.iloc[i, 2]) for i in range(13, 20)],
    "coincidence": [clean_numeric(df.iloc[i, 3]) for i in range(13, 20)],
    "plate": ["Plate2"] * 7,
}

# Plate3のデータ（行23-29, 0-indexedなので22-28）
plate3_data = {
    "HV": [clean_numeric(df.iloc[i, 0]) for i in range(23, 30)],
    "PMT1_count": [clean_numeric(df.iloc[i, 1]) for i in range(23, 30)],
    "PMT2_count": [clean_numeric(df.iloc[i, 2]) for i in range(23, 30)],
    "coincidence": [clean_numeric(df.iloc[i, 3]) for i in range(23, 30)],
    "plate": ["Plate3"] * 7,
}

# データフレームの作成
df_plate1 = pd.DataFrame(plate1_data)
df_plate2 = pd.DataFrame(plate2_data)
df_plate3 = pd.DataFrame(plate3_data)

# 全データの結合
combined_df = pd.concat([df_plate1, df_plate2, df_plate3], ignore_index=True)

print("\n処理後のデータ:")
print(combined_df)

# モノクロ印刷対応カラーパレット
colors = {
    "PMT1": "#000000",  # 黒
    "PMT2": "#000000",  # 濃いグレー
    "coincidence": "#000000",  # 中間グレー
}

# マーカーとラインスタイル（識別しやすく）
markers = {"PMT1": "o", "PMT2": "s", "coincidence": "^"}
linestyles = {"PMT1": "-", "PMT2": "--", "coincidence": ":"}

# Plate1のプロット
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(
    df_plate1["HV"],
    df_plate1["PMT1_count"],
    marker=markers["PMT1"],
    linestyle=linestyles["PMT1"],
    color=colors["PMT1"],
    linewidth=2,
    markersize=8,
    label="PMT1",
    markerfacecolor="white",
    markeredgewidth=2,
)
ax.plot(
    df_plate1["HV"],
    df_plate1["PMT2_count"],
    marker=markers["PMT2"],
    linestyle=linestyles["PMT2"],
    color=colors["PMT2"],
    linewidth=2,
    markersize=8,
    label="PMT2",
    markerfacecolor="white",
    markeredgewidth=2,
)
ax.plot(
    df_plate1["HV"],
    df_plate1["coincidence"],
    marker=markers["coincidence"],
    linestyle=linestyles["coincidence"],
    color=colors["coincidence"],
    linewidth=2,
    markersize=8,
    label="Coincidence",
    markerfacecolor="white",
    markeredgewidth=2,
)

ax.set_xlabel("High Voltage [V]")
ax.set_ylabel("Count Rate [count/s]")
# ax.set_title("Plate 1: Count Rate vs High Voltage")
ax.legend()
ax.grid(True, alpha=0.3, linestyle=":")
ax.set_xlim(1430, 1770)
plt.tight_layout()
plt.savefig("plate1_count_vs_voltage.pdf", dpi=300, bbox_inches="tight")
# plt.show()

# Plate2のプロット
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(
    df_plate2["HV"],
    df_plate2["PMT1_count"],
    marker=markers["PMT1"],
    linestyle=linestyles["PMT1"],
    color=colors["PMT1"],
    linewidth=2,
    markersize=8,
    label="PMT3",
    markerfacecolor="white",
    markeredgewidth=2,
)
ax.plot(
    df_plate2["HV"],
    df_plate2["PMT2_count"],
    marker=markers["PMT2"],
    linestyle=linestyles["PMT2"],
    color=colors["PMT2"],
    linewidth=2,
    markersize=8,
    label="PMT4",
    markerfacecolor="white",
    markeredgewidth=2,
)
ax.plot(
    df_plate2["HV"],
    df_plate2["coincidence"],
    marker=markers["coincidence"],
    linestyle=linestyles["coincidence"],
    color=colors["coincidence"],
    linewidth=2,
    markersize=8,
    label="Coincidence",
    markerfacecolor="white",
    markeredgewidth=2,
)

ax.set_xlabel("High Voltage [V]")
ax.set_ylabel("Count Rate [count/s]")
# ax.set_title("Plate 2: Count Rate vs High Voltage")
ax.legend()
ax.grid(True, alpha=0.3, linestyle=":")
ax.set_xlim(1430, 1770)
plt.tight_layout()
plt.savefig("plate2_count_vs_voltage.pdf", dpi=300, bbox_inches="tight")
# plt.show()

# Plate3のプロット
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(
    df_plate3["HV"],
    df_plate3["PMT1_count"],
    marker=markers["PMT1"],
    linestyle=linestyles["PMT1"],
    color=colors["PMT1"],
    linewidth=2,
    markersize=8,
    label="PMT5",
    markerfacecolor="white",
    markeredgewidth=2,
)
ax.plot(
    df_plate3["HV"],
    df_plate3["PMT2_count"],
    marker=markers["PMT2"],
    linestyle=linestyles["PMT2"],
    color=colors["PMT2"],
    linewidth=2,
    markersize=8,
    label="PMT6",
    markerfacecolor="white",
    markeredgewidth=2,
)
ax.plot(
    df_plate3["HV"],
    df_plate3["coincidence"],
    marker=markers["coincidence"],
    linestyle=linestyles["coincidence"],
    color=colors["coincidence"],
    linewidth=2,
    markersize=8,
    label="Coincidence",
    markerfacecolor="white",
    markeredgewidth=2,
)

ax.set_xlabel("High Voltage [V]")
ax.set_ylabel("Count Rate [count/s]")
# ax.set_title("Plate 3: Count Rate vs High Voltage")
ax.legend()
ax.grid(True, alpha=0.3, linestyle=":")
ax.set_xlim(1430, 1770)
plt.tight_layout()
plt.savefig("plate3_count_vs_voltage.pdf", dpi=300, bbox_inches="tight")
# plt.show()

# 全プレートの比較プロット（同時計数率のみ）
fig, ax = plt.subplots(figsize=(8, 5))
plate_colors = {"Plate1": "#000000", "Plate2": "#000000", "Plate3": "#000000"}
plate_markers = {"Plate1": "o", "Plate2": "s", "Plate3": "^"}
plate_linestyles = {"Plate1": "-", "Plate2": "--", "Plate3": ":"}

for i, (df_plate, plate_name) in enumerate(
    [(df_plate1, "Plate1"), (df_plate2, "Plate2"), (df_plate3, "Plate3")]
):
    ax.plot(
        df_plate["HV"],
        df_plate["coincidence"],
        marker=plate_markers[plate_name],
        linestyle=plate_linestyles[plate_name],
        color=plate_colors[plate_name],
        linewidth=2.5,
        markersize=10,
        label=f"{plate_name}",
        markerfacecolor="white",
        markeredgewidth=2.5,
        alpha=0.9,
    )

ax.hlines(
    y=80,
    xmin=1430,
    xmax=1770,
    color="black",
    linestyle="--",
    linewidth=1.5,
    label="Threshold (80 count/s)",
)
ax.set_xlabel("High Voltage [V]")
ax.set_ylabel("Coincidence Count Rate [count/s]")
# ax.set_title("Comparison of Coincidence Count Rates")
ax.legend(loc="upper left")
ax.grid(True, alpha=0.3, linestyle=":")
ax.set_xlim(1430, 1770)

# 軸の範囲を自動調整
y_min = min(
    [
        df_plate1["coincidence"].min(),
        df_plate2["coincidence"].min(),
        df_plate3["coincidence"].min(),
    ]
)
y_max = max(
    [
        df_plate1["coincidence"].max(),
        df_plate2["coincidence"].max(),
        df_plate3["coincidence"].max(),
    ]
)
ax.set_ylim(y_min * 0.9, y_max * 1.1)

plt.tight_layout()
plt.savefig("comparison_coincidence_rates.pdf", dpi=300, bbox_inches="tight")
# plt.show()
