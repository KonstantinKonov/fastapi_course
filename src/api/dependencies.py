from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, gt=0)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


class Hotel(BaseModel):
    title: Annotated[str, Query()]
    name: Annotated[str, Query()]


class HotelPatch(BaseModel):
    title: Annotated[str | None, Query(None)]
    name: Annotated[str | None, Query(None)]


PaginationDep = Annotated[PaginationParams, Depends()]
HotelDep = Annotated[Hotel, Depends()]
HotelPatchDep = Annotated[HotelPatch, Depends()]