""" model for FEBS """

import os
import json
import boto3
from botocore.client import Config
from core.exceptions import ConfigNotProvided, BadJsonConfig
from core.logger import logger


class MainModel():
    """ class to manage the main model """

    def __init__(self):
        """ constructor """
        logger.info('MainModel constructor')
        self._config = None
        self._bucket = None
        self._remote_prefix = ''
        self._remote_level = 0

    def __str__(self):
        """ return string to show object description """
        return "MainModel (bucket: {0}, prefix: {1}, level: {2})".format(
            self.get_config()['bucket_name'],
            self._remote_prefix,
            self._remote_level)

    def get_config(self, config_file=False):
        """ get config and store it """
        logger.info('get_config called')
        if not self._config:
            if not config_file:
                raise ConfigNotProvided(
                    "Unable to configure main_model without config_file"
                )
            try:
                with open(config_file) as my_f:
                    self._config = json.load(my_f)
                    logger.info(f'Loaded successfully {config_file}')
            except Exception:
                raise BadJsonConfig(f"File {config_file} is wrong")

        return self._config

    def get_bucket(self, config=False):
        """ get Bucket object """
        logger.info('get_bucket called')
        if not self._bucket:
            if not config:
                config = self.get_config()
            my_s3 = boto3.resource(
                's3',
                endpoint_url=config['endpoint_url'],
                aws_access_key_id=config['aws_access_key_id'],
                aws_secret_access_key=config['aws_secret_access_key'],
                config=Config(
                    signature_version=config['signature_version']
                ),
                region_name=config['region_name']
            )

            self._bucket = my_s3.Bucket(config['bucket_name'])
            logger.info(f'Loaded successfully bucket {config["bucket_name"]}')

        return self._bucket

    def upload(self, local_path, remote_filename):
        """ upload local file to remote server """
        if self._remote_prefix and not self._remote_prefix.endswith('/'):
            self._remote_prefix += '/'

        if remote_filename.startswith('/'):
            remote_filename = "/".join(remote_filename.split('/')[1:])

        logger.info(
            f"Uploading {local_path} to {self._remote_prefix}{remote_filename}"
        )
        self.get_bucket().upload_file(
            local_path,
            self._remote_prefix + remote_filename
        )

    def download(self, remote_filename, local_path):
        """ download remote file to local """
        logger.info(f'Downloading {remote_filename} to {local_path}')
        self.get_bucket().download_file(remote_filename, local_path)

    def list_files(self):
        """ get all files from bucket """
        if self._remote_level == 0:
            logger.info(f'Listing all files')
            return self.get_bucket().objects.all()
        logger.info(f'Fitlering files with prefix {self._remote_prefix}')
        return self.get_bucket().objects.filter(Prefix=self._remote_prefix)

    def empty_bucket(self):
        """ remove all objects from bucket """
        logger.info(f'Removing all objects from bucket')
        self.get_bucket().objects.delete()

    def go_up(self):
        """ go up into remote tree """

        logger.info('Going up into remote tree')
        self._remote_prefix = "/".join(
            self._remote_prefix.split('/')[:-2]
        ) + "/"
        self._remote_level -= 1
        if self._remote_level == 0:
            self._remote_prefix = ''

    def go_to(self, prefix):
        """ go to remote tree prefix """

        logger.info(f'Going to remote {prefix} tree')
        self._remote_level += 1
        self._remote_prefix += prefix.split("/")[0] + "/"

    def copy_bucket_to(self, other_model):
        """
            we want to copy all objects from this bucket to the other one
        """

        logger.info(f'Copying objects from {self} to {other_model}')
        if not isinstance(other_model, MainModel):
            raise TypeError(
                f"Expecting a MainModel object not a {type(other_model)} "
            )

        # get only discrepancies
        logger.info('Computing discrepancies')
        other_model_objects = [y.key for y in other_model.list_files()]
        discrepancies = [
            x.key for x in self.list_files()
            if x.key not in other_model_objects
        ]
        logger.info(f'Got {len(discrepancies)} discrepancies')

        for my_key in discrepancies:
            path, filename = os.path.split(my_key)

            self.download(my_key, '/tmp/' + filename)
            other_model.upload('/tmp/' + filename, path + '/' + filename)

            logger.info(f'Removing from local File system /tmp/{filename}')
            os.remove('/tmp/' + filename)
