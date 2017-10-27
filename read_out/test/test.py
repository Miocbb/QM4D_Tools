#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('1.out.losc.spec')

plt.plot(data[:,0], data[:,1])
plt.show()
