from api.domain.models.user.i_equatable import IEquatable
from api.domain.models.user.user_name import UserName


class User(IEquatable["User"]):

    def __init__(self, id: int, user_name: str, display_name: str) -> None:
        self.__id = id
        self.__user_name: UserName = UserName(user_name)
        self.__display_name: str = display_name

    @property
    def id(self) -> int:
        return self.__id

    @property
    def user_name(self) -> UserName:
        return self.__user_name

    @property
    def display_name(self) -> str:
        return self.__display_name

    def equals(self, other: "User") -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id
