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
# Formulario para agregar una nueva película
app.layout.children.append(html.Div([
    html.H2("Agregar una nueva película", style={"textAlign": "center"}),
    html.Div([
        dcc.Input(id="input-name", type="text", placeholder="Nombre de la película", style={"marginRight": "10px"}),
        dcc.Input(id="input-year", type="number", placeholder="Año", style={"marginRight": "10px"}),
        dcc.Input(id="input-duration", type="number", placeholder="Duración (min)", style={"marginRight": "10px"}),
        html.Button("Agregar", id="add-button", n_clicks=0)
    ], style={"textAlign": "center", "marginBottom": "20px"}),
    html.Div(id="add-movie-message", style={"textAlign": "center", "color": "green"})
]))

# Callback para manejar la adición de una nueva película
@app.callback(
    Output("add-movie-message", "children"),
    Input("add-button", "n_clicks"),
    [dash.dependencies.State("input-name", "value"),
     dash.dependencies.State("input-year", "value"),
     dash.dependencies.State("input-duration", "value")]
)
def add_movie(n_clicks, name, year, duration):
    if n_clicks > 0:
        if not name or not year or not duration:
            return "Por favor, complete todos los campos."
        new_movie = {
            "carMovieName": name,
            "carMovieYear": int(year),
            "duration": int(duration)
        }
        POST_URL = "https://carsmoviesinventoryproject-production.up.railway.app/api/v1/carsmovies"
        response = requests.post(POST_URL, json=new_movie)

        if response.status_code == 201:
            return "Película agregada exitosamente."
        else:
            return "Error al agregar la película."
    return ""

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
    

   