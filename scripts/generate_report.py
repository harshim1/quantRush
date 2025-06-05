
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_report(input_file):
    df = pd.read_csv(input_file, parse_dates=['timestamp'])

    # Summary statistics
    summary = df.describe()
    print("📊 Summary Statistics:\n", summary)

    # PnL over time
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='timestamp', y='pnl')
    plt.title("PnL Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("PnL")
    plt.tight_layout()
    plt.savefig("results/pnl_over_time.png")

    # Inventory over time
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x='timestamp', y='inventory')
    plt.title("Inventory Level Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Inventory")
    plt.tight_layout()
    plt.savefig("results/inventory_over_time.png")

    print("✅ Report generated and plots saved in results/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Performance Report from Simulation Log")
    parser.add_argument('--input', type=str, required=True, help='Path to simulation_log.csv')
    args = parser.parse_args()

    os.makedirs("results", exist_ok=True)
    generate_report(args.input)
