

class UserName:
    def __init__(self, value: str):
        if not value:
            raise ValueError("User name cannot be empty")
        if len(value) < 3:
            raise ValueError("User name must have at least 3 characters")
        if len(value) > 50:
            raise ValueError("User name must have at most 50 characters")
        self.value = value

    def __str__(self) -> str:
        return self.value
