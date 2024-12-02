from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Field, ForeignKey, String, Date, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from src.database import BaseOrm
import datetime as dt


class BookingsOrm(BaseOrm):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_from: Mapped[dt.date] = mapped_column(Date)
    date_to: Mapped[dt.date] = mapped_column(Date)
    price: Mapped[int] = mapped_column(Integer)


    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days()