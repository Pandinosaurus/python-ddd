from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, String, Table, Text, UniqueConstraint
from sqlalchemy.orm import composite, registry, relationship

from reception.domain.entity.room import Room
from reception.domain.value_object.guest import Guest
from reception.domain.value_object.reservation import ReservationNumber
from shared_kernel.domain.value_object import ReservationStatus, RoomStatus

metadata = MetaData()
mapper_registry = registry()


room_table = Table(
    "hotel_room",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("number", String(20), nullable=False),
    Column("status", String(20), nullable=False),
    Column("image_url", String(200), nullable=False),
    Column("description", Text, nullable=True),
    UniqueConstraint("number", name="uix_hotel_room_number"),
)

reservation_table = Table(
    "room_reservation",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("room_id", Integer, ForeignKey("hotel_room.id"), nullable=False),
    Column("number", String(20), nullable=False),
    Column("status", String(20), nullable=False),
    Column("date_in", DateTime(timezone=True)),
    Column("date_out", DateTime(timezone=True)),
    Column("guest_mobile", String(20), nullable=False),
    Column("guest_name", String(50), nullable=True),
)


def init_orm_mappers():
    """
    initialize orm mappings
    """
    from reception.domain.entity.reservation import Reservation as ReceptionReservationEntity
    from reception.domain.entity.room import Room as ReceptionRoomEntity

    mapper_registry.map_imperatively(
        ReceptionRoomEntity,
        room_table,
        properties={
            "room_status": composite(RoomStatus.from_value, room_table.c.status),
        }
    )
    mapper_registry.map_imperatively(
        ReceptionReservationEntity,
        reservation_table,
        properties={
            "room": relationship(Room, backref="reservations", order_by=reservation_table.c.id.desc, lazy="joined"),
            "reservation_number": composite(ReservationNumber.from_value, reservation_table.c.number),
            "reservation_status": composite(ReservationStatus.from_value, reservation_table.c.status),
            "guest": composite(Guest, reservation_table.c.guest_mobile, reservation_table.c.guest_name),
        }
    )

    from display.domain.entity.room import Room as DisplayRoomEntity

    mapper_registry.map_imperatively(
        DisplayRoomEntity,
        room_table,
        properties={
            "room_status": composite(RoomStatus.from_value, room_table.c.status),
        }
    )
