# TabPFN forwawrd modelling 
 
 This repository contains the code necessary to fit the TabPFN model to a part of your training data set and make predictions for the rest of the data points. The data used for the fitting are normally the interior parameters of the planet such as core/mantel mass, water mass fraction or Mg to Si mantle mass ratio but can also be extended to more general parameters of the planet such as age or different types of mixing assumptions. 

 
---
 
## 1. Installation & start
 
### Prerequisits 
- [Git](https://git-scm.com/)
- [Conda](https://docs.conda.io/en/latest/miniconda.html) (optional)
 
### Steps 
 
**1. Clone the repository in the desired folder**
```bash
git clone https://github.com/votre-repo/nom-du-projet.git
cd project_name 
```
 
**2. Create the python environement**

*a. Using conda*
```bash
conda create -n nom_env python=3.10
conda activate nom_env
pip install -r requirements.txt
```

*b. Using venv*

On Mac/Linux
```bash
python3 -m venv TabPFN_env
source TabPFN_env/bin/activate
pip install -r requirements.txt
```

On Windows 


```bash
python -m venv TabPFN_env
TabPFN_env\Scripts\activate
pip install -r requirements.txt
```


**3. Launch the script **
```bash
python run.py
```

Every time you want to run the programm make sure that the virtual environment is activated ! 
This is done by running the middle line of the procedure explained above.

Using conda 

```bash
conda activate TabPFN_env
```

Without conda on Mac/Linux

```bash
conda activate TabPFN_env
```

Without conda on Windows 

```bash
conda activate TabPFN_env
```
 
---
 
## 2. Running the script
 
### a) Prepare your data 
 
Place your data set in the  `data/input/` folder  :
 
```
nom-du-projet/
└── data/
    └── input/
        └── your_data.csv   ← here
```
 
The data should be in  `.csv` or `.txt` format . Les columns should include at least  the parameters you define in `config.yaml` (see section 3) if there are more columns than what you are using that is fine the programm should ignore them. 
 
> **Supported fromats :** The script can either work with columns separated by tabs/spaces or by commas, in order to adapt this see the "separator" parameter in config.yaml(section 3). The names of the columns should be the first line of the data and use the same separators as the rest of the data.
 
### b) Configurate `config.yaml`
 
This is the most important part of these instructions. The `config.yaml` file containes three sets of parameters that need to be adjusted depending on your needs. The different parameters are explained below. 

### Data related parametres
| Parameter | Type | Description |
|---|---|---|
| `data_path` | `string` | Name of the file in `data/input/` |
| `input_format` | `string` | Type of separator used in your data file can be either `\s+` or `,`| 
| `Param_names` | `list` | Name of the columns that are to be used as parameters |
| `Predict_names` | `list` | Name of the column that is to be predicetd (usually Radius) |

---

### Programm related parametres
| Parameter | Type | Description |
|---|---|---|
| `test_indices` | `list [start, end]` | Intervall of lines to be used to test the precision of rhe predictions If nothing is specified, the code will use a random sample with 20% of your data for the testing. The random sample stas the same through different runs for reproducibility|
| `batch_size` | `int` | Number of TabPFN predictions that are run in parallel (default 100). Increasing this number will make the code run faster but if the available memory is not enough it will crash so thread carefully. |
| `random_seed` | `int` | In order to have reprducible outputs the random test points are selected based on a seed. You can change this seed here|
---
 


### Output related parametres
| Parameter | Type | Description |
|---|---|---|
| `make_plot` | `bool` |  | True if you want to generate the pdf plot everytime False if you only want the csv data
| `output_csv` | `string` | Name of csv file generated in `output/csv/` |
| `output_pdf` | `string` | Name of pdf plot generated in `output/plots/` |
---
 


### c) Outputs générés
 
The script automaticall generates two files in the  `output/` folder :
 
| File | Description |
|---|---|
| `results.pdf` | Automatically generated plot of the TabPFN predictions against the true values for validation|
| `results.csv` | csv file with 2 columns : the frist one is the true values from your data set and the second one are the corresponding values predicted by TabPFN. This can be used to generate your own plots with the data if the automatic one does not meet your needs.|
 

 
---
 

## 4. Conseils d'utilisation
 
**Vérifier les colonnes reconnues**
Au lancement, le script affiche les colonnes détectées dans votre fichier. Assurez-vous qu'elles correspondent exactement aux noms dans `config.yaml` (sensible à la casse).
 
**En cas de colonne manquante**
Le script affichera un message d'erreur explicite indiquant quelle colonne est introuvable ainsi que la liste des colonnes disponibles.
 
**Choisir ses indices de test**
`test_indices: [0, 10]` réserve les lignes 0 à 9 pour le test. Si vous ne spécifiez pas cet argument, le script effectue un split aléatoire automatiquement.
 
**Réutiliser les données de sortie**
Le fichier `output/results.csv` contient toutes les données nécessaires pour reproduire ou personnaliser le graphique avec l'outil de votre choix (Excel, Python, R...).
 
**Modifier la configuration sans relancer**
Vous pouvez modifier `config.yaml` entre deux lancements sans toucher au code. C'est le seul fichier à éditer pour changer le comportement du script.
 