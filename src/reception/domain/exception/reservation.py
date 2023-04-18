from shared_kernel.exception import BaseMsgException


class ReservationNotFoundException(BaseMsgException):
    message = "Reservation is not found."


class ReservationStatusException(BaseMsgException):
    message = "Invalid request for current reservation status."
