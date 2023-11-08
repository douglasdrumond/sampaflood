import geopandas as gp
import libpysal as ps
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from mgwr.gwr import GWR, MGWR
from mgwr.sel_bw import Sel_BW
from mgwr.utils import compare_surfaces, truncate_colormap


def run_mgwr():
    georgia = gp.read_file(ps.examples.get_path('G_utm.shp'))
    fig, ax = plt.subplots(figsize=(10, 10))
    georgia.plot(ax=ax, **{'edgecolor': 'black', 'facecolor': 'white'})
    georgia.centroid.plot(ax=ax, c='black')
    plt.savefig('georgia_shp')
    plt.show()

    prenz = gp.read_file(ps.examples.get_path('prenzlauer.zip'))
    prenz_bound = gp.read_file(ps.examples.get_path('prenz_bound.zip'))
    fig, ax = plt.subplots(figsize=(10, 10))
    prenz_bound.plot(ax=ax, **{'edgecolor': 'black', 'facecolor': 'white'})
    prenz.plot(ax=ax, markersize=10, **{'edgecolor': 'black', 'facecolor': 'black'})
    plt.savefig('prenz')
    plt.show()

    # Prepare Georgia dataset inputs
    g_y = georgia['PctBach'].values.reshape((-1, 1))
    g_X = georgia[['PctFB', 'PctBlack', 'PctRural']].values
    u = georgia['X']
    v = georgia['Y']
    g_coords = list(zip(u, v))

    # Prepare Berlin dataset inputs
    # Take the logarithm of the price variable to correct for skewing
    b_y = np.log(prenz['price'].values.reshape((-1, 1)))
    b_X = prenz[['review_sco', 'accommodat', 'bathrooms']].values
    u = prenz['X']
    v = prenz['Y']
    b_coords = list(zip(u, v))

    # Calibrate a GWR model for Georgia dataset using computationally selected~bandwidth
    gwr_selector = Sel_BW(g_coords, g_y, g_X)
    gwr_bw = gwr_selector.search()
    print(gwr_bw)

    gwr_model = GWR(g_coords, g_y, g_X, gwr_bw)

    gwr_results = gwr_model.fit()
    print(gwr_results.resid_ss)


def run_mgwr_sao_paulo():
    sao_paulo = gp.read_file("../database/DEINFO_DISTRITO.shp")
    fig, ax = plt.subplots(figsize=(10, 10))
    sao_paulo.plot(ax=ax, **{'edgecolor': 'black', 'facecolor': 'white'})
    sao_paulo.centroid.plot(ax=ax, c='black')
    plt.savefig('sao_paulo_distritos')
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # run_mgwr()
    run_mgwr_sao_paulo()

