from pydantic import BaseModel, ConfigDict
import datetime as dt


class Bookings(BaseModel):
    room_id: int
    user_id: int
    date_from: dt.date
    date_to: dt.date
    price: int