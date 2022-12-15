""""Скрипт можно запустить и наблюдать как данные добавляются в кликхаус."""
import csv
from dataclasses import dataclass
from time import sleep

from clickhouse_driver import Client
from config import logger, settings


@dataclass
class ActualData:
    shard_1: int
    shard_2: int
    shard_3: int
    all_data: int


def get_data(client_1: Client, client_2: Client, client_3: Client
             ) -> ActualData:
    return ActualData(
        all_data=client_1.execute('SELECT COUNT(*) FROM default.test')[0][0],
        shard_1=client_1.execute('SELECT COUNT(*) FROM shard.test')[0][0],
        shard_2=client_2.execute('SELECT COUNT(*) FROM shard.test')[0][0],
        shard_3=client_3.execute('SELECT COUNT(*) FROM shard.test')[0][0],
    )


def main():
    client_1 = Client(host=settings.ch_host, port=settings.ch_port_1)
    client_2 = Client(host=settings.ch_host, port=settings.ch_port_2)
    client_3 = Client(host=settings.ch_host, port=settings.ch_port_3)
    last_all_data = 0
    log_file = open('./lods.csv', 'a', newline='')
    writer = csv.writer(log_file)
    try:
        while last_all_data < settings.cheker_count:
            actual_data = get_data(client_1, client_2, client_3)
            how_much_added = actual_data.all_data - last_all_data
            last_all_data = actual_data.all_data
            writer.writerow([
                actual_data.shard_1,
                actual_data.shard_2,
                actual_data.shard_3,
                actual_data.all_data,
                f'+{how_much_added}',
            ])
            logger.info(f'{actual_data.shard_1} | '
                        f'{actual_data.shard_2} | '
                        f'{actual_data.shard_3} || '
                        f'{actual_data.all_data} '
                        f'+{how_much_added}'
                        )

            sleep(settings.cheker_interval)
    except KeyboardInterrupt:
        logger.info('exit')
    finally:
        log_file.close()


if __name__ == '__main__':
    main()
