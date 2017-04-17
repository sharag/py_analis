import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from razlad.functions import f_probability, max_probabil
import pickle

# Формирвоание скачков
# Характеристики скачков
graph_len = 1000
surge_len = 200
surges = []

surge_ps = [0]*((graph_len - surge_len)//2)
surge_ps.extend([1]*surge_len)
surge_ps.extend([0]*int((graph_len - surge_len)/2))
surges.append(surge_ps)

surge_lin_ps = [0.0]*((graph_len - surge_len)//2)
surge_lin_ps.extend([x/surge_len for x in range(surge_len)])
surge_lin_ps.extend([1.0]*((graph_len - surge_len)//2))
surges.append(surge_lin_ps)

#surge_lin_ps_inv = [1.0]*((graph_len - surge_len)//2)
#surge_lin_ps_inv.extend([(1 - x/surge_len) for x in range(surge_len)])
#surge_lin_ps_inv.extend([0.0]*((graph_len - surge_len)//2))

surge_x1 = [0.0]*((graph_len - surge_len)//2)
surge_x1.extend([x/surge_len for x in range(surge_len)])
surge_x1.extend([(1 - x/surge_len) for x in range(surge_len)])
surge_x1.extend([0.0]*((graph_len - surge_len)//2))
surges.append(surge_x1)

#surge_x2_ps = [0.0]*((graph_len - surge_len)//2)
#surge_x2_ps.extend([((x*2/surge_len)**2)/2 for x in range(surge_len//2)])
#surge_x2_ps.extend([(1 - ((x - surge_len/2)/(surge_len//2))**2)/2 + 0.5 for x in range(surge_len//2)])
#surge_x2_ps.extend([1.0]*((graph_len - surge_len)//2))

#surge_x2_ps_inv = [1.0]*((graph_len - surge_len)//2)
#surge_x2_ps_inv.extend([1 - (((x*2/surge_len)**2)/2) for x in range(surge_len//2)])
#surge_x2_ps_inv.extend([1 - ((1 - ((x - surge_len/2)/(surge_len//2))**2)/2 + 0.5) for x in range(surge_len//2)])
#surge_x2_ps_inv.extend([0.0]*((graph_len - surge_len)//2))

surge_len_05 = surge_len//2
surge_x2 = [0.0]*((graph_len - surge_len)//2)
surge_x2.extend([((x*2/surge_len_05)**2)/2 for x in range(surge_len_05//2)])
surge_x2.extend([(1 - ((x - surge_len_05/2)/(surge_len_05//2))**2)/2 + 0.5 for x in range(surge_len_05//2)])
surge_x2.extend([1 - (((x*2/surge_len_05)**2)/2) for x in range(surge_len_05//2)])
surge_x2.extend([1 - ((1 - ((x - surge_len_05/2)/(surge_len_05//2))**2)/2 + 0.5) for x in range(surge_len_05//2)])
surge_x2.extend([0.0]*((graph_len - surge_len)//2))
surges.append(surge_x2)

with open('for_stat.pickle', 'wb') as f:
    pickle.dump(surges, f)

plt.figure(1)
plt.subplot(1, 1, 1)
plt.plot(surge_ps, linewidth=1)
plt.plot(surge_lin_ps, linewidth=1)
plt.plot(surge_lin_ps, linewidth=1)
plt.plot(surge_x2, linewidth=1)
plt.grid(True)
plt.show()


# Характеристики окна
win_size = 200
# скачок постоянной составляющей
len_win, len_win_bef, probabl_ps = max_probabil(surge_ps, win_size, surge_len, 1)
x_mesh_bef_ps, y_mesh_bef_ps = np.meshgrid(len_win, len_win_bef)

# линейное изменение постоянной составляющей
len_win, len_win_bef, probabl_lin_ps = max_probabil(surge_lin_ps, win_size, surge_len, 1)
x_mesh_bef_lin_ps, y_mesh_bef_lin_ps = np.meshgrid(len_win, len_win_bef)

# нелинейное изменение постоянной составляющей
#len_win, len_win_bef, probabl_x2_ps = max_probabil(surge_x2_ps, win_size, surge_len)
#x_mesh_bef_x2_ps, y_mesh_bef_x2_ps = np.meshgrid(len_win, len_win_bef)

# нелинейное изменение постоянной составляющей и обратно
#len_win, len_win_bef, probabl_x2_ps_obr = max_probabil(surge_x2_ps_obr, win_size, surge_len)
#x_mesh_bef_x2_ps_obr, y_mesh_bef_x2_ps_obr = np.meshgrid(len_win, len_win_bef)

# скачок постоянной составляющей
fig = plt.figure(1)
ax = fig.gca(projection='3d')
# Plot the surface.
surf = ax.plot_surface(x_mesh_bef_ps, y_mesh_bef_ps, probabl_ps.transpose(), cmap=cm.seismic, linewidth=2, antialiased=True)
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

plt.figure(2)
plt.subplot(1, 1, 1)
plt.plot(surge_ps, linewidth=3)
plt.grid(True)
plt.show()

# линейное изменение постоянной составляющей
fig = plt.figure(3)
ax = fig.gca(projection='3d')
# Plot the surface.
surf = ax.plot_surface(x_mesh_bef_lin_ps, y_mesh_bef_lin_ps, probabl_lin_ps.transpose(), cmap=cm.seismic, linewidth=2, antialiased=True)
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

plt.figure(4)
plt.subplot(1, 1, 1)
plt.plot(surge_lin_ps, linewidth=3)
plt.grid(True)
plt.show()

# нелинейное изменение постоянной составляющей
fig = plt.figure(5)
ax = fig.gca(projection='3d')
# Plot the surface.
#surf = ax.plot_surface(x_mesh_bef_x2_ps, y_mesh_bef_x2_ps, probabl_x2_ps.transpose(), cmap=cm.seismic, linewidth=2, antialiased=True)
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

plt.figure(6)
plt.subplot(1, 1, 1)
#plt.plot(surge_x2_ps, linewidth=3)
plt.grid(True)
plt.show()

# нелинейное изменение постоянной составляющей и обратно
fig = plt.figure(7)
ax = fig.gca(projection='3d')
# Plot the surface.
#surf = ax.plot_surface(x_mesh_bef_x2_ps_obr, y_mesh_bef_x2_ps_obr, probabl_x2_ps_obr.transpose(), cmap=cm.seismic, linewidth=2, antialiased=True)
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

plt.figure(8)
plt.subplot(1, 1, 1)
#plt.plot(surge_x2_ps_obr, linewidth=3)
plt.grid(True)
plt.show()

# Остатки
plt.figure(9)
plt.subplot(1, 1, 1)
#plt.plot(surge_lin_ps_inv, linewidth=3)
plt.grid(True)
plt.show()

plt.figure(10)
plt.subplot(1, 1, 1)
#plt.plot(surge_lin_ps_obr, linewidth=3)
plt.grid(True)
plt.show()

plt.figure(11)
plt.subplot(1, 1, 1)
#plt.plot(surge_x2_ps, linewidth=3)
plt.grid(True)
plt.show()

plt.figure(12)
plt.subplot(1, 1, 1)
#plt.plot(surge_x2_ps_inv, linewidth=3)
plt.grid(True)
plt.show()

