import uuid


class API_Core:
    def __init__(self):
        pass

    def generate_key(self):
        key = str(uuid.uuid4())
        return key


class DataBase:
    def __init__(self):
        self.core = API_Core()

    def add_key(self):
        pass  # TODO

    def __check_key_access(self, key: str) -> int:
        pass  # TODO

    def do_some_action(self, key: str, action: str):
        pass  # TODO

    def get_all_keys(self) -> list:
        pass  # TODO