import pandas as pd
import geopandas as gpd
import movingpandas as mpd
import geodatasets 
import matplotlib.pyplot as plt
from shapely.geometry import Point
from datetime import datetime 


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

