import pandas as pd
import geopandas as gpd
import movingpandas as mpd
import matplotlib.pyplot as plt
import geoviews as gv
import geodatasets 
from shapely.geometry import Point
from datetime import datetime, timedelta 
from os.path import exists
from urllib.request import urlretrieve

def get_osm_traces(page=0, bbox='16.18,48.09,16.61,48.32'):
    file = 'osm_traces.gpx'
    url = f'https://api.openstreetmap.org/api/0.6/trackpoints?bbox={bbox}&page={page}'
    if not exists(file):
        urlretrieve(url, file)
    gdf = gpd.read_file(file, layer='track_points')
    # dropping empty columns
    gdf.drop(columns=['ele', 'course', 'speed', 'magvar', 'geoidheight', 'name', 'cmt', 'desc',
       'src', 'url', 'urlname', 'sym', 'type', 'fix', 'sat', 'hdop', 'vdop',
       'pdop', 'ageofdgpsdata', 'dgpsid'], inplace=True) 
    gdf['t'] = pd.to_datetime(gdf['time'])
    gdf.set_index('t', inplace=True)
    return gdf


with open("out.txt", "w") as outfile:
    outfile.write("Hello world! :-) \n")


chicago = gpd.read_file(geodatasets.get_path("geoda.chicago_commpop"))
chicago.plot(column="POP2010")
plt.savefig("gpd-plot.png")


df = pd.DataFrame([
  {'geometry':Point(0,0), 't':datetime(2018,1,1,12,0,0)},
  {'geometry':Point(6,0), 't':datetime(2018,1,1,12,6,0)},
  {'geometry':Point(6,6), 't':datetime(2018,1,1,12,10,0)},
  {'geometry':Point(9,9), 't':datetime(2018,1,1,12,15,0)}
]).set_index('t')
gdf = gpd.GeoDataFrame(df, crs=31256)
toy_traj = mpd.Trajectory(gdf, 1)

t = datetime(2018,1,1,12,7,0)
point = toy_traj.get_position_at(t, method="interpolated")
point = gpd.GeoSeries([point])

ax = toy_traj.plot(column="speed", cmap="PRGn")
point.plot(ax=ax, color='hotpink', markersize=100)
plt.savefig("mpd-plot.png")


gdf = get_osm_traces()
osm_traces = mpd.TrajectoryCollection(gdf, 'track_fid')
osm_traces = mpd.MinTimeDeltaGeneralizer(osm_traces).generalize(tolerance=timedelta(minutes=1))
osm_traces.hvplot(title='OSM Traces', line_width=7, width=700, height=500)
geoviews_plot = osm_traces.get_trajectory(0).hvplot(
    title='Speed (m/s) along track', c='speed', cmap='RdYlBu',
    line_width=7, width=700, height=500, tiles='CartoLight', colorbar=True)
gv.save(geoviews_plot, "mpd-hvplot.png")
