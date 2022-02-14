# Python
import json
from re import search


# FastAPI
from fastapi import FastAPI
from fastapi import Body, Path
from fastapi import status
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware


# Pydantic
from pydantic import BaseModel
from pydantic import Field

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://micoloans.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Models
class Loan(BaseModel):
    loan_id: str = Field (
        ...
    )
    amount: int = Field(
        ...,
        gt=0
    )
    term: int = Field(
        ...,
        gt=0
    )
    interest_rate: float = Field(
        ...,
        gt=0.01,
        lt=1.00
    )


# Loans
## Loans paths
@app.get(path="/")
def home():
    return {"msg":"app running"}


@app.post(path="/loan", tags=["Loans"])
def create_loan(loan: Loan = Body(...)):
    with open("loans.json", "r+", encoding="utf-8") as file:
        results = json.loads( file.read() )
        loan_dict = loan.dict() 
        results.append(loan_dict)
        file.seek(0)
        file.write(json.dumps(results))

    return loan


@app.get(path="/loan", tags=["Loans"])
def retrive_all_loan():
    with open("loans.json", "r", encoding="utf-8") as file:
        results = json.loads( file.read() )
        
        return results


@app.get(path="/loan/{loan_id}", tags=["Loans"])
def retrive_loan(loan_id: str = Path(...)):
    with open("loans.json", "r", encoding="utf-8") as file:
        results = json.loads( file.read() )
        
        for result in results:
            if result["loan_id" ] == loan_id:
                return result
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This loan {loan_id}. Not Exists!."
        )


@app.put(path="/loan/{loan_id}", tags=["Loans"])
def update_loan(loan_id: str = Path(...), loan: Loan = Body(...) ):
    with open("loans.json","r+", encoding="utf-8") as file:
        results = json.loads( file.read() )
        loan_dict = loan.dict()

        for result in results:
            if result["loan_id"] == loan_id and loan_dict["loan_id"] == loan_id:
                results.remove(result)
                results.append( loan_dict)
                with open("loans.json","w",encoding="utf-8") as f:

                    f.seek(0)
                    f.write( json.dumps(results) )
                    return loan_dict
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"this loan {loan_id}. Not exists!."
        )


@app.delete(path="/loan/{loan_id}", tags=["Loans"])
def delete_loan(loan_id : str = Path(...), loan: Loan = Body(...)):
     with open("loans.json","r+", encoding="utf-8") as file:
        results = json.loads( file.read() )
        loan_dict = loan.dict()

        for result in results:
            if result["loan_id"] == loan_id and loan_dict["loan_id"] == loan_id:
                results.remove(result)
                with open("loans.json","w",encoding="utf-8") as f:

                    f.seek(0)
                    f.write( json.dumps(results) )
                    return loan_dict
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"this loan {loan_id}. Not exists!."
        )


# Amortization
## Amotization Paths
@app.get(path="/loan/{loan_id}/amortization", tags=["Amortization"])
def get_amortization_table(loan_id: str = Path(...)):
    with open("loans.json","r+",encoding="utf-8") as file:
        results = json.loads( file.read() )
        loan = {}
        for result in results:
            if result["loan_id"] == loan_id:
                loan.update( result )
                break
        if len(loan)>0:

            pago_mensual = ( loan["interest_rate"]*loan["amount"]) / (1 - (1+loan["interest_rate"])**-loan["term"] )
            balance = loan["amount"]
            amortization_table = []
            for payment_id in range(loan["term"]+1):
                
                result = calculate_payment(payment_id, pago_mensual,loan["interest_rate"], balance )
                balance = result["balance"]
                amortization_table.append(result)
            
            return amortization_table
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail= f"this loan {loan_id}. Not exists!."
    )


# Utils
def calculate_payment(payment_id, pago_mesual, interest, capital):
    balance = 0
    if payment_id == 0:
        row = {
        "payment_id": payment_id,
        "payment":0,
        "amortization_capital": 0,
        "interest": 0,
        "balance": capital 
    }
    else:
        payment = round(pago_mesual,2)
        interest = round(interest*capital,2)
        amortization_capital =  round( payment - interest,2)
        balance = round(capital - amortization_capital,2)
        row = {
        "payment_id": payment_id,
        "payment":payment,
        "amortization_capital": amortization_capital,
        "interest": interest,
        "balance": balance
    }
    
    return row