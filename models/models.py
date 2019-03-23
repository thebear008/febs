""" model for FEBS """

import json
import boto3
from botocore.client import Config
from core.exceptions import ConfigNotProvided


class MainModel():
    """ class to manage the main model """

    def __init__(self):
        """ constructor """
        self._config = None
        self._bucket = None

    def get_config(self, config_file=False):
        """ get config and store it """
        if not self._config:
            if not config_file:
                raise ConfigNotProvided(
                    "Unable to configure main_model without config_file"
                )
            try:
                with open(config_file) as my_f:
                    self._config = json.load(my_f)
            except Exception:
                print('ERROR TODO')

        return self._config

    def get_bucket(self, config=False):
        """ get Bucket object """
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

        return self._bucket

    def upload(self, local_path, remote_filename):
        """ upload local file to remote server """
        self.get_bucket().upload_file(local_path, remote_filename)

    def download(self, remote_filename, local_path):
        """ download remote file to local """
        self.get_bucket().download_file(remote_filename, local_path)

    def list_files(self):
        """ get all files from bucket """
        return self.get_bucket().objects.all()
