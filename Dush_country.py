import pandas as pd
import os
import plotly.express as px
import hashlib
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

# Läs in data
path = os.path.join(os.getcwd(),"data","athlete_events.csv")
os_data = pd.read_csv(path)
# Anonymisera kolumnen med idrottarnas namn med hashfunktionen SHA-256
os_data["Name_hash"]=os_data["Name"].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
os_hash_name = os_data.drop(columns="Name")

# Bygg Dash App
app = Dash(__name__, suppress_callback_exceptions=True)
# Bygg layout för land
country_layout = html.Div([
    html.H1('OS Dashbord'),
    html.H2('Landstatistik'),
    # Menu för att välja en land
    html.P("Välj a land"),
    dcc.RadioItems(
        id='country',
        options=[
            {'label':'Alla länder','value':'all' },
            {'label':'Östrike','value':'Austria'},
            ],
        value = 'all',
    ),
    # Menu för välj en graf
    html.P("Välj en graf"),
    dcc.Dropdown(
        id = 'country_graph',
        options = [
            {'label':"Topp 10 sport",'value':"topp10"},
            {'label':'Antal medaljer per OS','value':'medal'},
            {'label':'Histogram över åldrar', 'value':'age'},
            ],
        value = 'topp10',
        placeholder="Välj en graf",
    ),
    dcc.Graph(id="graph_output"),
    dcc.Link('Till Sportstatistik', href='/sport')
])

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
    else:
            return "Välj ett land"
    
    if c_graph == 'topp10':
        df_topp10 = df.groupby("Sport")["Medal"].count().sort_values(ascending = False).reset_index().head(10)
        fig = px.bar(df_topp10,x="Medal",y="Sport",color="Sport", title = "Topp10 Sport")
    elif c_graph == 'medal':
        df_y = df.groupby("Year")["Medal"].count().reset_index()
        fig = px.bar(df_y, x="Year",y="Medal", title = "Numbel of medal per OS")
    elif c_graph == 'age':
        fig = px.histogram(df, x = "Age",nbins =20, color = "Sex",color_discrete_map={"F": "pink","M": "blue"},title="Åldersfördelning")
    else:
        return "Välj en graf"
    return fig
# Här kan bygg sida för sport
sport_layout = about_layout = html.Div([
    html.H1("Sport statistik"),
    html.P("Bygg....."),
    dcc.Link('Till ländstatistik', href='/country')
])

app.layout = html.Div([

     dcc.Location(id = 'url',refresh = False),
     html.Div(id = 'page-content')
])
@app.callback(
     Output('page-content','children'),
     Input('url','pathname')
)
def display_page(pathname):
    if pathname == '/' or pathname =='/country':
        return country_layout
    elif pathname == '/sport':
        return sport_layout
    else:
        return '"404 - Sidan kunde inte hittas'
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8030, debug=True)