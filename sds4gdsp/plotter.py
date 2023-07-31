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

def plot_total_travel_distance(sample_traj_low, sample_traj_mid, sample_traj_high):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    sample_low = fetch_total_travel_distance(sample_traj_low)
    sample_mid = fetch_total_travel_distance(sample_traj_mid)
    sample_high = fetch_total_travel_distance(sample_traj_high)
    sample_low["orig_dt"] = pd.to_datetime(sample_low["orig_dt"])
    sample_mid["orig_dt"] = pd.to_datetime(sample_mid["orig_dt"])
    sample_high["orig_dt"] = pd.to_datetime(sample_high["orig_dt"])
    sample_low.groupby("orig_dt")["travel_distance"].sum().plot(ax=ax1, color="red", kind="line")
    sample_mid.groupby("orig_dt")["travel_distance"].sum().plot(ax=ax1, color="blue", kind="line")
    sample_high.groupby("orig_dt")["travel_distance"].sum().plot(ax=ax1, color="green", kind="line")
    sample_low.groupby("orig_dt")["travel_distance"].sum().plot(ax=ax2, color="red", kind="density")
    sample_mid.groupby("orig_dt")["travel_distance"].sum().plot(ax=ax2, color="blue", kind="density")
    sample_high.groupby("orig_dt")["travel_distance"].sum().plot(ax=ax2, color="green", kind="density")
    ax1.set_ylabel("travel distance (in KM)")
    ax2.set_ylabel("density")
    ax1.set_xlabel("")
    ax2.set_xlabel("travel distance (in KM)")
    ax1.legend(["low", "mid", "high"], frameon=False)
    ax2.legend(["low", "mid", "high"], frameon=False)
    plt.tight_layout()
    plt.close();
    return fig

def plot_routes(traj_low, traj_mid, traj_high):
    coords_low = traj_low.coords.tolist()
    coords_mid = traj_mid.coords.tolist()
    coords_high = traj_high.coords.tolist()
    od_pairs_low = list(zip(coords_low, coords_low[1:]))
    od_pairs_mid = list(zip(coords_mid, coords_mid[1:]))
    od_pairs_high = list(zip(coords_high, coords_high[1:]))
    routes_low, routes_mid, routes_high = [], [], []
    for od_pair in od_pairs_low:
        routes_low.append(
            shapely.geometry.LineString(
                map(shapely.wkt.loads, od_pair)
            )
        )
    for od_pair in od_pairs_mid:
        routes_mid.append(
            shapely.geometry.LineString(
                map(shapely.wkt.loads, od_pair)
            )
        )
    for od_pair in od_pairs_high:
        routes_high.append(
            shapely.geometry.LineString(
                map(shapely.wkt.loads, od_pair)
            )
        )
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(13, 5), sharex=True, sharey=True)
    gpd.GeoSeries(traj_low["coords"].apply(shapely.wkt.loads)).plot(ax=ax1, color="red", markersize=60, zorder=2);
    gpd.GeoSeries(traj_mid["coords"].apply(shapely.wkt.loads)).plot(ax=ax2, color="blue", markersize=60, zorder=2);
    gpd.GeoSeries(traj_high["coords"].apply(shapely.wkt.loads)).plot(ax=ax3, color="green", markersize=60, zorder=2);
    gpd.GeoSeries(routes_low).plot(ax=ax1, color="grey", linewidth=3, zorder=1, alpha=0.6)
    gpd.GeoSeries(routes_mid).plot(ax=ax2, color="grey", linewidth=3, zorder=1, alpha=0.6)
    gpd.GeoSeries(routes_high).plot(ax=ax3, color="grey", linewidth=3, zorder=1, alpha=0.6)
    ax1.ticklabel_format(useOffset=False)
    ax2.ticklabel_format(useOffset=False)
    ax3.ticklabel_format(useOffset=False)
    ax1.axis("off")
    ax2.axis("off")
    ax3.axis("off")
    ax1.legend(["low"], frameon=False, loc="lower center")
    ax2.legend(["mid"], frameon=False, loc="lower center")
    ax3.legend(["high"], frameon=False, loc="lower center")
    plt.tight_layout()
    plt.close()
    return fig

def get_day_in_a_life():
    return 1