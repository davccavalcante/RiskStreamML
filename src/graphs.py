import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.config import (
    PAYMENT_DISTRIBUTION_CHART,
    MONTHLY_TREND_CHART,
    STATS_SUMMARY_TABLE,
    OUTPUT_DIR
)
import os

def generate_payment_distribution_chart(df):
    """Generates a payment amount distribution chart."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    plt.figure(figsize=(10, 6))
    sns.histplot(df['amount'], bins=20, kde=True)
    plt.title('Payment Amount Distribution')
    plt.xlabel('Payment Amount')
    plt.ylabel('Frequency')
    plt.grid(True)

    plt.savefig(PAYMENT_DISTRIBUTION_CHART)
    print(f"Distribution chart saved to: {PAYMENT_DISTRIBUTION_CHART}")
    plt.close()

def generate_monthly_trend_chart(df):
    """Generates a line chart showing monthly payment trends."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df['payment_date'] = pd.to_datetime(df['payment_date'])
    monthly_summary = df.groupby(df['payment_date'].dt.to_period('M'))['amount'].sum()
    monthly_summary.index = monthly_summary.index.to_timestamp()

    plt.figure(figsize=(12, 6))
    plt.plot(monthly_summary.index, monthly_summary.values, marker='o', linestyle='-')
    plt.title('Monthly Trend of Total Payment Amount')
    plt.xlabel('Month')
    plt.ylabel('Total Amount Paid')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(MONTHLY_TREND_CHART)
    print(f"Monthly trend chart saved to: {MONTHLY_TREND_CHART}")
    plt.close()

def generate_stats_summary_table(df):
    """Generates an image of the statistical summary table."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    stats = df['amount'].describe().round(2).to_frame().reset_index()
    stats.columns = ['Metric', 'Value']

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=stats.values, colLabels=stats.columns, loc='center', cellLoc='center')
    table.set_fontsize(12)
    table.scale(1.2, 1.2)

    plt.title('Statistical Summary of Payments', pad=20)
    plt.savefig(STATS_SUMMARY_TABLE, bbox_inches='tight', pad_inches=0.1)
    print(f"Statistical summary table saved to: {STATS_SUMMARY_TABLE}")
    plt.close()
