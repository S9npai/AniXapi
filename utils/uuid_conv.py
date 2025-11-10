import uuid
from sqlalchemy.types import TypeDecorator, BINARY


class UUIDBinary(TypeDecorator):
    impl = BINARY(16)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, bytes):
            return value
        if isinstance(value, str):
            return uuid.UUID(value).bytes
        if isinstance(value, uuid.UUID):
            return value.bytes
        raise ValueError(f"Cannot convert {type(value)} to UUID binary")

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return str(value)
        return str(uuid.UUID(bytes=value))
