from telegram.ping_bot_base import dev_logger, usr_logger, log_meta, commit_critical_error, WARNING_CRITICAL_HIT

import sqlite3, typing, os, warnings

class ping_bot_database_manager(object):
    """
    Description:
        Base database manager class, that aggregates
        different methods for working with sqlite3 database.

    """

    def __init__(self, database_filename : str) -> None:
        """
        Description:
            Initialize the database object. Try to establish
            connection with the database.

        Args:
            database_filename: filename of the database

        Returns: None
        """
        dev_logger.debug(("Initializing sqlite3 database"))
        
        # Verify that given filename is valid.
        self.__assert_file_exists__(database_filename)
        
        # Establish connection.
        self.__connection = sqlite3.connect(database_filename)

        # Verify that the connection has been established.
        self.__assert_connection_established__(database_filename)
        
        self.__cursor = self.__connection.cursor()

    def __assert_file_exists__(self, database_filename) -> None:
        """
        Description:
            Assert that the database file exists. If not report an error
            to the /logs/deb_log.log file.

        Returns: None

        """
        result = os.path.exists(database_filename)

        if not result:
            commit_critical_error("Requested database file does not exist.")
        else:
            dev_logger.debug("Performed database file existing check.")

    def __assert_connection_established__(self, database_filename: str) -> None:
        """
        Check if *something* is connected to the database, if not
        report an error to the dev logging pipe.

        """
        try:
            self.__connection.cursor()
        except Exception as e:
            commit_critical_error("No connection to the database has been established: {}".format(e))

    @property
    def connection(self) -> sqlite3.Connection:
        """
        Description:
            Database connection getter.

        Returns: (sqlite3.Connection) class instance.
        """
        return self.__connection
        
    @property
    def cursor(self) -> sqlite3.Cursor:
        """
        Description:
            sqlite3 cursor getter.

        Returns: (sqlite3.Cursor) class instance.

        """
        return self.__cursor

    def add_user(self, chat_id: typing.Union[str, int]) -> None:
        """
        Description:
            Add new `char_id`(add new user) to the database. If the
            user is not distinct then do nothing.

        Args:
            chat_id: telegram chat id of the user.

        Returns: None

        """
        if self.contains(chat_id): 
            dev_logger.warning(log_meta["database-non-distinct-add"].format("telegram-users", "chat_id", chat_id))

            return 

        else:
            dev_logger.info(log_meta["database-insert"].format("telegram-users", "chat_id", chat_id))

            self.__cursor.execute(
                "INSERT INTO 'telegram-users' ('chat_id') VALUES (?)",
                (chat_id,)
            )

            return self.__connection.commit()

    def add_ip(self, chat_id: typing.Union[str, int], ip_address: str, exist_ok: bool = False) -> None:
        """
        Description:
            add `ip-adress` record to the `data-chain` table.

        Args:
            chat_id: telegram chat id of the user.
            ip_address: ip-address to start track.
            exist_ok: add only if the ip address is distinct
        Returns: None

        """
        dev_logger.info(log_meta["database-insert"].format("data-chain", "ip-address", ip_address))

        # If the ip already linked to the user.
        if exist_ok is False and bool(len(self.get_ip(chat_id))) is True:
            dev_logger.warning(log_meta["database-non-distinct-add"].format("data-chain", "ip-address", chat_id))
            return

        self.__cursor.execute(
            "INSERT INTO 'data-chain' ('chat_id', 'ip-address') VALUES (?, ?)",
            (self.__convert_from_telegram_id__(chat_id), ip_address)
        )

        return self.__connection.commit()

    def get_ip(self, chat_id: typing.Union[str, int]) -> typing.List[str]:
        """
        Description:
            get all tracked ip's if user

        Args:
            chat_id: telegram chat id of the user.

        Returns: List tracked ip addresses of the user.
        """
        result = self.__cursor.execute(
            "SELECT * FROM 'data-chain' WHERE `chat_id` = ?",
            (self.__convert_from_telegram_id__(chat_id), )
        )

        return result.fetchall()

    def remove_ip(self, chat_id: typing.Union[str, int], ip_address: str) -> None:
        """
        Description:
            remove `ip-adress` record to the `data-chain` table.

        Args:
            chat_id: telegram chat id of the user.
            ip_address: ip-address to start track.

        Returns: None

        """
        dev_logger.info(log_meta["database-delete"].format("data-chain", "ip-address", ip_address))

        self.__cursor.execute(
            "DELETE FROM `data-chain` WHERE `chat_id` = ? AND `ip-address` = '"+ip_address+"'",
            (self.__convert_from_telegram_id__(chat_id), )
        )

        return self.__connection.commit()

    def __convert_from_telegram_id__(self, user_id : typing.Union[str, int]) -> str:
        """
        Description:
            get database id from chat_id.
        Args:
            user_id: telegram chat id of the user.

        Returns: (str) id database record.

        """
        dev_logger.info(log_meta["database-get"].format("telegram-users", "id"))

        result = self.__cursor.execute(
            "SELECT `id` FROM `telegram-users` WHERE `chat_id` = ?",
            (user_id, )
        )

        return result.fetchone()[0]
    
    def __convert_from_id__(self, user_id : typing.Union[str, int]) -> str:
        """
        Description:
            get database id from chat_id.
        Args:
            user_id: database id of the user.

        Returns: (str) chat_id database record.

        """
        dev_logger.info(log_meta["database-get"].format("telegram-users", "id"))

        result = self.__cursor.execute(
            "SELECT `chat_id` FROM `telegram-users` WHERE `id` = ?",
            (user_id, )
        )
        
        return result.fetchone()[0]
        
    def contains(self, chat_id: typing.Union[str, int]) -> bool:
        """
        Description:
            check if user already exists id the database.

        Args:
            chat_id: telegram chat id of the user.

        Returns: (bool) Result of the request.

        """
        dev_logger.info(log_meta["database-get"].format("telegram-users", "id"))

        result = self.__cursor.execute(
            "SELECT `id` FROM `telegram-users` WHERE `chat_id` = ?",
            (chat_id,)
        )

        return bool(len(result.fetchall()))

    def disconnect(self) -> None:
        """
        Description:
            close the connection to the database.
        """
        self.__connection.close()