from telegram.ping_bot_base import dev_logger, usr_logger, log_meta
from telegram.ping_bot_database import ping_bot_database_manager

import pytest, warnings, sqlite3, logging

DATABASE_NAME = "bot-users.sqlite3"
DATABASE_DUMP = "bot-users-dump.sqlite3"

DATABASE_NAME_CORRUPTED = DATABASE_NAME + "JASid1*(&SDmn.doesnotexits"
DATABASE_DUMP_CORRUPTED = DATABASE_DUMP + "ASD*(&(()@#DS.doesnotexits"

logger = logging.getLogger("DevLogger")

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
        # that database connects successfully with no error\warnings
        # using correct database.
        database_class = ping_bot_database_manager(DATABASE_DUMP)

    def test_database_ioctl_add_user(self) -> None:
        # Call ping_bot_database_manager::add_user() to
        # verify that database process adding successfully
        database_class = ping_bot_database_manager(DATABASE_DUMP)
        database_class.add_user("1288")

    def test_database_ioctl_add_ip(self) -> None:
        # Call ping_bot_database_manager::add_user() to
        # verify that database process adding successfully
        database_class = ping_bot_database_manager(DATABASE_DUMP)
        database_class.add_user("1288")
        database_class.add_ip("1288", "128.168.0.0.1")

    @pytest.fixture(autouse=True)
    def test_database_ioctl_add_ip_distinct_check(self, caplog) -> None:
        # Call ping_bot_database_manager::add_user() to
        # verify that database process adding successfully
        # ip already exists in the database
        database_class = ping_bot_database_manager(DATABASE_DUMP)

        with caplog.at_level(logging.WARNING):
            database_class.remove_ip("1288", "128.168.0.0.1")
            database_class.add_ip("1288", "128.168.0.0.1", exist_ok=True)
            database_class.add_ip("1288", "128.168.0.0.1", exist_ok=False)
            assert log_meta["database-non-distinct-add"].format("data-chain", "ip-address", "1288") in caplog.text

        with caplog.at_level(logging.WARNING):
            database_class.remove_ip("1288", "128.168.0.0.1")
            database_class.add_ip("1288", "128.168.0.0.1", exist_ok=False)
            database_class.add_ip("1288", "128.168.0.0.1", exist_ok=False)
            assert log_meta["database-non-distinct-add"].format("data-chain", "ip-address", "1288") in caplog.text
