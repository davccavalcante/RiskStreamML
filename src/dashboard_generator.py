import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from src.config import INTERACTIVE_DASHBOARD_PATH, OUTPUT_DIR

def generate_interactive_dashboard(df, duplicates_df, anomalies_df, logger):
    """Generates an interactive HTML dashboard with the analysis results."""
    logger.info("Generating interactive HTML dashboard.")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Chart 1: Payment Distribution
    fig1 = px.histogram(df, x="amount", nbins=20, title='Payment Amount Distribution')

    # Chart 2: Monthly Trend
    df['payment_date'] = pd.to_datetime(df['payment_date'])
    monthly_summary = df.groupby(df['payment_date'].dt.to_period('M'))['amount'].sum().reset_index()
    monthly_summary['payment_date'] = monthly_summary['payment_date'].dt.to_timestamp()
    fig2 = px.line(monthly_summary, x="payment_date", y="amount", title='Monthly Trend of Total Payment Amount')

    # Chart 3: Anomalous Payments (if any)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df.index, y=df['amount'], mode='markers', name='All Payments'))
    if not anomalies_df.empty:
        fig3.add_trace(go.Scatter(x=anomalies_df.index, y=anomalies_df['amount'], mode='markers', name='Anomalies (ML)', marker=dict(color='red', size=10)))
    fig3.update_layout(title='Payments and Detected Anomalies', xaxis_title='Record Index', yaxis_title='Payment Amount')

    # Duplicates Table
    duplicates_html = "<h3>Detected Duplicates</h3>"
    if not duplicates_df.empty:
        duplicates_html += duplicates_df.to_html(index=False)
    else:
        duplicates_html += "<p>No duplicates found.</p>"

    # HTML Dashboard Layout
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Risk Analysis Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .chart-container {{ margin-bottom: 40px; border: 1px solid #eee; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 8px rgba(0,0,0,0.1); }}
            h1, h2, h3 {{ color: #333; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Payment Risk Analysis Dashboard</h1>
        <p>This interactive dashboard presents the key insights from the risk analysis pipeline.</p>

        <div class="chart-container">
            <h2>Payment Amount Distribution</h2>
            <div id="chart1"></div>
        </div>

        <div class="chart-container">
            <h2>Monthly Trend of Total Payment Amount</h2>
            <div id="chart2"></div>
        </div>

        <div class="chart-container">
            <h2>Payments and Detected Anomalies</h2>
            <div id="chart3"></div>
        </div>

        <div class="chart-container">
            {duplicates_html}
        </div>

        <script>
            Plotly.newPlot('chart1', {fig1.to_json(pretty=True).replace("\n", "")});
            Plotly.newPlot('chart2', {fig2.to_json(pretty=True).replace("\n", "")});
            Plotly.newPlot('chart3', {fig3.to_json(pretty=True).replace("\n", "")});
        </script>
    </body>
    </html>
    """

    with open(INTERACTIVE_DASHBOARD_PATH, 'w') as f:
        f.write(html_content)

    logger.info(f"Interactive dashboard saved to: {INTERACTIVE_DASHBOARD_PATH}")
