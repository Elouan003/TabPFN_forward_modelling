from progress.bar import Bar
import numpy as np 
from pathlib import Path
import yaml 

BASE_DIR = Path(__file__).resolve().parent.parent

def progress_bar(current, total, bar_length=20):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    print(f'Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)



# loads parameters from config file 
def load_config(path=BASE_DIR / "config.yaml") : 
    with open(path, "r") as f:
        return yaml.safe_load(f)