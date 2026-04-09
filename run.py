import argparse 
import yaml 
import pandas as pd 
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from tabpfn import TabPFNRegressor
from pathlib import Path
import matplotlib.pyplot as plt 
from src.plot import R_plot
from src.help import progress_bar,load_config




BASE_DIR = Path(__file__).resolve().parent


    
def main(): 
    #1. Read parameter file 
    config = load_config()
    data_path = config["data_path"]
    #...
    #...

    #2. Read csv file 
    data  = pd.read_csv(BASE_DIR/ "data" / "input"  / data_path, sep = "\s+", index_col=False)
    

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
    predict = data[config["predict_name"][0]]
    interior_parameters = data.drop(config["predict_name"][0], axis=1)
    print(np.ravel(predict.values))
    

    #4. Split into train and test samples either randomly or with indices given at input 
    if(config["test_indices"][0]==config["test_indices"][1]) : #checks if user specified a range of test indices 
        print("\n")
        print("No test indices specified using random train/test split ")
        
        interior_train, interior_test, predict_train, predict_test = train_test_split(
        #np.ravel(interior_parameters),
        interior_parameters,
        np.ravel(predict.values),
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
    pfn_predictions = []

    for i in range(0, len(predict_test), batch_size):
        batch = interior_test[i:i + batch_size]
        preds = reg.predict(batch)
        pfn_predictions.append(preds)
        #progress_bar(i,)
    

    pfn_predictions = np.concatenate(pfn_predictions)




    #6. Make the validation plot of R_predicted against R_control 
    pred_name = config["predict_name"][0]
    R_plot(predict_test,pfn_predictions,f"TabPFN predicted {pred_name} vs test values")


    #7. Save  R_predicted and R_control so that the user can have acces to the data and plot is as he likes 
    
    df_output = pd.DataFrame({
        "True R ": predict_test,
        "Tab_pfn R": pfn_predictions
    })

    output_path = BASE_DIR / "data" / "output" / "test"
    output_path.parent.mkdir(exist_ok=True)
    df_output.to_csv(output_path, index=False)  
    

   

if __name__ == "__main__":
    main()