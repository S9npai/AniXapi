from uuid import UUID, uuid4
from sqlalchemy.types import TypeDecorator, BINARY
import uuid

def binary_to_uuid(binary_uuid:bytes) -> str:
    return str(UUID(bytes=binary_uuid))

def uuid_to_binary(uuid_str:str) -> bytes | None:
    if uuid_str is None:
        return None
    try:
        return UUID(uuid_str).bytes
    except ValueError:
        return None

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
