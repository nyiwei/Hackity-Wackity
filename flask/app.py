from flask import Flask, render_template
import folium
import geopandas
import pandas as pd

app = Flask(__name__)
crime = pd.read_csv('static/dataset.csv')

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Map routes
@app.route('/map1')
def map1():
    df = geopandas.read_file('static/SingaporePoliceForceNPCBoundary.geojson')
    df["Description"] = df["Description"].str.split('<td>')
    df["Description"] = df["Description"].str[1]

    df["Description"] = df["Description"].str.split('<')
    df["Description"] = df["Description"].str[0]

    df_temp = df[~df['Description'].str.contains("M-Sect") & ~df['Description'].str.contains("S-Sect")]
    m = folium.Map(location=[crime['lat'].mean(), crime['long'].mean()], zoom_start=12)
    folium.GeoJson(df_temp).add_to(m)

    for each in crime[:100].iterrows():
        folium.Marker(
            location = [each[1]["lat"],each[1]["long"]],
            clustered_marker = True).add_to(m)

    
    # Get HTML representation of the map
    map_html = m._repr_html_()

    return render_template('map.html', map_html=map_html)

@app.route('/map2')
def map2():
    # Create a simple Folium map
    m = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
    folium.Marker([51.5074, -0.1278], popup='<b>London</b>').add_to(m)
    
    # Get HTML representation of the map
    map_html = m._repr_html_()

    return render_template('map.html', map_html=map_html)

# Navigation bar
@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

if __name__ == '__main__':
    app.run(debug=True)
