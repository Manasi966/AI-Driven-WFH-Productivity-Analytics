import pandas as pd
import matplotlib.pyplot as plt
import os


# Load CSV 
df = pd.read_csv("daily_report.csv", header=None)

# Force correct column names
df.columns = ["Date", "Focus_Min", "Idle_Min", "Away_Min", "Productivity_%"]

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Sort by date
df = df.sort_values("Date")

# WEEKLY AGGREGATION

weekly = df.resample("W", on="Date").mean(numeric_only=True)

# WEEKLY BAR CHART

plt.figure(figsize=(7, 4))

bars = plt.bar(
    weekly.index.strftime("%Y-%m-%d"),
    weekly["Productivity_%"]
)

plt.title("Weekly Productivity Summary", fontsize=14, fontweight="bold")
plt.xlabel("Week")
plt.ylabel("Productivity (%)")
plt.ylim(0, 100)
plt.grid(axis="y", linestyle="--", alpha=0.5)

# Add value labels on bars

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 1,
        f"{round(height, 1)}%",
        ha="center",
        va="bottom",
        fontweight="bold"
    )

plt.tight_layout()


# Save image-
plt.savefig("weekly_productivity.png", dpi=300)

plt.show()

print("✅ Weekly analytics completed")
print("📁 Graph saved as: weekly_productivity.png")
