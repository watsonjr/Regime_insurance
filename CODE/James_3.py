import subprocess

## Run Jack's julia script for making the windows data (Data_utils.csv)
subprocess.run(["julia", "Jack_windows.jl"], check=True)

## Plot
import pandas as pd
import matplotlib.pyplot as plt

#======================= p
# Load data
df = pd.read_csv("../DATA/Data_utils.csv")

# Create figure
plt.figure(figsize=(6, 6))  # Good for 1-column journal width
#plt.figure(figsize=(8, 4))  # 2-column style

# Plot lines
plt.plot(df["p"], df["utils_with"], linewidth=2, label="Utility With")
plt.plot(df["p"], df["utils_without"], linewidth=2, label="Utility Without")
plt.plot(df["p"], df["utility_alternative"], linewidth=2, label="Utility Alternative")

# Labels and title
plt.xlabel("Probability (p)", fontsize=12)
plt.ylabel("Utility", fontsize=12)

# Ticks, legend, grid
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=10)
plt.grid(True, linestyle="--", alpha=0.7)

# Tight layout for better spacing
plt.tight_layout()

# Save high-resolution figure
plt.savefig("../FIGS/utility_plot_p.png", dpi=300)



#======================= c
# Load data
df = pd.read_csv("../DATA/Data_utils.csv")

# Create figure
plt.figure(figsize=(6, 6))  # Good for 1-column journal width
#plt.figure(figsize=(8, 4))  # 2-column style

# Plot lines
plt.plot(df["c"], df["utils_with"], linewidth=2, label="Utility With")
plt.plot(df["c"], df["utils_without"], linewidth=2, label="Utility Without")
plt.plot(df["c"], df["utility_alternative"], linewidth=2, label="Utility Alternative")

# Labels and title
plt.xlabel("Extraction Rate (c)", fontsize=12)
plt.ylabel("Utility", fontsize=12)

# Ticks, legend, grid
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=10)
plt.grid(True, linestyle="--", alpha=0.7)

# Tight layout for better spacing
plt.tight_layout()

# Save high-resolution figure
plt.savefig("../FIGS/utility_plot_c.png", dpi=300)

# Show plot
plt.show()





