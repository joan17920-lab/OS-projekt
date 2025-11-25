import pandas as pd
import os
import plotly.express as px
import hashlib
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from projekt.utils import graph_sport_output

# Läs in data
<<<<<<< HEAD
rela_path = os.path.dirname(os.path.abspath(__file__))
path_noc_regions = os.path.join(rela_path,"data","noc_regions.csv")
path_athlete_events = os.path.join(rela_path,"data","athlete_events.csv")
=======
path_noc_regions = os.path.join(os.getcwd(),"data","noc_regions.csv")
path_athlete_events = os.path.join(os.getcwd(),"data","athlete_events.csv")
>>>>>>> a75a22c78365db6a7d13c45f55d6038cb51bd43d
noc_region_df = pd.read_csv(path_noc_regions)
athlete_events_df = pd.read_csv(path_athlete_events)
os_data = pd.merge(athlete_events_df, noc_region_df, how='inner', on='NOC')

# Anonymisera kolumnen med idrottarnas namn med hashfunktionen SHA-256
os_data["Name_hash"]=os_data["Name"].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
os_hash_name = os_data.drop(columns="Name")

# Bygg Dash App
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

#ChatGpt give  av Css card 
card_style = {
    "padding": "20px",
    "margin": "10px",
    "borderRadius": "10px",
    "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
    "backgroundColor": "lightsteelblue"
}
# Bygg layout för landstatistik
country_layout = html.Div([
    html.H1('OS Dashbord'),
    html.Div([
        html.H2('Landstatistik'),
    # Menu för välj ett land
        html.P("Välj ett land"),
        dcc.RadioItems(
            id='country',
            options=[
                {'label':'Alla länder','value':'all' },
                {'label':'Österrike','value':'Austria'},
                ],
            value = 'all',
        )
    ], style =card_style),
    # Menu för välj en graf
    html.Div([
        html.P("Välj en graf"),
        dcc.Dropdown(
            id = 'country_graph',
            options = [
                {'label':"Topp 10 sport",'value':"topp10"},
                {'label':'Antal medaljer per OS','value':'medal'},
                {'label':'Histogram över åldrar', 'value':'age'},
                ],
            value = 'topp10',
        )
    ], style = card_style),
    html.Div ([
        dcc.Graph(id='graph_output')
    ], style=card_style), 
    html.Div([dcc.Link('Till Sportstatistik', href='/sport')], style = card_style)
],
style={
    "backgroundColor": "#f2f2f2",
    "padding": "20px"
    }
)


#   Skapa input och output  
@app.callback(
    Output('graph_output','figure'),
    [
        Input('country','value'),
        Input('country_graph','value'),
    ]
)
def graph_output (country, c_graph):
    
    if country == 'all':
        df = os_hash_name
    elif country =='Austria':
        df = os_hash_name[os_hash_name["Team"]=="Austria"]
    
    if c_graph == 'topp10':
        df_topp10 = df.groupby("Sport")["Medal"].count().sort_values(ascending = False).reset_index().head(10)
        fig = px.bar(df_topp10,x="Medal",y="Sport",color="Sport", title = "Topp 10 Sport")
    elif c_graph == 'medal':
        df_y = df.groupby("Year")["Medal"].count().reset_index()
        fig = px.bar(df_y, x="Year",y="Medal", title = "Numbel of medal per OS")
    elif c_graph == 'age':
        fig = px.histogram(df, x = "Age",nbins =20, color = "Sex",color_discrete_map={"F": "pink","M": "blue"},title="Åldersfördelning")
    return fig

# layout för sports statistik
sport_layout = about_layout = html.Div([
    html.H1("Sport statistik"),
    html.Div([
        html.P("Välj sport"),
        dcc.Dropdown(id='sport_name',
                    options=['Alpine Skiing', 
                                'Football', 
                                'Gymnastics', 
                                "Handball"],
                        value="Alpine Skiing")],style =card_style),
    html.Div([
        html.P("Välj plot"),                    
        dcc.Dropdown(id='sport_plot',
                    options=['plot_age_distribution', 
                                'plot_medal_distribution', 
                                'plot_age_by_gender', 
                                "plot_events_by_year", 
                                "plot_medals_per_athlete"],
                        value="plot_age_distribution")], style =card_style),
    html.Div([dcc.Graph(id="graph_sport_output")], style =card_style),
    html.Div([dcc.Link('Till landstatistik', href='/country')],style =card_style)
],
style={
    "backgroundColor": "#f2f2f2",
    "padding": "20px"
    }
)

@app.callback(
    Output('graph_sport_output','figure'),
    Input('sport_name','value'),
    Input('sport_plot','value'),
)
def update_sport_graph(sport_name, sport_plot): 
    fig = graph_sport_output(os_hash_name, sport_name, sport_plot) 
    return fig

# Layout för multipage  
app.layout = html.Div([
     dcc.Location(id = 'url',refresh = False),
     html.Div(id = 'page-content')
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/' or pathname =='/country':
        return country_layout
    elif pathname == '/sport':
        return sport_layout
    else:
        return '404 - Sidan kunde inte hittas'
    
if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8030, debug=True)
    app.run (debug = False)