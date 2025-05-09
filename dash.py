import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Загрузка данных
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderData.csv')

# Инициализация приложения
app = dash.Dash(__name__)

# Макет страницы
app.layout = html.Div([
    html.H1('Анализ данных Gapminder'),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df['country'].unique()],
        value='Canada'  # Значение по умолчанию
    ),
    dcc.Graph(id='life-exp-graph')
])

# Callback для обновления графика
@app.callback(
    Output('life-exp-graph', 'figure'),
    Input('country-dropdown', 'value')
)
def update_graph(selected_country):
    filtered_df = df[df['country'] == selected_country]
    fig = px.line(filtered_df, x='year', y='lifeExp', title=f'Ожидаемая продолжительность жизни в {selected_country}')
    return fig

# Запуск сервера
if __name__ == '__main__':
    app.run_server(debug=True)
