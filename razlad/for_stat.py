import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from razlad.get_surge import f_probability

graph_len = 500
k_surge = 0.02
surge_len = int(graph_len*k_surge)

surge_ps = [0]*((graph_len - surge_len)//2)
surge_ps.extend([1]*surge_len)
surge_ps.extend([0]*int((graph_len - surge_len)/2))

surge_lin_ps = [0.0]*((graph_len - surge_len)//2)
surge_lin_ps.extend([x/surge_len for x in range(surge_len)])
surge_lin_ps.extend([1.0]*((graph_len - surge_len)//2))

surge_lin_ps_inv = [1.0]*((graph_len - surge_len)//2)
surge_lin_ps_inv.extend([(1 - x/surge_len) for x in range(surge_len)])
surge_lin_ps_inv.extend([0.0]*((graph_len - surge_len)//2))

surge_lin_ps_obr = [0.0]*((graph_len - surge_len)//2)
surge_lin_ps_obr.extend([x/k_surge/graph_len for x in range(surge_len)])
surge_lin_ps_obr.extend([(1 - x/k_surge/graph_len) for x in range(surge_len)])
surge_lin_ps_obr.extend([0.0]*((graph_len - surge_len)//2))

surge_x2_ps = [0.0]*((graph_len - surge_len)//2)
surge_x2_ps.extend([((x*2/surge_len)**2)/2 for x in range(surge_len//2)])
surge_x2_ps.extend([(1 - ((x - surge_len/2)/(surge_len//2))**2)/2 + 0.5 for x in range(surge_len//2)])
surge_x2_ps.extend([1.0]*((graph_len - surge_len)//2))

surge_x2_ps_inv = [1.0]*((graph_len - surge_len)//2)
surge_x2_ps_inv.extend([1 - (((x*2/surge_len)**2)/2) for x in range(surge_len//2)])
surge_x2_ps_inv.extend([1 - ((1 - ((x - surge_len/2)/(surge_len//2))**2)/2 + 0.5) for x in range(surge_len//2)])
surge_x2_ps_inv.extend([0.0]*((graph_len - surge_len)//2))

surge_x2_ps_obr = [0.0]*((graph_len - surge_len)//2)
surge_x2_ps_obr.extend([((x*2/surge_len)**2)/2 for x in range(surge_len//2)])
surge_x2_ps_obr.extend([(1 - ((x - surge_len/2)/(surge_len//2))**2)/2 + 0.5 for x in range(surge_len//2)])
surge_x2_ps_obr.extend([1 - (((x*2/surge_len)**2)/2) for x in range(surge_len//2)])
surge_x2_ps_obr.extend([1 - ((1 - ((x - surge_len/2)/(surge_len//2))**2)/2 + 0.5) for x in range(surge_len//2)])
surge_x2_ps_obr.extend([0.0]*((graph_len - surge_len)//2))

len_win_x = np.arange(4, 40, 1)
len_win_bef = np.arange(2, 38, 1)
probabl_ps = np.zeros([len(len_win_x), len(len_win_bef)])
bef_aft = np.zeros([])
bef_surge = np.zeros([])
aft_surge = np.zeros([])
for len_win_ind in range(len(len_win_x)):
    for len_win_bef_ind in range(len(len_win_bef)):
        if len_win_x[len_win_ind] - len_win_bef[len_win_bef_ind] < 2:
            continue
        if len_win_bef[len_win_bef_ind] < len_win_x[len_win_ind]//2:
            continue
        len_win_aft = len_win_x[len_win_ind] - len_win_bef[len_win_bef_ind]
        bef_aft = np.append(bef_aft, len_win_bef[len_win_bef_ind]/len_win_aft)
        bef_surge = np.append(bef_surge, [len_win_bef[len_win_bef_ind] / surge_len])
        aft_surge = np.append(aft_surge, [len_win_aft / surge_len])
        probabl_ps[len_win_ind][len_win_bef_ind] = \
            max(f_probability(surge_ps, len_win_bef[len_win_bef_ind], len_win_aft))
        print('Win len:' + str(len_win_x[len_win_ind]) + ',\twin bef:' + str(len_win_bef[len_win_bef_ind]) +
              ',\twin aft:' + str(len_win_aft) + ',\tWinBef/WinAft:' + str(bef_aft[-1]) + ',\tWinBef/surge:' +
              str(bef_surge[-1]) + ',\tWinAft/surge:' + str(aft_surge[-1]) + ',\tmax:' +
              str(probabl_ps[len_win_ind][len_win_bef_ind]))
        print()
x_mesh_bef, y_mesh_bef = np.meshgrid(len_win_x, len_win_bef)
x_mesh_bef_aft, y_mesh_bef_aft = np.meshgrid(len_win_x, bef_aft)
x_mesh_bef_surge, y_mesh_bef_surge = np.meshgrid(len_win_x, bef_surge)
x_mesh_aft_surge, y_mesh_aft_surge = np.meshgrid(len_win_x, aft_surge)

fig = plt.figure()
ax = fig.gca(projection='3d')
# Plot the surface.
surf = ax.plot_surface(x_mesh_bef, y_mesh_bef, probabl_ps.transpose(), cmap=cm.seismic,
                       linewidth=1, antialiased=True)
# Customize the z axis.
#ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
#ax.xaxis(len_win_x)
ax.set_xlabel('Win len')
ax.set_ylabel('win_before')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()


plt.figure(1)
plt.subplot(1, 1, 1)
plt.plot(surge_ps, linewidth=3)
plt.grid(True)
plt.show()

plt.figure(2)
plt.subplot(1, 1, 1)
plt.plot(surge_lin_ps, linewidth=3)
plt.grid(True)
plt.show()

plt.figure(3)
plt.subplot(1, 1, 1)
plt.plot(surge_lin_ps_inv, linewidth=3)
plt.grid(True)
plt.show()

plt.figure(4)
plt.subplot(1, 1, 1)
plt.plot(surge_lin_ps_obr, linewidth=3)
plt.grid(True)
plt.show()

plt.figure(5)
plt.subplot(1, 1, 1)
plt.plot(surge_x2_ps, linewidth=3)
plt.grid(True)
plt.show()

plt.figure(6)
plt.subplot(1, 1, 1)
plt.plot(surge_x2_ps_inv, linewidth=3)
plt.grid(True)
plt.show()

plt.figure(7)
plt.subplot(1, 1, 1)
plt.plot(surge_x2_ps_obr, linewidth=3)
plt.grid(True)
plt.show()
