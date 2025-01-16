from pydantic import BaseModel
from typing import Optional, List


class Wallet(BaseModel):
    wallet_address: str
