'''Models used in the API e.g in the request body'''
from pydantic import BaseModel


class Date(BaseModel):
    '''
    Specific date without time.
    '''
    year: int = 2022
    month: int | None = 1
    day: int | None = 1
