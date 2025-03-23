import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("spring_crops.csv")

# Filter to keep only rows with "Regular" quality
df_regular = df[df["quality"] == "Regular"]

# Drop rows with missing growth_time or sell_price
filtered_df = df_regular.dropna(subset=["growth_time", "sell_price"])

# Create the scatter plot
fig = px.scatter(
    filtered_df,
    x="growth_time",
    y="sell_price",
    text="name",
    title="Growth Time vs. Sell Price of Spring Crops (Regular Quality) in Stardew Valley",
    labels={
        "growth_time": "Growth Time (days)",
        "sell_price": "Sell Price (gold)"
    },
    hover_data=["description", "production_per_season"]
)

# Optional: adjust layout and label position
fig.update_traces(textposition="top center")
fig.update_layout(height=600, width=800)

# Show the plot
fig.show()