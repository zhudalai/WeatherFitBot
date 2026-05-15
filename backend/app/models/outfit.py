from pydantic import BaseModel


class OutfitAdvice(BaseModel):
    summary: str
    top: str
    bottom: str
    shoes: str
    accessories: str
    tips: str
