from fastapi import FastAPI, Depends
import schemas
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
import requests
import json
import os

app = FastAPI()
models.Base.metadata.create_all(engine)

api_key = os.getenv("API_KEY")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_assets_with_native_balance(api_key, owner_address):
    headers = {"Content-Type": "application/json"}

    body = {
        "jsonrpc": "2.0",
        "id": "my-id",
        "method": "getAssetsByOwner",
        "params": {
            "ownerAddress": owner_address,
            "displayOptions": {"showFungible": True, "showNativeBalance": True},
        },
    }

    url = "https://mainnet.helius-rpc.com/?api-key=" + api_key
    response = requests.post(url, headers=headers, data=json.dumps(body))
    result = response.json().get("result", {})

    return result


@app.get("/net-worth")
def net_worth_by_wallet_address(request: schemas.Wallet):
    output = get_assets_with_native_balance(api_key, request.wallet_address)
    net_worth = output["nativeBalance"].get("total_price")

    filtered_items = [
        item
        for item in output.get("items", [])
        if item.get("interface") == "FungibleToken"
    ]

    for data in filtered_items:
        price_info = data["token_info"].get("price_info")
        if price_info:
            net_worth += price_info.get("total_price")

    print(f"Address: {request.wallet_address} | Net Worth: ${net_worth} USDC")
    return net_worth
