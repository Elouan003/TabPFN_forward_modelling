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
    


def validate_config(config):
    errors = []

    if not config["data_path"]:
        errors.append("  - 'data_path' is empty : specify the name of your file in config.yaml")
    
    if not config["param_names"] or config["param_names"] == [""]:
        errors.append("  - 'param_names' is empty  : specifiy which columns are to be used as parameters in config.yaml")
    
    if not config["predict_name"] or config["predict_name"] == [""]:
        errors.append("  - 'predict_name' is empty : specify which column is to be predicted in config.yaml")

    if errors:
        print("❌ Error : the following parameters where not given in  config.yaml :\n")
        for e in errors:
            print(e)
        print("\n→ Please edit config.yaml before realaunching the script. More informatin on the config.yaml file can be found in READEM.md")
        return False
    
    return True