from telegram.ping_bot_base     import dev_logger, usr_logger
from telegram.ping_bot_database import ping_bot_database_manager

import pytest, warnings

DATABASE_NAME  = "bot-users.sqlite3"
DATABASE_DUMP  = "bot-users-dump.sqlite3"

DATABASE_NAME_CORRUPTED  = DATABASE_NAME  + "JASid1*(&SDmn.doesnotexits"
DATABASE_DUMP_CORRUPTED  = DATABASE_DUMP  + "ASD*(&(()@#DS.doesnotexits"

class Test_database_io_assertation_control:

    @pytest.mark.filterwarnings("ignore::RuntimeWarning")
    def test_database_ioctl_assert_dbfile(self):
        # Call static method from database class to ensure that
        # *current* file-exists-check is raises correct exception.
        # with corrupted database filename(ex.: performs correct
        # file-does-exist-check.
        with pytest.raises(SystemExit):
            ping_bot_database_manager.__assert_file_exists__(DATABASE_DUMP_CORRUPTED)
    
    @pytest.mark.filterwarnings("ignore::RuntimeWarning")
    def test_database_ioctl_assert_connection(self):
        # Call static method from database class to ensure that
        # *current* connection-exists is raises correct exception.
        # with corrupted database filename(ex.: performs correct
        # connection check.       
         with pytest.raises(SystemExit):
            ping_bot_database_manager.__assert_connection_established__(DATABASE_DUMP_CORRUPTED)
    

def test_database_connects_succesfully():
    # Connect using default constructor on a dump database
    #database_instance = ping_bot_database_manager("bot-users-dump.sqlite3")
    pass

    
