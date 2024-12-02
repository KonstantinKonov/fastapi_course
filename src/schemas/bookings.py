from pydantic import BaseModel, ConfigDict
import datetime as dt


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: dt.date
    date_to: dt.date


class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: dt.date
    date_to: dt.date


class Booking(BookingAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)