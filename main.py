import classTransfer as ct
import pandas as pd
import data_read as dr
import matplotlib.pyplot as plt
import transfer_analysis as ta

"""
names = ["VG","IG","tG","VD","ID","tD"]
data = pd.read_csv("test_data.dat", sep="\t", names=names, header=1)

t1 = ct.Transfer(data.VG, data.IG, data.VD, data.ID)

th = t1.calculate_threshold(0.9e-5)
print(th)

print(t1.calculate_mobility(0.9e-5, 1e-9, 4e-6, 8e-6))
print(t1.calculate_subthreshold(-1,0))

t1.plot_transfer()
"""

"""
d = dr.read_file("test_recovery.dat")
fig, ax = plt.subplots()
for i in range(len(d)):
    ax.plot(d[i].VG, d[i].ID)
    print(d[i].time)

plt.show()
"""

#To change is using mac or windows
a = dr.read_folder("./Transfer/*.dat")
vth = []
time = []

for i in range(len(a)):
   vth.append(a[i].calculate_threshold(5e-5))
   time.append((a[i].time-a[0].time).seconds/3600)
   
fig, ax = plt.subplots()
for i in range(len(a)):
    ax.plot(a[i].VG, a[i].ID)

dd = ta.extract_transfer_data(a, 3e-8, 4e-6, 8e-6, 800)

fig2, ax2 = plt.subplots()
ax2.plot(dd.Dose, dd.Mobility)

plt.show()

