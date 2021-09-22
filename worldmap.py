import folium
import pandas

data = pandas.read_csv("volcanosbig.csv")   #database of volcanos
lat = list(data["Latitude"])
lon = list(data["Longitude"])
elev = list(data["Elevation (m)"])
name = list(data["Volcano Name"])

map = folium.Map(location=[20.2830, -103.4252], zoom_start=5, tiles="Stamen Terrain") #Jocotepec, MX
fgv=folium.FeatureGroup(name="Volcanos")
fgp=folium.FeatureGroup(name="Population")      #adding layers

html = """      
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""             #adds google search to popups

def color_producer(elevation):  # function colors popups by elevation
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

def mapit(lat,lon,elev,name):   #function adds the popup markers
    for lt, ln, el, name in zip(lat, lon,elev, name):
        iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
        fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=folium.Popup(iframe),
        fill_color=color_producer(el), color = "grey", fill = True, fill_opacity=0.7))
        

mapit(lat, lon, elev, name) #add popups

#adds color layer for population
fgp.add_child(folium.GeoJson(data=open("world.json", 'r', encoding='utf-8-sig').read(),
style_function=lambda x:( {'fillColor':'green' if x['properties']['POP2005']< 50000000
else 'orange' if 5000000 <= x['properties']['POP2005'] < 200000000 else 'red'})))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())    #creates layer control for volcano and population layers

map.save("Interactive_World_Map.html")
