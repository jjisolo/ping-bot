from telegram.ping_bot_base import dev_logger, usr_logger, log_meta, commit_critical_error, WARNING_CRITICAL_HIT

import sqlite3, psutil, typing, os, warnings

class ping_bot_database_manager(object):
    """
    Base database manager class, that aggregates
    different methods for working with sqlite3 database.
    """

    def __init__(self, database_filename : str) -> None:
        """
        Establish connection to the database.

        :param databse_filename(str): filename of the database.
        """
        dev_logger.debug(("Initializing sqlite3 database"))
        
        # Verify that given filename is valid.
        self.__assert_file_exists__(database_filename)
        
        # Establish connection.
        self.__connection = sqlite3.connect(database_filename)

        # Verify that the connection has been established.
        self.__assert_connection_established__(database_filename)
        
        self.__cursor = self.__connection.cursor()
    
    @classmethod # For Unit-Testing.
    def __assert_file_exists__(cls, database_filename) -> None:
        """
        Check if the requested file exists, if not report an error
        to the dev logging pipe.
        """
        result = os.path.exists(database_filename)

        if not result:
            commit_critical_error("Requested database file does not exist.")
        else:
            dev_logger.debug("Performed database file existing check.")
    
    @classmethod # For Unit-Testing.
    def __assert_connection_established__(cls, database_filename: str) -> None:
        """
        Check if *something* is connected to the database, if not
        report an error to the dev logging pipe.
        """
        for procedure in psutil.process_iter():
            try:
                files = procedure.open_files()
                if files:
                    for file in files:
                        if database_filename in file.path:
                            return
            except psutil.NoSuchProcess as error:
                commit_critical_error("Expirienced psutil error:", error)

        commit_critical_error("No connection to the database has been established.")

    @property
    def connection(self) -> sqlite3.Connection:
        """
        Database connection getter.
        """
        return self.__connection
        
    @property
    def cursor(self) -> sqlite3.Cursor:
        """
        Databse cursor getter.
        """
        return self.__cursor

    def add_user(self, chat_id: typing.Union[str, int]) -> None:
        """
        Add user id to the database
        """

        if self.contains(chat_id): 
            dev_logger.warning(log_meta["database-non-distinct-add"].format("telegram-users", "chat_id", chat_id))

            return 

        else:
            self.__cursor.execute("INSERT INTO 'telegram-users' ('chat_id') VALUES (?)", (chat_id,))

            dev_logger.info(log_meta["database-insert"].format("telegram-users", "chat_id", chat_id))

            return self.__connection.commit()

    def __convert_from_telegram_id__(self, user_id : typing.Union[str, int]) -> str:
        """
        static_cast<column::id>(column::chat_id);
        """
        result = self.__cursor.execute("SELECT `id` FROM `telegram-users` WHERE `chat_id` = ?", (user_id, ))

        dev_logger.info(log_meta["database-get"].format("telegram-users", "id"))

        return result.fetchone[0]
    
    def __convert_from_id__(self, chat_id : typing.Union[str, int]) -> str:
        """
        static_cast<column::chat_id>(column::id);
        """
        result = self.__cursor.execute("SELECT `chat_id` FROM `telegram-users` WHERE `id` = ?", (chat_id, ))

        dev_logger.info(log_meta["database-get"].format("telegram-users", "id"))

        return result.fetchone[0]
        
    def contains(self, chat_id: typing.Union[str, int]) -> bool:
        """
        Check if chat_id is already in database. True if contains, False if not.
        """
        result = self.__cursor.execute("SELECT `id` FROM `telegram-users` WHERE `chat_id` = ?", (chat_id,))

        dev_logger.info(log_meta["database-get"].format("telegram-users", "id"))

        return bool(len(result.fetchall()))

