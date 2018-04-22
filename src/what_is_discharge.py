# interactive backwater module written by Andrew J. Moodie
# see module and website for more information
# classroom module for this model can be found at 
# http://www.coastalsustainability.rice.edu/outreach/
# the model setup below is parameterized to the Lower Mississippi River
# as established by Nittrouer et al., 
# Spatial and temporal trends, GSAB, 2012


# IMPORT LIBLARIES
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widget
import matplotlib.patches as ptch
import utils
from river import River

# SET PARAMETERS
Bc = 600 # channel width
Bf = Bc*3 # floodplain width
S0 = 1e-4 # channel slope
Cfc = 0.005 # channel friction coefficient
Cff = 0.01 # floodplain friction coefficient
g = 9.81

xmin = -Bf
xmax = Bf

Q = Qinit = 100
Qbf = 600
Qmin = 50

Hninit = channel_geom.get_flowdepth(Qinit, Bc, Cfc, Cff, S0, g, Qbf)
Hnmax = channel_geom.get_flowdepth(Qbf, B, Cfc, Cff, S0, g, Qbf)

x = channel_geom.make_xcoords(B)
y = channel_geom.make_ycoords(x, Hninit, Hnmax)
bed_patch = channel_geom.channel_bed(x, xmin, xmax)

ymin = np.floor(-Hnmax)


# DEFINE FUNCTIONS
def update(val):
    Q = slide_Q.val
    Hn = channel_geom.get_flowdepth(Q, B, Cfc, Cff, S0, g, Qbf)
    y = channel_geom.make_ycoords(x, Hn, Hnmax)

    water_shade.set_xy(np.column_stack((x, y)))

    fig.canvas.draw_idle()


# H = hydro.get_backwater_dBdx(eta, S, B, H0, Cf, Q, nx, dx)
# Xs = hydro.find_backwaterregion(H, dx)
# # zed = 0.5 + -1e-5*(x - (L*mou)) + hydro.get_backwater_dBdx(eta, S, B, H0, Cf, Qbf, nx, dx)
# zed = 0.5 + hydro.get_backwater_dBdx(eta, S, B, H0, Cf, Qbf, nx, dx)

# nitt_bed, nitt_water = channel.load_nitt()
# nitt_water_dict = [{'10,000 m$^3$/s':nitt_water.hdr.index('f5k_10k')},
#                    {'20,000 m$^3$/s':nitt_water.hdr.index('f15k_20k')},
#                    {'35,000 m$^3$/s':nitt_water.hdr.index('f30k_35k')}]
# nitt_water_dict_idx = np.array( [ list(d.values()) for d in nitt_water_dict ] )
# nitt_water.seldata = nitt_water.data[:, nitt_water_dict_idx.flatten()]

# setup the figure
plt.rcParams['toolbar'] = 'None'
plt.rcParams['figure.figsize'] = 11, 7
fig, ax = plt.subplots()
fig.canvas.set_window_title('SedEdu -- River Discharge: Part I')
plt.subplots_adjust(left=0.075, bottom=0.5, top=0.95, right=0.95)
background_color = 'white'
ax.set_xlabel("cross-channel coordinate")
ax.set_ylabel("elevation (m)")
plt.ylim(ymin, 1.5)
plt.xlim(xmin, xmax)
# ax.xaxis.set_major_formatter( plt.FuncFormatter(lambda v, x: int(-1*(v - (L/1000*mou)))) )

# add plot elements
# RK_line = plt.plot(np.tile(L/1000*mou - RKs, (2, 1)),
#                    np.tile(np.array([-50, 100]), (np.size(RKs), 1)).transpose(), 
#                    ls=':', lw=1.5, color='grey')
# eta_line, = plt.plot(x/1000, eta, lw=2, color='black') # plot bed
# eta_shade = ax.add_patch(ptch.Polygon(utils.format_polyvects(
#                          x/1000, x/1000, -50*np.ones(np.size(eta)), eta),
#                          facecolor='saddlebrown'))

zero_line = plt.plot([xmin, xmax], [0, 0], 'k--', lw=1.2) # plot zero
water_shade = ax.add_patch(ptch.Polygon(np.column_stack((x, y)), facecolor='powderblue'))
# bed_line = ax.plot(x, cbed, lw=1.5)
bed_line = ax.add_patch(ptch.Polygon(bed_patch, lw=1.5, facecolor='sienna'))


# RK_labels = [plt.text(x, y, '< '+s, backgroundcolor='white') 
#                                for x, y, s in zip(L/1000*mou - RKs + 6, 
#                                [6, 20, 70, 80, 90], # 85-np.arange(0,np.size(RKs))*5 
#                                RKnames)]
# ax.set_prop_cycle(plt.cycler('color', ['green', 'gold', 'red']))
# nitt_water_line = plt.plot(np.tile((L/1000*mou - np.array(nitt_water.RK)).transpose(), (1,3)),
#                            nitt_water.seldata, lw=1.5)
# nitt_water_legend = ax.legend([l for l in nitt_water_line], 
#                               [ str(list(d.keys())[0]) for d in nitt_water_dict ])
# for l in nitt_water_line:
#     l.set_visible(False)
# nitt_water_legend.set_visible(False)
# nitt_bed_line, = plt.plot(L/1000*mou - nitt_bed.data[:,0], nitt_bed.data[:,1],
#                          '.', color='grey', visible=False)
# Q_val = plt.text(0.05, 0.85, "Q = " + utils.format_number(Q),
#                   fontsize=16, transform=ax.transAxes, 
#                   backgroundcolor='white')
# Bw_val = plt.text(( (Xs[1]-Xs[0])/2 + Xs[0])/1000, 45, 
#     "backwater from \n" + "RK " + str(int(L*mou/1000-Xs[0]/1000)) +
#     " to " + str(int(L*mou/1000-Xs[1]/1000)), 
#     horizontalalignment="center", backgroundcolor="white")
# Bw_brack, = plt.plot(np.array([Xs[0], Xs[0], Xs[1], Xs[1]])/1000, np.array([36, 40, 40, 36]), 'k-', lw=1.2)


# add slider
widget_color = 'lightgoldenrodyellow'
ax_Q = plt.axes([0.075, 0.35, 0.525, 0.05], facecolor=widget_color)
slide_Q = utils.MinMaxSlider(ax_Q, 'water discharge (m$^3$/s)', Qmin, Qbf, 
    valinit=Qinit, valstep=5, transform=ax.transAxes)


# 


# add gui table
# ax_overTable = plt.axes([0.20, 0.1, 0.5, 0.1], frameon=False, xticks=[], yticks=[])
# tabData = [['0', '0', False], ['0', '0', False],
#            ['0', '0', False], ['0', '0', False],
#            ['0', '0', False]]
# tabRowName = RKnames
# tabColName = ['flow depth (m)', 'stage (m)', 'over levee?'];
# overTable = plt.table(cellText=tabData, rowLabels=tabRowName,
#                       colLabels=tabColName, colWidths=[0.3, 0.2, 0.2],
#                       loc="center")
# overTable.scale(1, 1.5) # xscale, yscale 
# for tab_row in np.arange(1, np.size(tabData,0)+1):
#     vect_idx = tab_row - 1
#     H_val = H[RKidxs[vect_idx]]
#     overTable._cells[(tab_row, 0)]._text.set_text(utils.format_table_number(H_val))
#     stage_val = H[RKidxs[vect_idx]]+ eta[RKidxs[vect_idx]]
#     overTable._cells[(tab_row, 1)]._text.set_text(utils.format_table_number(stage_val))
#     over_val = H[RKidxs[vect_idx]] + eta[RKidxs[vect_idx]]   >   eta[RKidxs[vect_idx]] + zed[RKidxs[vect_idx]]
#     overTable._cells[(tab_row, 2)]._text.set_text(str(over_val))
#     overTable._cells[(tab_row, 2)]._text.set_color(utils.format_table_color(over_val))


# add gui buttons
chk_data_ax = plt.axes([0.75, 0.25, 0.15, 0.15], facecolor=background_color)
chk_data_dict = {'overbank flow':'ob'}
chk_data = widget.CheckButtons(chk_data_ax, chk_data_dict, [False])

btn_reset_ax = plt.axes([0.75, 0.1, 0.1, 0.04])
btn_reset = widget.Button(btn_reset_ax, 'Reset', color=widget_color, hovercolor='0.975')


def reset(event):
    slide_Q.reset()
    chk_data_status = chk_data.get_status()
    for cb in [i for i, x in enumerate(chk_data_status) if x]:
        chk_data.set_active(cb)
    fig.canvas.draw_idle()

def slider_update(label):
    chk_val = chk_data_dict[label]
    if chk_val == 'ob':
        if slide_Q.valmax == Qbf:
            slide_Q.set_slidermax(Qbf*2)
        else:
            slide_Q.set_slidermax(Qbf)
    fig.canvas.draw_idle()

# connect widgets
slide_Q.on_changed(update)
chk_data.on_clicked(slider_update)
# btn_reset.on_clicked(reset)


# show the results
plt.show()
