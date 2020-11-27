# This file consists of the base model for bank customer churn prediction
from pydantic import BaseModel
class ChurnModel(BaseModel):
    Geography: str
    CreditScore: float 
    Gender: bool 
    Age: int 
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: bool
    IsActiveMember: bool
    EstimatedSalary: float
    
