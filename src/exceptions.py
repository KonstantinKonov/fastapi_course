from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = 'Unknown error'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Object not found"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "No more rooms"


class AlreadyExists(NabronirovalException):
    detail = "This room/hotel/facility already exists"


class Hotel404(HTTPException):
    detail = "hotel not found"
    status_code = 404


class Room404(HTTPException):
    detail = "room not found"
    status_code = 404