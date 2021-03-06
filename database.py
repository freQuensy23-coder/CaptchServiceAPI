import time
import uuid
import pymysql
from pymysql.cursors import DictCursor
import database_config as config
import Access_levels

import logging

log = logging.getLogger("db")


class API_Core:
    def __init__(self):
        pass

    def generate_key(self):
        key = str(uuid.uuid4())
        return key


class DataBase:
    def __init__(self):
        self.core = API_Core()
        self.connection = pymysql.connect(
            host=config.host,
            user=config.name,
            password=config.passwd,
            db=config.name,
            charset="utf8",
            cursorclass=DictCursor
        )

        self.cursor = self.connection.cursor()
        timeout = 2147482
        self.cursor.execute(query=f"""SET SESSION wait_timeout := {timeout};""")
        self.connection.commit()
        log.debug("db inited")

    def add_key(self, access=10, expires=Access_levels.key_live_time)->str:
        self.__open_connection()
        key = self.core.generate_key()
        q = f"""INSERT INTO api_keys (access, api_key, expires) VALUES ({access}, '{key}', {int(time.time()) + expires})"""
        cur = self.connection.cursor()
        cur.execute(q)
        self.connection.commit()
        self.__close_connection()
        return key

    def __check_key_access(self, key: str) -> int:
        """Get access level for key"""
        self.__open_connection()
        q = f"""SELECT access FROM api_keys WHERE api_key='{key}'"""
        cur = self.connection.cursor()
        cur.execute(q)
        self.__close_connection()
        return cur.fetchone()["access"]

    def do_some_action(self, key: str, action: str):
        acc = self.__check_key_access(key=key)
        log.debug(f"Doing action {action} {time.time()}")
        if acc >= eval(f"Access_levels.{action}"):
            if action == "get_captcha":
                return True
                # TODO Time limit
            if action == "get_unlim_captcha":
                return True
            if action == "add_new_user":
                key = self.add_key()
                return key
            if action == "del_user":
                pass # TODO
            if action == "get_user_data":
                pass # TODO

    def get_all_keys(self) -> list:
        self.__open_connection()
        q = f"""SELECT * FROM api_keys"""
        cur = self.connection.cursor()
        cur.execute(q)
        self.__close_connection()
        return cur.fetchall()

    def del_user(self, key):
        pass # TODO

    def __open_connection(self):
        self.connection = pymysql.connect(
            host=config.host,
            user=config.name,
            password=config.passwd,
            db=config.name,
            charset="utf8",
            cursorclass=DictCursor
        )

        self.cursor = self.connection.cursor()
        timeout = 2147482
        self.cursor.execute(query=f"""SET SESSION wait_timeout := {timeout};""")
        self.connection.commit()
        log.debug("db reinited")

    def __close_connection(self):
        log.debug("connection_close")
        self.connection.close()