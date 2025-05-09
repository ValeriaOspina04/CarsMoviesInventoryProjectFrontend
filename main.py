import dash
from dash import dcc, html, dash_table
import requests
from dash.dependencies import Input, Output

# Crear la aplicación Dash
app = dash.Dash(__name__)

# URL de la API
API_URL = "https://carsmoviesinventoryproject-production.up.railway.app/api/v1/carsmovies?page=0&size=5&sort=carMovieYear,desc"

# Función para obtener datos de la API
def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return data["Movies"]
    else:
        return []

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Cars Movies Inventory Dashboard", style={"textAlign": "center"}),
    dash_table.DataTable(
        id="movies-table",
        columns=[
            {"name": "ID", "id": "id"},
            {"name": "Name", "id": "carMovieName"},
            {"name": "Year", "id": "carMovieYear"},
            {"name": "Duration (min)", "id": "duration"}
        ],
        data=fetch_data(),
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "padding": "10px"},
        style_header={"backgroundColor": "lightblue", "fontWeight": "bold"}
    )
])

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
    