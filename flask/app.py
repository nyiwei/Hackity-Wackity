from flask import Flask, render_template, request, jsonify
import folium
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import requests

app = Flask(__name__)
crime = pd.read_csv('static/dataset.csv')

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Map routes
@app.route('/map1')
def map1():
    df = gpd.read_file('static/SingaporePoliceForceNPCBoundary.geojson')
    df["Description"] = df["Description"].str.split('<td>')
    df["Description"] = df["Description"].str[1]

    df["Description"] = df["Description"].str.split('<')
    df["Description"] = df["Description"].str[0]

    df_temp = df[~df['Description'].str.contains("M-Sect") & ~df['Description'].str.contains("S-Sect")]

    #df_temp = df[df['Description'].str.contains("SG-NPC")]

    # Get unique descriptions
    unique_descriptions = df["Description"].unique()

    # Generate colors
    num_colors = len(unique_descriptions)
    colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a',
            '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94',
            '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d',
            '#17becf', '#9edae5', '#393b79', '#5254a3', '#6b6ecf', '#9c9ede',
            '#637939', '#8ca252', '#b5cf6b', '#cedb9c', '#8c6d31', '#bd9e39',
            '#e7ba52', '#e7cb94', '#843c39', '#ad494a', '#d6616b', '#e7969c',
            '#7b4173', '#a55194', '#ce6dbd']

    color_map = dict(zip(unique_descriptions, colors))

    m = folium.Map(location=[crime['lat'].mean(), crime['long'].mean()], zoom_start=12)
    for _, row in df_temp.iterrows():
        description = row["Description"]
        color = color_map[description]
        #print(color)
        style = { 'color': color, 'weight': 2}  # Change the outline color
        popup = folium.Popup(description, parse_html=True)
        folium.GeoJson(row.geometry, style_function=lambda x, style=style: style, popup=popup).add_to(m)


    crime_sub = crime[:200]
    geometry_points = [Point(xy) for xy in zip(crime_sub['long'], crime_sub['lat'])]
    gdf_points = gpd.GeoDataFrame(crime_sub, geometry=geometry_points)

    # Create an empty list to store the associated descriptions
    associated_descriptions = []

    # Loop through each poisnt and check which polygon contains it
    for idx, point in gdf_points.iterrows():
        for idx_polygon, polygon in df.iterrows():
            if polygon['geometry'].contains(point['geometry']):
                associated_descriptions.append(polygon['Description'])
                break  # Once the point is found in a polygon, exit the loop

    crime_sub['associated_description'] = associated_descriptions

    for _, row in crime_sub.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["long"]],
            radius=10, 
            color=color_map.get(row["associated_description"], "gray"),
            fill=True,
            fill_color=color_map.get(row["associated_description"], "gray"),
            fill_opacity=0.7,
            popup=folium.Popup(str(row["Severity"]), parse_html=True)
        ).add_to(m)


    
    # Get HTML representation of the map
    map_html = m._repr_html_()

    return render_template('map.html', map_html=map_html)

@app.route('/map2')
def map2():
    
    return render_template('map2.html')

@app.route('/generate_coordinates', methods=['POST'])
def generate_coordinates():
    r = crime.sample()
    lat = r.lat.values[0]
    long = r.long.values[0]
    return jsonify({'lat': lat, 'long': long})

@app.route('/get_nearest_npc', methods=['POST'])
def get_nearest_npc():
    data = request.json
    lat = data['lat']
    long = data['long']
    
    url = "https://www.onemap.gov.sg/api/common/elastic/search?searchVal=neighbourhood%police&returnGeom=Y&getAddrDetails=N"
     
    response = requests.request("GET", url)
     
    search_results = response.json()
    
    nearest_npc = None
    min_dist = float("inf")

    for result in search_results["results"]:
        npc_lat = float(result['LATITUDE'])
        npc_long = float(result['LONGITUDE'])
        distance = ((lat - npc_lat)**2 + (long - npc_long)**2)**0.5
        if distance < min_dist:
            min_dist = distance
            nearest_npc = (npc_lat, npc_long)
    
    if nearest_npc:
        nearest_npc_lat, nearest_npc_long = nearest_npc
        return jsonify({'lat': nearest_npc_lat, 'long': nearest_npc_long})
    else:
        return jsonify({'error': 'No NPC found'}), 404

@app.route('/get_route', methods=['POST'])
def get_route():
    data = request.json
    start = data['start']
    end = data['end']

    params = {
        'start': f'{start[0]},{start[1]}',
        'end': f'{end[0]},{end[1]}',
        'routeType': 'walk',
        'token': ONEMAP_TOKEN
    }

    response = requests.get(ONEMAP_API_URL, params=params)
    route_data = response.json()
    
    return jsonify(route_data)


# Navigation bar
@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

if __name__ == '__main__':
    app.run(debug=True)
