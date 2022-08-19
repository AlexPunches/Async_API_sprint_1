import os
import psycopg2
import sqlite3
import sys
from contextlib import contextmanager
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(
    __file__)))
sys.path.append(BASE_DIR)

from sqlite_to_postgres import logger, settings
from sqlite_to_postgres.loaders import (ExtractDataError, ForeignKeyError,
                                        PostgresSaver, SQLiteExtractor)


@contextmanager
def conn_context_sqlite3(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def load_from_sqlite(
          sl_connect: sqlite3.Connection,
          pg_connect: _connection,
) -> None:
    """Основной метод загрузки данных из SQLite в Postgres."""
    postgres_saver = PostgresSaver(pg_connect)
    sqlite_extractor = SQLiteExtractor(sl_connect)

    data_tables = sqlite_extractor.get_tables()
    while len(data_tables) > 0:
        table = data_tables.pop(0)
        sqlite_extractor.last_id = None
        count = 0
        try:
            data_for_save = sqlite_extractor.extract_data(table=table)
            for data in data_for_save:
                postgres_saver.save_data(data, table)
                count += len(data)

        except ForeignKeyError as e:
            logger.warning(e)
            data_tables.append(table)
        except ExtractDataError as e:
            logger.warning(e)
        else:
            logger.info("Table <%s> finished. "
                        "Processed %s rows.", table, count)
    # Обнулим вотчер,
    # чтобы следующая синхронизация из PG в ES стала полной - мало ли чего.
    postgres_saver.clear_watcher()


if __name__ == '__main__':
    with (
        conn_context_sqlite3(settings.sqlite3_path) as sqlite_conn,
        psycopg2.connect(**settings.dsl, cursor_factory=DictCursor) as pg_conn
    ):
        load_from_sqlite(sqlite_conn, pg_conn)
