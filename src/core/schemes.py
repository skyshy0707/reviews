from datetime import datetime
from typing import Annotated, List, Literal, Tuple, Union

from fastapi import Query
from pydantic import BaseModel, computed_field, Field, model_serializer
from pydantic.fields import FieldInfo
from pydantic.main import create_model


class Pagination(BaseModel):
    limit: int = Query(10, gt=0, le=100)
    offset: int = Query(0, ge=0)


def create_pagination_response_model(model) -> BaseModel:
    items_type = List[model]
    total_type = Annotated[int, Field(0, ge=0)]
    return create_model(
        "Items",
        __base__=Pagination,
        **{
            "items": (
                items_type,
                FieldInfo(
                    annotation=items_type
                )
            ),
            "total": (
                total_type,
                FieldInfo(
                    annotation=total_type,
                )
            )
        }
    )

def as_tuple(obj: list) -> Union[str, Tuple[str]]:
    return str(tuple(obj)).replace(",", "") if len(obj) == 1 else tuple(obj)


class ReviewCommonFields(BaseModel):
    text: str

class Review(ReviewCommonFields):
    id: int
    sentiment: str
    created_at: str

    @model_serializer(when_used='json')
    def order_fields(self) -> dict:
        data = { "id": self.id }
        data.update(dict(self))
        return data

class ReviewCreate(ReviewCommonFields):

    @computed_field(return_type=str)
    @property
    def created_at(self) -> str:
        return datetime.now().isoformat()

    @computed_field(return_type=str)
    @property
    def sentiment(self) -> Literal["negative", "neutral", "positive"]:
        SENTIMENT_TYPES = {
            "negative": [
                "плох",
                "ненави"
            ],
            "positive": [
                "люб",
                "отличн"
            ]
        }
        for evaluation, content in SENTIMENT_TYPES.items():
            for word in content:
                if word.lower() in self.text:
                    return evaluation
                
        return "neutral"

class SearchReviews(Pagination):
    sentiment: List[str] = Field(Query([]))