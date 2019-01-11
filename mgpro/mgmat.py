import numpy as np
from mgpro import expand
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.fftpack import fft2, fftshift, ifft2, ifftshift
from scipy.interpolate import griddata


def cal_pos(max_len, len_x, len_y):
    if max_len > 1 or max_len < 0:
        raise ValueError('Input arg of max_len must be in the range of 0 to 1')
    if len_x > len_y:
        width = max_len
        hight = max_len * (len_y / len_x)
    else:
        hight = max_len
        width = max_len * (len_x / len_y)
    return width, hight


def xyz2grd(raw_data, dx, dy, xy_limit=None):
    data = raw_data.copy()
    data[:, [0, 1]] = data[:, [1, 0]]
    if xy_limit is None:
        xmin = np.min(raw_data[:, 0])
        xmax = np.max(raw_data[:, 0])
        ymin = np.min(raw_data[:, 1])
        ymax = np.max(raw_data[:, 1])
    else:
        xmin, xmax, ymin, ymax = xy_limit
    xrange = np.arange(xmin, xmax, dx)
    yrange = np.arange(ymin, ymax, dy)
    ymesh, xmesh = np.meshgrid(yrange, xrange, indexing='ij')
    grid_data = griddata(data[:, 0:2], data[:, 2], (ymesh, xmesh))
    return xrange, yrange, grid_data


class JetNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        if midpoint is None:
            self.midpoint = [0.2, 0.4, 0.6, 0.8]
        else:
            try:
                self.midpoint = list(midpoint)
            except Exception as e:
                raise ValueError(e)
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin] + self.midpoint + [self.vmax], np.linspace(0, 1, len(self.midpoint)+2)
        return np.ma.masked_array(np.interp(value, x, y))


class mgmat(object):
    def __init__(self, file, dx, dy, xy_limit=None):
        self.dx = dx
        self.dy = dy
        in_data = np.loadtxt(file)
        # self.x = np.unique(in_data[:, 0])
        # self.y = np.unique(in_data[:, 1])
        # len_x = self.x.shape[0]
        # len_y = self.y.shape[0]
        # self.dx = np.mean(np.diff(self.x))
        # self.dy = np.mean(np.diff(self.y))
        # self.data = np.zeros([len_y, len_x])
        # m = 0
        # for i in range(len_y):
        #     for j in range(len_x):
        #         self.data[i, j] = in_data[m, 2]
        #         m += 1
        self.x, self.y, self.data = xyz2grd(in_data, dx, dy, xy_limit=xy_limit)
        self.data_expand, self.row_begin, self.row_end, self.col_begin, self.col_end = expand.expand(self.data)
        self.data_sf = fftshift(fft2(self.data_expand))
        self.h = None
        self.order = None
        self.result = np.array([])

    def continuation(self, h, order):
        self.h = h
        self.order = order
        (len_row, len_col) = self.data_sf.shape
        dom_row = 2 * np.pi / len_row / self.dy
        dom_col = 2 * np.pi / len_col / self.dx
        row = np.arange(1, len_row+1)
        col = np.arange(1, len_col+1)
        row0 = int(len_row / 2) + 1
        col0 = int(len_col / 2) + 1
        (col_mesh, row_mesh) = np.meshgrid(col, row)
        H = np.sqrt(((col_mesh - col0)*dom_col)**2+((row_mesh - row0)*dom_row)**2) ** order \
            * np.exp(h * np.sqrt(((col_mesh - col0)*dom_col)**2+((row_mesh - row0)*dom_row)**2))
        self.result = np.real(ifft2(ifftshift(H * self.data_sf)))[self.row_begin: self.row_end + 1, self.col_begin: self.col_end + 1]
        return self.result

    def pltmap(self, fig, data, breakpoint=None):
        f_width = fig.get_figwidth()
        f_height = fig.get_figheight()
        frac_w = min([f_height, f_width])/max([f_height, f_width])
        real_width, real_height = cal_pos(0.7, data.shape[1], data.shape[0])
        real_width *= frac_w
        fig.clf()
        ax_raw = fig.gca()
        pcm = ax_raw.pcolor(data, cmap='jet')
        # ax_raw.figure.canvas.draw()
        cb = fig.colorbar(pcm, extend='both')
        # ax_raw.set_position([.1, .125, real_width, real_height], which='original')
        # cb.ax.set_position([.8, .1, real_height/6.27, real_height])
        fig.canvas.draw()

    def savetxt(self, filename):
        with open(filename, 'w') as f:
            for i, x in enumerate(self.x):
                for j, y in enumerate(self.y):
                    f.write('{:.4f}\t{:.4f}\t{:f}\n'.format(x, y, self.result[j, i]))


if __name__ == '__main__':
    filename = '../mag_geod.dat'
    mg = mgmat(filename, 2000, 2000)
    mg.continuation(0, 1)
    mg.savetxt('../mag_up0_diff1.dat')
    # f=plt.figure(figsize=(7, 5))
    # mg.pltmap(f, mg.result)
    # plt.show()
    # ax = f.gca()
    # pcm = ax.pcolor(mg.data)
    #
    # print(ax.get_position())
    # cb = f.colorbar(pcm, extend='both')
    # ax.set_position([.1,.1] + list(cal_pos(0.7, len(mg.x), len(mg.y))), which='original')
    # cb.ax.set_position([.8, .1, 0.1250, 0.78375])
    # #mg.pltmap(breakpoint=[-8000, -800, 800, 8000])
    # plt.show()
