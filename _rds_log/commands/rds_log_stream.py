import sys
import click
import pathlib
import time
import operator
import logging

from collections import namedtuple

import boto3

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)


from ..rds import RDSLogDownload, RDSLogStream
from ..local_log import LocalLogFile


def _get_log_files(config, db_identifier, root_directory):
    result = config.rds_client.describe_db_log_files(DBInstanceIdentifier=db_identifier)

    rds_logs = sorted((rds_log for rds_log in result['DescribeDBLogFiles']),
                      key=operator.itemgetter('LogFileName'))

    def downloads():
        for rds_log in rds_logs[:-1]:
            local_file = LocalLogFile(root_directory, rds_log['LogFileName'])

            if local_file.size != rds_log['Size']:
                yield RDSLogDownload(config, local_file)

    return (list(downloads()), RDSLogStream(config, LocalLogFile(root_directory, rds_logs[-1]['LogFileName'])))


_Config = namedtuple('Config', ['access_key', 'secret_key', 'region', 'db_identifier', 'rds_client'])


@click.command()
@click.argument('db_identifier')
@click.argument('destination_directory', type=click.Path(file_okay=False, dir_okay=True, exists=True))
def main(db_identifier, destination_directory):
    destination_directory = pathlib.Path(destination_directory)
    current_stream = None

    boto_session = boto3.session.Session()

    config = _Config(
        access_key=boto_session._session.get_credentials().access_key,
        secret_key=boto_session._session.get_credentials().secret_key,
        region=boto_session._session.get_config_variable('region'),
        db_identifier=db_identifier,
        rds_client=boto_session.client('rds'),
    )

    try:

        while True:
            downloads, stream = _get_log_files(config, db_identifier, destination_directory)
            new_stream = stream != current_stream

            if new_stream:
                if current_stream:
                    current_stream.stop_stream()

                for download in downloads:
                    logger.info('Downloading full copy of {}'.format(download))
                    download.download()

                current_stream = stream
                current_stream.start_stream()

            else:
                logger.info('Check completed, no new file found')

            time.sleep(60)

    finally:
        if current_stream:
            current_stream.stop_stream()
