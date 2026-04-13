# TabPFN forward modelling 
(Built with PriorLabs-TabPFN)
 
 This repository contains the code necessary to fit the TabPFN model to a part of your training data set and make predictions for the rest of the set. The data used for the fitting are normally the interior parameters of the planet such as core/mantel mass, water mass fraction or Mg to Si mantle mass ratio but can also be extended to more general parameters of the planet such as age or different types of mixing assumptions. 


---
## TabPFN Version  

This work was done with TabPFn V2 as described in [Hollmann et al. 2025 ](https://www.nature.com/articles/s41586-024-08328-6)

The standard license for this version can be found [here](https://github.com/PriorLabs/TabPFN/blob/main/LICENSE).

---
 
## 1. Installation & start 
 
### Prerequisits 
- [Git](https://git-scm.com/)
- [Conda](https://docs.conda.io/en/latest/miniconda.html) (optional)
 
### Steps 
 
**1. Clone the repository in the desired folder**
```bash
git clone https://github.com/Elouan003/TabPFN_forward_modelling
cd TabPFN_forward_modelling 
```
 
**2. Create the python environement**

*a) Using conda*
```bash
conda create -n TabPFN_env python=3.10
conda activate TabPFN_env
pip install -r requirements.txt
```

*b) Using venv*

On Mac/Linux
```bash
python3.10 -m venv TabPFN_env
source TabPFN_env/bin/activate
pip install -r requirements.txt
```

On Windows 


```bash
py -3.10 -m venv TabPFN_env
TabPFN_env\Scripts\activate
pip install -r requirements.txt
```
> **Important** The  2 versions using venv require you to have python 3.10 installed on your computer. If it is not clear to you how to do this look into brew, pyenv or conda as recommended above.
 
---
 
## 2. Running the script
 
### a) Prepare your data 
 
Place your data set in the  `data/input/` folder  :
 
```
TabPFN_forward_modelling/
└── data/
    └── input/
        └── your_data.csv   ← here
```
 
The data should be in  `.csv` or `.txt` format . Les columns should include at least the parameters you define in `config.yaml` (see section 3) if there are more columns than what you are using that is fine the programm should ignore them. 
 
> **Supported fromats :** The script can either work with columns separated by tabs/spaces or by commas, in order to adapt this see the "input_format" parameter in config.yaml (section 3). The names of the columns should be the first line of the data and use the same separators as the rest of the data.
 
### b) Configurate the code parameters 
 
This is the most important part of these instructions. The `config.yaml` file containes three sets of parameters that need to be adjusted depending on your needs. The different parameters are explained below. 

You should always set the parameters regarding your data ! Without this the code will not be able to produce any output. Be especially carefull with the names of the columns used as parameters and that are to predict. The programm will warn you if some names you used are not automatically recognized. If that is the case, check the spelling of the parameters as well as the formatting (separator type and so on) of your file. 

### Data related parametres
| Parameter | Type | Description | default value |
|---|---|---|---|
| `data_path` | `string` | Name of the file in `data/input/` | None 
| `input_format` | `string` | Type of separator used in your data file can be `\s+` or `,`| \s+
| `Param_names` | `list` | Name of the columns that are to be used as parameters | None 
| `Predict_names` | `list` | Name of the column that is to be predicetd (usually Radius) | None 



### Programm related parametres
| Parameter | Type | Description |default value |
|---|---|---|---|
| `test_indices` | `list [start,end]` | Intervall of lines to be used to test the precision of rhe predictions If nothing is specified, the code will use a random sample with 20% of your data for the testing. The random sample stas the same through different runs for reproducibility| [0,0]
| `batch_size` | `int` | Number of TabPFN predictions that are run in parallel (default 100). Increasing this number will make the code run faster but if the available memory is not enough it will crash so thread carefully. | 100
| `random_seed` | `int` | In order to have reprducible outputs the random test points are selected based on a seed. You can change this seed here| 42

 


### Output related parametres
| Parameter | Type | Description | default value |
|---|---|---|---|
| `make_plot` | `bool`    | True if you want to generate the pdf plot everytime False if you only want the csv data | True 
| `output_csv` | `string` | Name of csv file generated in `output/csv/` | results.csv
| `output_pdf` | `string` | Name of pdf plot generated in `output/plots/` | results.pdf
---
 


### c) Run the script 
Once everything is set up, run 

```bash
python run.py
```
In the `TabPFN_forward_modelling` folder on your computer. The script will show updates of the progress and signal the more common errors that might occur.


Every time you want to run the programm make sure that the virtual environment is activated ! 
This is done by running the middle line of the procedure explained above.

Using conda 

```bash
conda activate TabPFN_env
```

Without conda on Mac/Linux

```bash
source TabPFN_env/bin/activate
```

Without conda on Windows 

```bash
TabPFN_env\Scripts\activate
```



## 3. Generated outputs

The script automatically generates two files in the  `output/` folder :
 
| File | Description |
|---|---|
| `results.pdf` | Automatically generated plot of the TabPFN predictions against the true values for validation|
| `results.csv` | csv file with 2 columns : the first one is the true values from your data set and the second one are the corresponding values predicted by TabPFN. This can be used to generate your own plots with the data if the automatic one does not meet your needs.|

 

 
---
 

## 4.  Notes and recommendations 
 
 ### Modify the configuration for your use

The `config.yaml` file is where you can set all the parameters for the code. Take some time to read through the different parameters and what they do. This part is central to understanding and using this code. 
 
### In case of missing/not recognized column
The script will automatically produce an error message, if this is the case, telling you which parameters it could not find in the data. Check the spelling and casing of the parameters as well as the `input_format` parameter you are using.
 
### Choose your testing indices
`test_indices: [0, 100]` uses the 100 first lines as test for the models predictions. If you dont specify these the script will pick 20% of the lines at random to use for testing.
 
### Using the raw results for your own work/plots
The file produced in  `output/csv/` contains all necessary data for you to conduct your own analysis of the mode precision. The first columns contains the reals values of the parameter that was to predict, and the second column the values predicted for TabPFN.  
 

 