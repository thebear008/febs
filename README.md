# FEBS

**F**ile **E**xplorer for **B**ucket **S**3 is a quick UI in Python3 to deal with S3 Buckets.

## Requirements

UI library is `tkinter`. It is auto setup with your python3. Nothing to do.

About the other requirements, since we qre deqling with S3 Bucket we need `boto3`. So please execute

```
pip install -r requirements.txt
```

## Configuration

Credentials and URL are mandatory to connect your S3 Bucket.
We decided to trust a JSON file.

```
{
    "endpoint_url": "http://localhost:9000",
    "aws_access_key_id": "XXX",
    "aws_secret_access_key": "YYY",
    "signature_version": "s3v4",
    "region_name": "us-east-1",
    "bucket_name": "my_bucket"
}
```

## Execute

### S3 bucket

To test we can use https://www.minio.io/, it is a great object storage server.
For a linux 64 bits compute, you can retrieve the binary file with

```
wget https://dl.minio.io/server/minio/release/linux-amd64/minio
```

Then create a folder to store your objectx and execute.

```
mkdir /data
chmod +x minio
./minio server /data
```

It will provide you all details you need to use your new S3 server.

```
Endpoint:  http://192.168.1.165:9000  http://172.17.0.1:9000  http://192.168.122.1:9000  http://127.0.0.1:9000
AccessKey: 2IQYX9R1OCHK70Q10BB0
SecretKey: JyXD9I36W8OIRlZtZs0VzUycl1o+3xVbVYUC1laq

Browser Access:
   http://192.168.1.165:9000  http://172.17.0.1:9000  http://192.168.122.1:9000  http://127.0.0.1:9000

Command-line Access: https://docs.minio.io/docs/minio-client-quickstart-guide
   $ mc config host add myminio http://192.168.1.165:9000 2IQYX9R1OCHK70Q10BB0 JyXD9I36W8OIRlZtZs0VzUycl1o+3xVbVYUC1laq

Object API (Amazon S3 compatible):
   Go:         https://docs.minio.io/docs/golang-client-quickstart-guide
   Java:       https://docs.minio.io/docs/java-client-quickstart-guide
   Python:     https://docs.minio.io/docs/python-client-quickstart-guide
   JavaScript: https://docs.minio.io/docs/javascript-client-quickstart-guide
   .NET:       https://docs.minio.io/docs/dotnet-client-quickstart-guide
```

### Run python

Run this command :

```
python3 run.py
# custom HOME for left column
HOME=/tmp python3 run.py
```

## Features

1. Double click on left column will upload the file to S3 bucket.
2. Double click on right column will download from S3 bucket.

## Tests

Just execute

```
pytest --cov=core --cov=models --cov=views tests/
======================================================================================== test session starts =========================================================================================
platform linux -- Python 3.6.6, pytest-4.4.1, py-1.8.0, pluggy-0.9.0
rootdir: /home/lonclegr/workspace/github/febs
plugins: cov-2.6.1
collected 1 item

tests/test_models.py .                                                                                                                                                                         [100%]

----------- coverage: platform linux, python 3.6.6-final-0 -----------
Name                 Stmts   Miss  Cover
----------------------------------------
core/__init__.py         0      0   100%
core/exceptions.py       7      2    71%
core/logger.py          16      2    88%
models/__init__.py       0      0   100%
models/models.py        82     59    28%
views/__init__.py        0      0   100%
views/views.py          84     84     0%
----------------------------------------
TOTAL                  189    147    22%


====================================================================================== 1 passed in 0.32 seconds ======================================================================================
coverage report -m
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
core/__init__.py         0      0   100%
core/exceptions.py       7      2    71%   8-10
core/logger.py          16      2    88%   20, 26
models/__init__.py       0      0   100%
models/models.py        82     59    28%   24, 31-44, 48-66, 70-79, 86-87, 91-95, 99-100, 105-111, 116-118, 126-156
views/__init__.py        0      0   100%
views/views.py          84     84     0%   2-156
--------------------------------------------------
TOTAL                  189    147    22%
```

## Model Features

1. Copy bucket

Example

```
# coding: utf-8

from models.models import MainModel
videos = MainModel()
videos.get_config('config.json')
toto = MainModel()
toto.get_config('config2.json')
videos.copy_bucket_to(toto)
videos.copy_bucket_to(toto, 1 * 1024 * 1024)  # copy only files under 1MB
```
