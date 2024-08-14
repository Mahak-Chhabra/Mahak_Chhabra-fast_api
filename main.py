from fastapi import FastAPI, Depends, HTTPException, Header
from . import crud, schemas
from .database import sync_table

app = FastAPI()

# Initialize tables
sync_table()


@app.post("/accounts/", response_model=schemas.UserAccount)
def account_(account: schemas.AccountCreate):
    return crud.create_user_account(account_data=account)


@app.post("/accounts/{account_id}/destinations/", response_model=schemas.EndDestination)
def destination_(account_id: str, destination: schemas.DestinationCreate):
    return crud.create_end_destination(destination_data=destination, account_id=account_id)


@app.get("/accounts/{account_id}/destinations/", response_model=list[schemas.EndDestination])
def getdestinations_(account_id: str):
    return crud.get_end_destinations_by_account_id(account_id=account_id)


@app.post("/server/incoming_data/")
def incoming_data(data: dict, x_token: str = Header(None)):
    if not x_token:
        raise HTTPException(status_code=401, detail="Un Authenticate")

    account = crud.get_user_account_by_token(token=x_token)
    if not account:
        raise HTTPException(status_code=401, detail="Un Authenticate")

    destinations = crud.get_end_destinations_by_account_id(account_id=account.id)
    if not destinations:
        return {"status": "No destinations found"}

    for destination in destinations:
        data_destination(destination, data)

    return {"status": "success"}


def data_destination(destination, data):
    import requests

    headers = destination.headers
    if destination.http_method.upper() == "GET":
        response = requests.get(destination.url, headers=headers, params=data)
    else:
        response = requests.post(destination.url, headers=headers, json=data)

    if not response.ok:
        raise HTTPException(status_code=500, detail=f"Failed to send data to {destination.url}")
