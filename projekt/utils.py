import pandas as pd
import plotly.express as px
import seaborn as sns



def graph_sport_output (os_hash_name, sport_name, sport_plot): 
    df = os_hash_name[os_hash_name["Sport"]==sport_name]

    if sport_plot == "plot_age_distribution":   # Taken from Kehua. sns.histplot() -> px.histogram()
        fig = px.histogram(df, x="Age", nbins=20)
    
    elif sport_plot == "plot_medal_distribution": # Failing.
        medal_distribution = df.groupby(['region', 'Medal']).size().unstack(fill_value=0)
        fig = medal_distribution.plot(kind='bar', stacked=True, title=f'Medal Distribution in {sport_name}')

    elif sport_plot == "plot_age_by_gender":    #Failing
        fig = sns.boxplot(x='Sex', y='Age', data=df)

    elif sport_plot == "plot_events_by_year":   # Taken from Kehua. sns.boxplot() -> px.histogram()
        fig = px.histogram(df, x='Year')

    elif sport_plot == "plot_medals_per_athlete":   # Taken from Philips Alpine_Skiing sns.barplot() -> px.bar()
        MedalsPerCountry = df.groupby(by="region")["Medal"].count()
        MedalsPerCountry_sorted = MedalsPerCountry.sort_values(ascending=False).reset_index()

        AthletePerCountry = df.groupby(by="region")["ID"].count()
        AthletePerCountry_sorted = AthletePerCountry.sort_values(ascending=False).reset_index()

        MedalsPerContestant = pd.merge(MedalsPerCountry_sorted, AthletePerCountry_sorted, how="inner" )
        MedalsPerContestant["Medal per ID %"] = 100 * MedalsPerContestant["Medal"] / MedalsPerContestant["ID"]  # Calculating medals per athlete quotient
        MedalsPerContestant = MedalsPerContestant.sort_values(by="Medal per ID %", ascending=False).head(10)   # Excluding countries with lower quotient than 0.1%
        fig = px.bar(MedalsPerContestant, x="Medal per ID %", y="region")

    else:
        fig = px.histogram(df, x = "Age",nbins =20, color = "Sex",color_discrete_map={"F": "pink","M": "blue"},title="Åldersfördelning")
        print(f"{sport_plot} saknar tillhörande graf. Kolla att din önskade graf finns i utilis.py")
    
    return fig
