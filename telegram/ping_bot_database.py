from telegram.ping_bot_base import dev_logger, usr_logger, commit_critical_error, WARNING_CRITICAL_HIT

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
        
        self.__assert_file_exists(database_filename)
        self.connection = sqlite3.connect(database_filename)
        self.__assert_connection__(database_filename)
        
        self.cursor = self.connection.cursor()
    
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
            dev_logger.info("Performed database file existing check.")
    
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
                        if file.path == database_filename:
                            return
            except psutil.NoSuchProcess as error:
                commit_critical_error("Expirienced psutil error:", error)

        commit_critical_error("No connection to the database has been established.")
 
