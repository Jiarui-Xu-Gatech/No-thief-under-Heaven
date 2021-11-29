# -*- coding:utf-8 -*-
"""
author: 11238
date: 2021year 11month 14day
"""
import pypianoroll
import matplotlib.pyplot as plt

def create_score(path):
    multitrack = pypianoroll.read(path)
    multitrack.plot()
    #plt.show()
    plt.savefig('midiscore.png')
