import argparse 
import yaml 
import pandas as pd 
import numpy as np
import random 
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from tabpfn import TabPFNRegressor
from pathlib import Path
import matplotlib.pyplot as plt 
from src.plot import R_plot
from src.help import progress_bar,load_config
from src.help import validate_config
import torch



BASE_DIR = Path(__file__).resolve().parent


    
def main(): 
    #1. Read parameter file 
    config = load_config()
    data_path = config["data_path"]
    if not (validate_config(config)): 
        return 
   
    #...
    #...

    #2. Read csv file 
    print("\n# Loading your data ..")
    data  = pd.read_csv(BASE_DIR/ "data" / "input"  / data_path, sep = config["input_format"], index_col=False)
 
    

    
    
    

    #checks for errors in spelling or naming of parameters to avoid pandas errors down the line 
    mandatory_columns = config["param_names"] + config["predict_name"]
    for col in mandatory_columns:
        if col not in data.columns:
            print(f"Error : The column '{col}' does not exist in the data file. Make sure your data is formatted as specified in README.txt")
            print(f"Available columns : {data.columns.tolist()}")
            return  # 
    print()
    print("# File loaded succesfully \n ")
        
    #3. Split the data frame into parameters that are to be  predicted or are  given
    predict = data[config["predict_name"][0]]
    interior_parameters = data[config["param_names"]]

    

    #4. Split into train and test samples either randomly or with indices given at input 
    if(config["test_indices"][0]==config["test_indices"][1]) : #checks if user specified a range of test indices 
        print("# No test indices specified using random train/test split ")
        size_data_set = len(np.ravel(predict.values))
        test_sample_size = (size_data_set-500)/size_data_set
        interior_train, interior_test, predict_train, predict_test = train_test_split(
        #np.ravel(interior_parameters),
        interior_parameters,
        np.ravel(predict.values),
        test_size =  test_sample_size,
        random_state= 42,# Stays the same for reproducibility  
        )
    else : #use user specified subset for the testing of the training 
        test_indices = list(range(config["test_indices"][0], config["test_indices"][1]))
     
        
        interior_test = interior_parameters.iloc[test_indices]
        interior_train = interior_parameters.drop(index=test_indices)
        idx = np.random.choice(len(interior_train), min(500, len(interior_train)), replace=False)
        interior_train = interior_train.iloc[idx]

        predict_test = predict.iloc[test_indices]
        predict_train = predict.drop(index=test_indices)
        predict_train = predict_train.iloc[idx]
   

    #Warn for slow use in case of CPU for many samples 
    if torch.cuda.is_available():
        device = "cuda"       # Windows/Linux Nvidia
    elif torch.backends.mps.is_available():
        device = "mps"        # Mac Apple Silicon
    else:
        device = "cpu"

    print(f"→ Using : {device}")

    if device == "cpu" and len(interior_test) > 1000:
        print("⚠️  Warning : dataset > 1000 lines on CPU, computing can be slow.")
    #5. Make the TabPFN fit 
    
    reg = TabPFNRegressor(device = device,ignore_pretraining_limits=True)
    reg.fit(interior_train,predict_train)
    print("\n# TabPFN regressor fitted ")


    #6. Run the predctions in a batch 
    batch_size = config["batch_size"]  # try 100–500 depending on memory
    pfn_predictions = []
    print("\n# TabPFN predictions :  ")
    for i in range(0, len(predict_test), batch_size):
        progress_bar(i,len(predict_test)//batch_size*100)
        batch = interior_test[i:i + batch_size]
        preds = reg.predict(batch)
        pfn_predictions.append(preds)
    progress_bar(1,1)
    

    pfn_predictions = np.concatenate(pfn_predictions)




    #6. Make the validation plot of R_predicted against R_control 
    pred_name = config["predict_name"][0]
    if(config["make_plot"]):
        filename = BASE_DIR/ "data" / "output"  / "plots" / config["output_pdf"]
        
    
        R_plot(predict_test,pfn_predictions,pred_name,filename)


    #7. Save the Radii predicted by TabPFN and the "True" Radii so that the user can have acces to the data and plot is as he likes 
    
    df_output = pd.DataFrame({
        "True R ": predict_test,
        "Tab_pfn R": pfn_predictions
    })

    output_path = BASE_DIR / "data" / "output" / "csv" / config["output_csv"]
    output_path.parent.mkdir(exist_ok=True)
    df_output.to_csv(output_path, index=False)  
    

    print("\nDONE :) ")

    def predict(args): 
     
        
        parameters =np.array(args)
        if  not len(args) == len(config["param_names"]) :
            print("\nParameter mismatch : the number of values must match 'param_names' in config.yaml" )
        parameters = parameters.reshape(1,-1)
        df = pd.DataFrame(parameters, columns=config["param_names"])
        

        return  reg.predict(df)
    print("\n ---Single planet prediction---")
    answer = input("Do you want to make a single planet prediction? (y/n) : ").strip().lower()
    if answer != 'y':
        return

    # 2) Demande une valeur pour chaque nom de la liste
    
    values = []

    for name in config["param_names"]:
        while True:  # Boucle pour forcer une valeur numérique valide
            try:
                val = float(input(f"Enter a value for '{name}' : "))
                values.append(val)
                break
            except ValueError:
                print("  !!  Please enter a numerical value")

    print(f"\nPredicted {pred_name}: {predict(values)[0]}")

if __name__ == "__main__":
    main()