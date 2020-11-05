# WebApp for Predicting the Price of Used Cars

This repository consists of files required to create and deploy a machine learning model as a WebApp using Flask for predicting price of used cars in Germany.

### Dataset:
Data is scrapped from eBay Kleinanzeigen, a classifieds section of the German eBay website. For privacy reasons, it isn't uploaded here. However, the repo contains a cleaned copy of the dataset (removing all personal information).

### Methodology:
Here are the following steps taken into consideration in developing the prediction model. Refer [ML_pipeline.ipynb](ML_pipline.ipynb) for step by step explanation.
1. Data cleaning - Handling missing values by imputations and performing outlier detection using Inter Quantile Range method  
2. Data Visualization - categorical EDAs  
[!Screenshot](readme_resource/categorical_eda.png)   
3. Feature Engineering - Categorical encoding, feature importance and selection  
4. Model Selection - Comparing different regressor models and choosing the best one with the least RMSE and highest r2 score  
[!Screenshot](readme_resource/models.png)  
5. Hyperparameter tuning and Optimization for Random Forest Regressor  
6. Car price prediction and evaluation  

### Files:
| filename | Description |
|----------|-------------|
| requirements.txt | Basic libraries and packages required for execution |
| cleaned_car_data.csv | Cleaned Dataset |
| ML_pipeline.ipynb | Notebook (step by step explanation) |
| backend_model.py, app.py | Python scripts for model creation and deployment |
| regressor.pkl | Backend model(serialized) for Webapp |
| static/*, templates/* | Front-end (HTML CSS styling) for Webapp |

### Steps to Execute:
1. Git clone the repository. Make sure you have all the libraries and packages as mentioned in the requirements.txt
2. Run ```python3 app.py```
3. Open the browser and go to URL : http://127.0.0.1:5000/
4. Fill the required fields (Type of Gearbox, Mileage Driven, Registration Year, Type of Fuel and Type of the vehical) to get your result.  

### TestApp:

[!Screenshot](readme_resource/how_to_use.gif)
  










