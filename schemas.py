from typing import List

from pydantic import BaseModel


class LinkModel(BaseModel):
    products: List[dict]
