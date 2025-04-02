import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv("fifa_world_cup_finals.csv")

# Standardize country names
df["Winner"] = df["Winner"].replace("West Germany", "Germany")
df["Runner-up"] = df["Runner-up"].replace("West Germany", "Germany")

# Count World Cup wins per country
win_counts = df["Winner"].value_counts().reset_index()
win_counts.columns = ["Country", "Wins"]

# Create the Choropleth map
fig = px.choropleth(
    win_counts,
    locations="Country",
    locationmode="country names",
    color="Wins",
    hover_name="Country",
    color_continuous_scale="Blues",
    title="FIFA World Cup Winners by Country"
)

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={"textAlign": "center"}),
    dcc.Graph(id="world_cup_map", figure=fig),

    html.Label("Select a Country to View Wins:"),
    dcc.Dropdown(
        id="country_dropdown",
        options=[{"label": country, "value": country}
                 for country in win_counts["Country"]],
        value="Brazil",
        clearable=False
    ),
    html.Div(id="win_output"),

    html.Label("Select a Year to View Winner & Runner-up:"),
    dcc.Dropdown(
        id="year_dropdown",
        options=[{"label": str(year), "value": year} for year in df["Year"]],
        value=2022,
        clearable=False
    ),
    html.Div(id="year_output")
])


@app.callback(
    dash.Output("win_output", "children"),
    [dash.Input("country_dropdown", "value")]
)
def update_wins(country):
    wins = win_counts[win_counts["Country"] == country]["Wins"].values[0]
    return f"{country} has won {wins} World Cups."


@app.callback(
    dash.Output("year_output", "children"),
    [dash.Input("year_dropdown", "value")]
)
def update_year(year):
    row = df[df["Year"] == year].iloc[0]
    return f"In {year}, {row['Winner']} won the World Cup, defeating {row['Runner-up']}."


if __name__ == "__main__":
    app.run(debug=True)
