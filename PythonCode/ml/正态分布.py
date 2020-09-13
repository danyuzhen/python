# -*- coding: utf-8 -*-
"""
Created on Sat May  4 10:56:51 2019

@author: admin
"""

import numpy as np
import matplotlib.pyplot as plt
import math

u = 14*60   # 期望值u,最高点
u1 = 12   # 期望值u,最高点

# 标准差o
sig = math.sqrt(1)

x = np.linspace(0, 1440, 1440)
#for i in range(3000,10000):
#    sig = math.sqrt(i)
#    y = np.exp(-(x - u) ** 2 /(2 * sig ** 2)) / (math.sqrt(2 * math.pi) *sig)
#            
#    plt.plot(x, y, "b-", linewidth=2)
#    plt.grid(True)
#    plt.show()

sig = math.sqrt(1000000)
y = np.exp(-(x - u) ** 2 /(2 * sig ** 2)) / (math.sqrt(2 * math.pi) *sig)
        
plt.plot(x, y, "b-", linewidth=2)
plt.grid(True)
plt.show()
    