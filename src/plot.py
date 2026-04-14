import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def R_plot(prediction,validation,pred_name,Filename):
    # add MSE ??? 
    plt.figure(figsize=(10, 8))
    ax = plt.gca()
    ax.plot(validation,validation,color = "plum",label = "1:1 line")
    ax.scatter(validation,prediction,marker = ".", color = "teal")
    plt.title(f"TabPFN predicted {pred_name} vs test values")
    plt.ylabel(f"{pred_name} predicted by TabPFN in given units", fontsize=12)
    plt.xlabel(f"Validation {pred_name} in given units", fontsize=12)
    plt.legend()
    plt.savefig(Filename)