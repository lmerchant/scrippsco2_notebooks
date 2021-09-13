from matplotlib import rcParams
from matplotlib import ticker
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Polygon
import numpy as np


def set_website_plot_props(ax, fig, xmin, xmax, ymin, ymax, xlabel, ylabel):

    # ---------------------------------
    # Plot properties for website plots
    # ---------------------------------

    # Allow room at top for the 3 titles
    fig.subplots_adjust(top=0.85)

    # activate latex text rendering
    #rc('axes', linewidth=1)
    rcParams.update({
        "text.usetex": True,
        "font.family": "sans-serif",
        "font.weight":  "bold",
        "font.sans-serif": ["Helvetica"]})

    rcParams['text.latex.preamble'] = r'\usepackage{sfmath} \boldmath'

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.tick_params(which='both', bottom=True, top=True, left=True, right=True)

    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=16)

    ax.tick_params(which='major', direction='in', length=9, width=1)

    tick_spacing = 5
    ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    tick_spacing = 5
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    # Display every other y major tick label
    for label in ax.yaxis.get_ticklabels()[::2]:
        label.set_visible(False)

    ax.xaxis.get_major_formatter()._usetex = True
    ax.yaxis.get_major_formatter()._usetex = True

    ax.tick_params(which='minor', direction='in', length=4)
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(5))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))

    bold_xlabel = r'\textbf{{{}}}'.format(xlabel)
    bold_ylabel = r'\textbf{{{}}}'.format(ylabel)

    ax.set_xlabel(bold_xlabel, fontsize=21, labelpad=8)
    ax.set_ylabel(bold_ylabel, fontsize=21, labelpad=12)


def add_3_plot_titles(ax, title1, title2, title3):

    # Add 3 plot title for scrippsco2 website

    bold_title1 = r'\textbf{{{}}}'.format(title1)
    bold_title2 = r'\textbf{{{}}}'.format(title2)

    ax.annotate(bold_title1, xy=(0, 1.15), xycoords='axes fraction', fontsize=21,
                horizontalalignment='left', verticalalignment='top')
    ax.annotate(bold_title2, xy=(0, 1.095), xycoords='axes fraction', fontsize=21,
                horizontalalignment='left', verticalalignment='top')
    ax.annotate(title3, xy=(0, 1.04), xycoords='axes fraction', fontsize=12,
                horizontalalignment='left', verticalalignment='top')


def add_4_plot_titles(ax, title1, title2, title3, title4):

    # Add 4 plot title for scrippsco2 website

    bold_title1 = r'\textbf{{{}}}'.format(title1)
    bold_title2 = r'\textbf{{{}}}'.format(title2)
    bold_title3 = r'\textbf{{{}}}'.format(title3)

    ax.annotate(bold_title1, xy=(0, 1.2), xycoords='axes fraction', fontsize=21,
                horizontalalignment='left', verticalalignment='top')
    ax.annotate(bold_title2, xy=(0, 1.15), xycoords='axes fraction', fontsize=21,
                horizontalalignment='left', verticalalignment='top')
    ax.annotate(bold_title3, xy=(0, 1.095), xycoords='axes fraction', fontsize=21,
                horizontalalignment='left', verticalalignment='top')
    ax.annotate(title4, xy=(0, 1.04), xycoords='axes fraction', fontsize=12,
                horizontalalignment='left', verticalalignment='top')


def add_sio_logo(logo_file, fig):

    # Add SIO logo to plot

    logo = mpimg.imread(logo_file)

    newax = fig.add_axes([0.73, 0.18, 0.2, 0.2], anchor='SE', zorder=1)
    plt.imshow(logo)
    plt.axis('off')


def save_plot_for_website(fig, pdf_file, png_file):

    # Save plot as  pdf and png for scrippsco2 website

    # For pdf
    width_in = 11
    height_in = 8.5
    fig.set_size_inches(width_in, height_in)

    plt.subplots_adjust(left=0.109, right=0.95, top=0.85, bottom=0.15)

    fig.savefig(pdf_file, facecolor='w', edgecolor='w',
                orientation='landscape', format=None,
                transparent=False, pad_inches=0)

    # For png
    width_px = 1200
    height_px = (height_in/width_in) * width_px

    png_dpi = 100
    fig.set_size_inches(width_px/png_dpi, height_px/png_dpi)

    fig.savefig(png_file, facecolor='w', edgecolor='w',
                orientation='landscape', dpi=png_dpi, pad_inches=0)


def gradient_fill(x, y, fill_color=None, xmin=None, ymin=None, alpha_bottom=None, ax=None, **kwargs):

    # Create gradient under a curve

    # https://stackoverflow.com/questions/29321835/is-it-possible-to-get-color-gradients-under-curve-in-matplotlib
    # Modified to add gradient below curve and have a bottom alpha
    # def gradient_fill(x, y, fill_color=None, ax=None, **kwargs):
    """
    Plot a line with a linear alpha gradient filled beneath it.

    Parameters
    ----------
    x, y : array-like
        The data values of the line.
    fill_color : a matplotlib color specifier (string, tuple) or None
        The color for the fill. If None, the color of the line will be used.
    ax : a matplotlib Axes instance
        The axes to plot on. If None, the current pyplot axes will be used.
    Additional arguments are passed on to matplotlib's ``plot`` function.

    Returns
    -------
    line : a Line2D instance
        The line plotted.
    im : an AxesImage instance
        The transparent gradient clipped to just the area beneath the curve.
    """
    if ax is None:
        ax = plt.gca()

    line, = ax.plot(x, y, **kwargs)
    if fill_color is None:
        fill_color = line.get_color()

    if alpha_bottom is None:
        alpha_bottom = 0

    if xmin is None:
        xmin = x.min()

    if ymin is None:
        ymin = y.min()

    zorder = line.get_zorder()
    alpha = line.get_alpha()
    alpha = 1.0 if alpha is None else alpha

    z = np.empty((100, 1, 4), dtype=float)
    rgb = mcolors.colorConverter.to_rgb(fill_color)
    z[:, :, :3] = rgb
    #z[:,:,-1] = np.linspace(0, alpha, 100)[:,None]
    z[:, :, -1] = np.linspace(alpha_bottom, alpha, 100)[:, None]

    #xmin, xmax, ymin, ymax = x.min(), x.max(), y.min(), y.max()
    xmax, ymax = x.max(), y.max()

    im = ax.imshow(z, aspect='auto', extent=[xmin, xmax, ymin, ymax],
                   origin='lower', zorder=zorder)

    xy = np.column_stack([x, y])
    xy = np.vstack([[xmin, ymin], xy, [xmax, ymin], [xmin, ymin]])
    clip_path = Polygon(xy, facecolor='none', edgecolor='none', closed=True)
    ax.add_patch(clip_path)
    im.set_clip_path(clip_path)

    ax.autoscale(True)
    return line, im
