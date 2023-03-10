import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('/Users/mishudhar/Desktop/Life Expectancy vs GDP 1950-2018.csv')
print(df.head(3))

df.rename(columns= {'Year':'year', 'GDP per capita':'gdpPercap', 'Population (historical estimates)':'pop',
                    'Continent':'continent',
                    'Life expectancy':'lifeExp'}, inplace= True)
#print(df.head(3))
#print(list(df.columns))

app = dash.Dash()


year_options = []
for year in df['year'].unique():
    year_options.append({'label':str(year), 'value':year})

app.layout = html.Div([
    dcc.Graph(id = 'graph'),
    dcc.Dropdown(id = 'year-picker', options = year_options,
                 value = df['year'].min())
])


@app.callback(Output('graph', 'figure'),
              [Input('year-picker', 'value')])
def update_figure(selected_year):

    filtered_df = df[df['year'] == selected_year]

    traces = []
    for continent_name in filtered_df['continent'].unique():
        df_by_continent = filtered_df[filtered_df['continent']== continent_name]
        traces.append(go.Scatter(
            x = df_by_continent['gdpPercap'],
            y = df_by_continent['lifeExp'],
            mode= 'markers',
            opacity= 0.7,
            marker= {'size':15},
            name = continent_name

        ))
    return {'data': traces,
            'layout':go.Layout(title= 'My plot',
                               xaxis= {'title':'Gdp Per Cap', 'type':'log'},
                               yaxis={'title':'Life Expectancy'})}

if __name__ == '__main__':
    app.run_server()