import argparse 
import yaml 
import pandas as pd 
import numpy as np
from progress.bar import Bar
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from tabpfn import TabPFNRegressor
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# loads parameters from config file 
def load_config(path=BASE_DIR / "config.yaml") : 
    with open(path, "r") as f:
        return yaml.safe_load(f)
    
def main(): 
    #1. Read parameter file 
    config = load_config()
    data_path = config["data_path"]
    #...
    #...

    #2. Read csv file 
    data  = pd.read_csv(BASE_DIR  / data_path ,sep = ",")

    print("The following columns where recognized : ", data.columns.tolist())
    print("If some are missing see the csv_format section of the REAMDE file")

     



    #checks for errors in spelling or naming of parameters to avoid pandas errors down the line 
    mandatory_columns = config["param_names"] + config["predict_name"]
  
    for col in mandatory_columns:
        if col not in data.columns:
            print(f"Error : The column '{col}' does not exist in the data file. Make sure your data is formateed as specified in README.txt")
            print(f"Available columns : {data.columns.tolist()}")
            return  # 
        
    #3. Split the data frame into parameters that are to be  predicted or are  given
    predict = data[config["predict_name"]]
    interior_parameters = data.drop(config["predict_name"], axis=1)
   
    

    #4. Split into train and test samples either randomly or with indices given at input 
    if(config["test_indices"][0]==config["test_indices"][1]) : #checks if user specified a range of test indices 
        print("\n")
        print("No test indices specified using random train/test split ")
        
        interior_train, interior_test, predict_train, predict_test = train_test_split(
        interior_parameters,
        predict,
        test_size=  0.2,
        random_state= 42,# Stays the same for reproducibility  
        )
    else : #use user specified subset for the testing of the training 
        test_indices = list(range(config["test_indices"][0], config["test_indices"][1]))

        interior_test = interior_parameters.iloc[test_indices]
        interior_train = interior_parameters.drop(index=test_indices)

        predict_test = predict.iloc[test_indices]
        predict_train = predict.drop(index=test_indices)

    #5. Make the TabPFN fit 
    reg = TabPFNRegressor()
    reg.fit(interior_train,predict_train)


    #6. Run the predctions in a batch 
    batch_size = 100   # try 100–500 depending on memory
    predictions = []

    for i in range(0, len(predict_test), batch_size):
        batch = interior_train[i:i + batch_size]
        preds = reg.predict(batch)
        predictions.append(preds)
    

    predictions = np.concatenate(predictions)




   

if __name__ == "__main__":
    main()