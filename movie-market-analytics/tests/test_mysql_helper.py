from src.db.mysql_helper import MySQLHelper


def test_mysql_helper_initialization():
    db = MySQLHelper()
    assert db.host is not None
    assert db.port == 3306 or isinstance(db.port, int)
