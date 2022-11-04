from telegram.ping_bot_base     import dev_logger, usr_logger
from telegram.ping_bot_database import ping_bot_database_manager

import pytest, warnings, sqlite3

DATABASE_NAME  = "bot-users.sqlite3"
DATABASE_DUMP  = "bot-users-dump.sqlite3"

DATABASE_NAME_CORRUPTED  = DATABASE_NAME  + "JASid1*(&SDmn.doesnotexits"
DATABASE_DUMP_CORRUPTED  = DATABASE_DUMP  + "ASD*(&(()@#DS.doesnotexits"

database_class : ping_bot_database_manager = None

class Test_database_io_assertation_control:

    @pytest.mark.filterwarnings("ignore::RuntimeWarning")
    def test_database_ioctl_assert_dbfile(self) -> None:
        # Call static method from database class to ensure that
        # *current* file-exists-check is raises correct exception.
        # with corrupted database filename(ex.: performs correct
        # file-does-exist-check.
        with pytest.raises(SystemExit):
            ping_bot_database_manager.__assert_file_exists__(DATABASE_DUMP_CORRUPTED)
   
    def test_database_ioctl_assert_dbfile_with_right_dbfile(self) -> None:
        # Now assert that the function works well with
        # correct database.
        ping_bot_database_manager.__assert_file_exists__(DATABASE_NAME)
       
    @pytest.mark.filterwarnings("ignore::RuntimeWarning")
    def test_database_ioctl_assert_connection(self) -> None:
        # Call static method from database class to ensure that
        # *current* connection-exists is raises correct exception.
        # with corrupted database filename(ex.: performs correct
        # connection check.       
         with pytest.raises(SystemExit):
            ping_bot_database_manager.__assert_connection_established__(DATABASE_DUMP_CORRUPTED)
 
    def test_database_ioctl_connects_succesfully(self) -> None:
        # Call ping_bot_database_manager::constructor to verify
        # that database connects succesfully with no error\warings
        # using correct database.
        database_class = ping_bot_database_manager(DATABASE_DUMP)
    
    def test_database_ioctl_add_user(self) -> None:
        # Call ping_bot_database_manager::add_user() to
        # verify that databse process adding succesfully
        database_class = ping_bot_database_manager(DATABASE_DUMP)
        database_class.add_user("1288")
