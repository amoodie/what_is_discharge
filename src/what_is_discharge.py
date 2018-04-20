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
import utils, channel_geom

# SET PARAMETERS
B = 600 # channel width
S0 = 1e-4 # channel slope
Cf = 0.005
g = 9.81

Qwinit = 100
Qw = Qwinit
Qwbf = 350
Qwmax = 600
Qwmin = 50

Hninit = channel_geom.get_Hn(Qwinit, B, Cf, S0, g)
Hnmax = channel_geom.get_Hn(Qwmax, B, Cf, S0, g)

x = channel_geom.make_xcoords(B)
y = channel_geom.make_ycoords(x, Hninit, Hnmax)


# DEFINE FUNCTIONS
def update(val):
    Q = slide_Qw.val
    # B = B
    # Cf = Cf
    # S0 = S0
    # g = 9.81
    Hn = channel_geom.get_Hn(Q, B, Cf, S0, g)
    y = channel_geom.make_ycoords(x, Hn, Hnmax)

    water_shade.set_xy(np.column_stack((x, y)))



    fig.canvas.draw_idle()


# H = hydro.get_backwater_dBdx(eta, S, B, H0, Cf, Qw, nx, dx)
# Xs = hydro.find_backwaterregion(H, dx)
# # zed = 0.5 + -1e-5*(x - (L*mou)) + hydro.get_backwater_dBdx(eta, S, B, H0, Cf, Qwbf, nx, dx)
# zed = 0.5 + hydro.get_backwater_dBdx(eta, S, B, H0, Cf, Qwbf, nx, dx)

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
plt.ylim(np.floor(-Hnmax), 1)
plt.xlim(-(B/2)*1.1, B/2*2)
# ax.xaxis.set_major_formatter( plt.FuncFormatter(lambda v, x: int(-1*(v - (L/1000*mou)))) )

# add plot elements
# RK_line = plt.plot(np.tile(L/1000*mou - RKs, (2, 1)),
#                    np.tile(np.array([-50, 100]), (np.size(RKs), 1)).transpose(), 
#                    ls=':', lw=1.5, color='grey')
# eta_line, = plt.plot(x/1000, eta, lw=2, color='black') # plot bed
# eta_shade = ax.add_patch(ptch.Polygon(utils.format_polyvects(
#                          x/1000, x/1000, -50*np.ones(np.size(eta)), eta),
#                          facecolor='saddlebrown'))
# zed_line = plt.plot(x[:mouIdx]/1000, eta[:mouIdx]+zed[:mouIdx], 'k--', lw=1.2) # plot levee
# water_line, = plt.plot(x/1000, eta+H, lw=2, color='steelblue') # plot initial condition
water_shade = ax.add_patch(ptch.Polygon(np.column_stack((x, y)), facecolor='powderblue'))
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
# Qw_val = plt.text(0.05, 0.85, "Qw = " + utils.format_number(Qw),
#                   fontsize=16, transform=ax.transAxes, 
#                   backgroundcolor='white')
# Bw_val = plt.text(( (Xs[1]-Xs[0])/2 + Xs[0])/1000, 45, 
#     "backwater from \n" + "RK " + str(int(L*mou/1000-Xs[0]/1000)) +
#     " to " + str(int(L*mou/1000-Xs[1]/1000)), 
#     horizontalalignment="center", backgroundcolor="white")
# Bw_brack, = plt.plot(np.array([Xs[0], Xs[0], Xs[1], Xs[1]])/1000, np.array([36, 40, 40, 36]), 'k-', lw=1.2)


# add slider
widget_color = 'lightgoldenrodyellow'
ax_Qw = plt.axes([0.075, 0.35, 0.525, 0.05], facecolor=widget_color)
slide_Qw = utils.MinMaxSlider(ax_Qw, 'water discharge (m$^3$/s)', Qwmin, Qwmax, 
    valinit=Qwinit, valstep=5, transform=ax.transAxes)

# slide_Qw.set_val(1000)
slide_Qw.set_slidermax(1000)

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
chk_data_dict = {'show water lines':'wl', 'show thalweg':'tw'}
chk_data = widget.CheckButtons(chk_data_ax, chk_data_dict,
                                            (False, False))

btn_reset_ax = plt.axes([0.75, 0.1, 0.1, 0.04])
btn_reset = widget.Button(btn_reset_ax, 'Reset', color=widget_color, hovercolor='0.975')


def reset(event):
    slide_Qw.reset()
    chk_data_status = chk_data.get_status()
    for cb in [i for i, x in enumerate(chk_data_status) if x]:
        chk_data.set_active(cb)
    fig.canvas.draw_idle()


# connect widgets
slide_Qw.on_changed(update)
# chk_data.on_clicked(draw_nitt)
# btn_reset.on_clicked(reset)


# show the results
plt.show()
