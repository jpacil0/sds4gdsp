import os
import shapely
import geopandas as gpd
import matplotlib.pyplot as plt
from PIL import Image

def get_route_fig(r):
    fig, ax = plt.subplots(1, 1)
    gpd.GeoSeries(r).plot(ax=ax, linewidth=5, zorder=1)
    orig = shapely.geometry.Point([r.xy[0][0], r.xy[1][0]])
    dest = shapely.geometry.Point([r.xy[0][-1], r.xy[1][-1]])
    gpd.GeoSeries(orig).plot(ax=ax, color="red", markersize=250, zorder=2, alpha=0.8)
    gpd.GeoSeries(dest).plot(ax=ax, color="green", markersize=250, zorder=2, alpha=0.8)
    plt.axis("off")
    ax.ticklabel_format(useOffset=False)
    plt.close()
    return fig

def load_images(dirpath, extension=".jpg"):
    imgs = []
    for f in sorted(os.listdir(dirpath)):
        if f.endswith(extension):
            img_path = os.path.join(dirpath, f)
            imgs.append(Image.open(img_path))
    return imgs

def plot_images(imgs, nrows=5, ncols=6, figsize=(10, 10)):
    num_figs = nrows * ncols
    num_imgs = len(imgs)
    num_figs = min(num_figs, num_imgs)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    for i, ax in enumerate(axes.flat):
        if i < num_imgs:
            ax.imshow(imgs[i])
        ax.axis("off")
    plt.tight_layout()
    plt.show()
    return fig

def visualize_route(traj):
    coords = traj.coords.tolist()
    od_pairs = list(zip(coords, coords[1:]))
    routes = []
    for od_pair in od_pairs:
        routes.append(
            shapely.geometry.LineString(
                map(shapely.wkt.loads, od_pair)
            )
        )
    fig, ax = plt.subplots(1, figsize=(7, 5))
    gpd.GeoSeries(traj["coords"].apply(shapely.wkt.loads)).plot(ax=ax, color="blue", markersize=60, zorder=2);
    gpd.GeoSeries(traj.head(1)["coords"].apply(shapely.wkt.loads)).plot(ax=ax, color="green", markersize=120, zorder=3);
    gpd.GeoSeries(traj.tail(1)["coords"].apply(shapely.wkt.loads)).plot(ax=ax, color="red", markersize=120, zorder=3);
    gpd.GeoSeries(routes).plot(ax=ax, color="grey", linewidth=3, zorder=1, alpha=0.6)
    ax.ticklabel_format(useOffset=False)
    ax.legend(["_", "orig", "dest"])
    plt.tight_layout()
    plt.axis("off")
    plt.close()
    return fig

def get_day_in_a_life():
    return 1