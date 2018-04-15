import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex, Normalize
from matplotlib.patches import Polygon
from matplotlib.colorbar import ColorbarBase
import pandas as pd
import numpy as np
import seaborn as sns
sns.set(color_codes=True)

# this code is for plotting the map visualizations and viewing distribution and descriptive statistics of the results
# followed example for plotting to US states here: https://github.com/matplotlib/basemap/blob/master/examples/fillstates.py


# Plotting to map
def plot_map(subreddit, state_averages):
    """Plots

            Args:
                subreddit (string): Subreddit of interest
                state_averages (dataframe): dataframe of resulting partipation rates

            Returns:
                plots data to map of US states

    """

    fig, ax = plt.subplots()

    # Lambert Conformal map of lower 48 states.
    m = Basemap(llcrnrlon=-119,llcrnrlat=20,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

    # draw boundaries
    shp_info = m.readshapefile('st99_d00','states',drawbounds=True,
                               linewidth=0.45,color='gray')

    # input subreddit
    subreddit_of_interest = subreddit

    colors={}
    statenames=[]
    cmap = plt.cm.YlGnBu # use Yellow Green Blue colormap
    vmin = .95*(min(state_averages[subreddit_of_interest])); vmax = 1.05*(max(state_averages[subreddit_of_interest]))
    norm = Normalize(vmin=vmin, vmax=vmax)
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        # remove Alaska, Hawaii, DC and Puerto Rico.
        if statename not in ['Alaska', 'Hawaii', 'District of Columbia','Puerto Rico']:
            participation = state_averages[subreddit_of_interest][statename]
            colors[statename] = cmap(np.sqrt((participation-vmin)/(vmax-vmin)))[:3]
        statenames.append(statename)

    # Color each state
    for nshape,seg in enumerate(m.states):
        # remove Alaska, Hawaii, DC and Puerto Rico.
        if statenames[nshape] not in ['Alaska', 'Hawaii', 'Puerto Rico', 'District of Columbia']:
            color = rgb2hex(colors[statenames[nshape]])
            poly = Polygon(seg,facecolor=color,edgecolor=color)
            ax.add_patch(poly)


    # make legend
    ax_c = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    cb = ColorbarBase(ax_c,cmap=cmap,norm=norm,orientation='vertical',
                    label=r'User Participation Rate')

    plt.show()

if __name__ == '__main__':


    # import data and set index to state
    state_averages = pd.read_csv('state_averages.csv')
    state_averages = state_averages.set_index('State')

    # plot participation rate maps for each mental health subreddit and the total of all 'total_average'
    plot_map('Anxiety',state_averages)
    plot_map('SanctionedSuicide',state_averages)
    plot_map('SuicideWatch',state_averages)
    plot_map('addiction',state_averages)
    plot_map('depression',state_averages)
    plot_map('mentalhealth',state_averages)
    plot_map('total_average',state_averages)
    plot_map('total_average_no_suicide',state_averages)
    plot_map('total_average_suicide',state_averages)

    # plot distribution of total average participation rates
    sns.distplot(state_averages['total_average'], bins=8,kde=True, rug=True);


    # calculate descriptive statistcs of the total average participation
    np.std(state_averages['total_average'])
    state_averages['total_average'].mean()
    state_averages['total_average'].min()
    state_averages['total_average'].max()





