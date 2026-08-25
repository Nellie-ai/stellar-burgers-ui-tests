from dataclasses import dataclass
from uuid import uuid4


DEFAULT_INGREDIENT = "Флюоресцентная булка R2-D3"


@dataclass(frozen=True)
class User:
    email: str
    password: str
    name: str
    access_token: str = ""
    refresh_token: str = ""


def generate_user() -> User:
    unique_id = uuid4().hex
    return User(
        email=f"diplom3_{unique_id}@example.com",
        password=f"Qa-{unique_id[:12]}",
        name=f"QA {unique_id[:8]}",
    )
