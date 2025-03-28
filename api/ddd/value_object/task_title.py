from api.ddd.value_object.exception import ValueObjectError


class TaskTitle:
    def __init__(self, name: str) -> None:
        # Falsyはエラー
        if not name:
            raise ValueObjectError("名前は1文字以上で入力してください")
        # 255文字以上はエラー
        if len(name) > 255:
            raise ValueObjectError("タスク名は255文字以下にしてください")
        self.name: str = name

    def value(self) -> str:
        return self.name
