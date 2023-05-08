import numpy as np
import matplotlib.pyplot as plt

frames1, data1 = np.loadtxt('RMSDs/1BSG_Sabla_apo_ca_rmsd.dat', unpack=True, usecols=(0,1))
frames2, data2 = np.loadtxt('RMSDs/1BUE_NmcA_apo_ca_rmsd.dat', unpack=True, usecols=(0,1))
frames3, data3 = np.loadtxt('RMSDs/3BLM_blaZ_apo_ca_rmsd.dat', unpack=True, usecols=(0,1))
frames4, data4 = np.loadtxt('RMSDs/1E25_Per1_apo_ca_rmsd.dat', unpack=True, usecols=(0,1))
frames5, data5 = np.loadtxt('RMSDs/1BTL_tem1_apo_ca_rmsd.dat', unpack=True, usecols=(0,1))
frames6, data6 = np.loadtxt('RMSDs/1BZA_Toho1_apo_ca_rmsd.dat', unpack=True, usecols=(0,1))


plt.plot(frames1, data1, linewidth=0.5,  color='skyblue', label='1BSG_Sabla')
plt.plot(frames2, data2, linewidth=0.5,  color='lightgreen', label='1BUE_NmcA')
plt.plot(frames3, data3, linewidth=0.5,  color='plum', label='3BLM_blaZ')
plt.plot(frames4, data4, linewidth=0.5,  color='lightsalmon', label='1E25_Per1')
plt.plot(frames5, data5, linewidth=0.5,  color='lightgrey', label='1BTL_tem1')
plt.plot(frames6, data6, linewidth=0.5,  color='brown', label='1BZA_Toho1')

plt.legend()
plt.xlabel("frames")
plt.ylabel("rmsd, A")
plt.title("Combined rmsd of tested systems")
plt.savefig('rmsd.png')
