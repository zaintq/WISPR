#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx
from mpl_toolkits.basemap import Basemap
from matplotlib_scalebar.scalebar import ScaleBar

def main():
    G = nx.Graph()
    G = nx.read_gpickle("mendocino.gpickle")

    ###############################################################################
    # The following code is just for plotting a figure.
    ###############################################################################
    m = Basemap(
            projection='merc',
            ellps = 'WGS84',
            llcrnrlon=-123.85,
            llcrnrlat=38.7,
            urcrnrlon=-123.5,
            urcrnrlat=39.3,
            lat_ts=0,
            epsg = 4269,
            resolution='h',
            suppress_ticks=True)

    colors = []
    size = []
    for node in G.nodes():
        lat,lng =  G.node[node]['pos']
        if lat == 0 or lng == 0:
            G.remove_node(node)
            continue
        nodetype = G.node[node]['type']
        if nodetype == 'cpe':
            #G.remove_node(node)
            #colors.append('b')
            #size.append(5)
            continue
        #elif nodetype == 'wireless-bridge-master':
            #colors.append('k')
            #size.append(20)
        #elif nodetype == 'wireless-bridge-client':
        #    colors.append('w')
        #    size.append(20)
        #elif nodetype == 'router':
        #    colors.append('yellow')
        #    size.append(35)
        #elif 'switch' in nodetype:
        #    colors.append('green')
        #    size.append(5)
        else:
            colors.append('red')
            size.append(25)

    edges,edgecolors = zip(*nx.get_edge_attributes(G,'color').items())
    m.arcgisimage(service='World_Shaded_Relief', xpixels = 5000, verbose= True,dpi=300)
    scalebar = ScaleBar(101233.3,length_fraction=0.3) # 1 pixel = 6.074  meter
    plt.gca().add_artist(scalebar)
    nx.draw(G, nx.get_node_attributes(G, 'pos'), node_color=colors, with_labels=False, weight=0.25, node_size=size)
    plt.savefig("mendocino_topologymap.pdf",bbox_inches='tight',dpi=300)

if __name__ == "__main__":
    main()