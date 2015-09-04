import subprocess
import logging
import os
import signal


logger = logging.getLogger(__name__)


def _rds_cmd_options(config):
    return [
        '--region',
        config.region,
        '--access-key-id',
        config.access_key,
        '--secret-key',
        config.secret_key,
    ]


class RDSLogDownload:
    def __init__(self, config, local_file):
        self._config = config
        self._local_file = local_file

    def download(self):
        cmd = [
            'rds',
            'rds-download-db-logfile',
            self._config.db_identifier,
            '--log-file-name',
            self._local_file.filename,
        ] + _rds_cmd_options(self._config)

        with self._local_file.open_for_write() as f:
            self._proc = subprocess.Popen(cmd, stdout=f)
            return_code = self._proc.wait()

            if return_code == 0:
                logger.info('Download success')
            else:
                logger.warning('Download failed. rds-download-db-logfile exit code {}'.format(return_code))

    def __repr__(self):
        return '<RDSLogDownLoad "{}">'.format(self._local_file.filename)


class RDSLogStream:
    def __init__(self, config, local_file):
        self._config = config
        self._local_file = local_file

    def __eq__(self, other):
        return hasattr(other, '_local_file') and other._local_file.filename == self._local_file.filename

    def start_stream(self):
        cmd = [
            'rds',
            'rds-watch-db-logfile',
            self._config.db_identifier,
            '--log-file-name',
            self._local_file.filename,
        ] + _rds_cmd_options(self._config)

        logger.info('Starting stream of {}'.format(self._local_file.filename))

        self._out_file = self._local_file.open_for_write()
        self._proc = subprocess.Popen(cmd,
                                      stdout=self._out_file,
                                      start_new_session=True)

    def stop_stream(self):
        logger.info('Stopping stream of {}'.format(self._local_file.filename))
        os.killpg(self._proc.pid, signal.SIGKILL)
        self._out_file.close()

    def __repr__(self):
        return '<RDSLogStream "{}">'.format(self._local_file.filename)
