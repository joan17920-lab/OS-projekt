import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Funktionen för att plotta diagram
def graph_sport_output (os_hash_name, sport_name, sport_plot): 
    df = os_hash_name[os_hash_name["Sport"]==sport_name]

    if sport_plot == "plot_age_distribution":  
        fig = px.histogram(df, x="Age", nbins=20)
    
    elif sport_plot == "plot_medal_distribution": 
        medal_distribution = df.groupby(['region', 'Medal']).size().unstack(fill_value=0)
        fig = px.bar(medal_distribution,y=['Bronze', 'Gold', 'Silver'],title=f'Medal Distribution in {sport_name}')

    elif sport_plot == "plot_age_by_gender":        
        fig = px.box(df,x='Sex', y='Age')

    elif sport_plot == "plot_events_by_year":  
        events_per_year = df.groupby('Year')['Event'].nunique()
        fig = px.bar(events_per_year, x= events_per_year.index,y= events_per_year.values)

    elif sport_plot == "plot_medals_per_athlete": 
        MedalsPerCountry = df.groupby(by="region")["Medal"].count()
        MedalsPerCountry_sorted = MedalsPerCountry.sort_values(ascending=False).reset_index()

        AthletePerCountry = df.groupby(by="region")["ID"].count()
        AthletePerCountry_sorted = AthletePerCountry.sort_values(ascending=False).reset_index()

        MedalsPerContestant = pd.merge(MedalsPerCountry_sorted, AthletePerCountry_sorted, how="inner" )
        MedalsPerContestant["Medal per ID %"] = 100 * MedalsPerContestant["Medal"] / MedalsPerContestant["ID"]  # Calculating medals per athlete quotient
        MedalsPerContestant = MedalsPerContestant.sort_values(by="Medal per ID %", ascending=False).head(10)   # Excluding countries with lower quotient than 0.1%
        fig = px.bar(MedalsPerContestant, x="Medal per ID %", y="region")
    elif sport_plot == "plot_sankey_for_austria":
        aust = df[df['region'] == 'Austria'].copy()
 
        aust['Medal'] = aust['Medal'].fillna('No Medal')
    
        sexes = list(aust['Sex'].unique())
        medals = list(aust['Medal'].unique())
        years = list(aust['Year'].unique())
    
        labels = sexes + medals + years
    
        index_map = {label: i for i, label in enumerate(labels)}
    
        sex_to_medal = aust.groupby(['Sex', 'Medal']).size().reset_index(name='count')
    
        medal_to_year = aust.groupby(['Medal', 'Year']).size().reset_index(name='count')
    
        sources = []
        targets = []
        values = []
    
        for _, row in sex_to_medal.iterrows():
            sources.append(index_map[row['Sex']])
            targets.append(index_map[row['Medal']])
            values.append(row['count'])
    
        for _, row in medal_to_year.iterrows():
            sources.append(index_map[row['Medal']])
            targets.append(index_map[row['Year']])
            values.append(row['count'])
    
        fig = go.Figure(data=[go.Sankey(
            node=dict(label=labels, pad=15, thickness=20),
            link=dict(source=sources, target=targets, value=values)
        )])
    
        fig.update_layout(title_text=f"Sankey Diagram – {sport_name} (Austria)", font_size=12)
    elif sport_plot == "plot_best_result_age":
        df_new = df.dropna(subset="Medal")
        w_df = df_new.groupby("Year")["Age"].mean().reset_index()
        fig = px.line(w_df, x="Year", y="Age")
    elif sport_plot == "plot_age_distribution_by_sex":
        fig = px.histogram(df.dropna(subset=["Age"]), x="Age", color="Sex", nbins=20)
    else:
        fig = px.histogram(df, x = "Age",nbins =20, color = "Sex",color_discrete_map={"F": "pink","M": "blue"},title="Åldersfördelning")
    
    return fig
