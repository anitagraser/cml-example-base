import pandas as pd
import geopandas as gpd
import movingpandas as mpd
import matplotlib.pyplot as plt
import geoviews as gv
import geodatasets 
from shapely.geometry import Point
from datetime import datetime, timedelta 
from pathlib import Path
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


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
toy_traj.add_speed()

t = datetime(2018,1,1,12,7,0)
point = toy_traj.get_position_at(t, method="interpolated")
point = gpd.GeoSeries([point])

ax = toy_traj.plot(column="speed", cmap="PRGn")
point.plot(ax=ax, color='hotpink', markersize=100)
plt.savefig("mpd-plot.png")

geoviews_plot = toy_traj.hvplot(
    title='Speed (m/s) along track', c='speed', cmap='RdYlBu',
    line_width=7, width=700, height=500, tiles='CartoLight', colorbar=True)

options = Options()
options.add_argument("--headless")
driver = Firefox(
    options=options,
    executable_path=str(Path("/__w/cml-example-base/cml-example-base/3/envs/mpd/bin/geckodriver")))

gv.save(geoviews_plot, "mpd-hvplot.png", webdriver=driver)

