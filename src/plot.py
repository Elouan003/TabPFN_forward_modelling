import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def R_plot(prediction,validation,Title,Filename):
    # add MSE ??? 
    plt.figure(figsize=(10, 8))
    ax = plt.gca()
    ax.plot(validation,validation,color = "plum",label = "1:1 line")
    ax.scatter(validation,prediction,marker = ".", color = "teal")
    plt.title(Title)
    plt.ylabel("Radius predicted by TabPFN in Earth radii", fontsize=12)
    plt.xlabel("Validation radius in Earth radii", fontsize=12)
    plt.legend()
    plt.savefig(Filename)