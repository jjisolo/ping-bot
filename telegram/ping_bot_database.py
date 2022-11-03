from ping_bot_base.py import dev_logger, usr_logger

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

        

