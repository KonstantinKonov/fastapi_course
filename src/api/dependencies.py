from typing import Annotated
from fastapi import Depends, Query, Body
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, gt=0)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


class Hotel(BaseModel):
    title: Annotated[str, Body()]
    location: Annotated[str, Body()]


class HotelPatch(BaseModel):
    title: Annotated[str | None, Body()]
    location: Annotated[str | None, Body()]


PaginationDep = Annotated[PaginationParams, Depends()]
HotelDep = Annotated[Hotel, Depends()]
HotelPatchDep = Annotated[HotelPatch, Depends()]