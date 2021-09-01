# Cray STS Service

For generating short lived Ceph S3 credentials


## Build and testing the container

```
cat <<EOF > conf/creds
access_key: foo
secret_key: bar
EOF
docker build . --tag cray/sts && docker run -p 8000:8000 -v $PWD/conf:/conf cray/sts
```

## Testing outside the container (ensure that endpoint_url is resolvable where we are running)

```
cat <<EOF > conf/creds/access_key
foo
EOF

cat <<EOF > conf/creds/secret_key
bar
EOF

cat <<EOF > conf/rados_conf
endpoint_url: http://rgw.local:8080
arn: arn:aws:iam:::user/ARS
EOF

pip install -e .
pip install gunicorn nox

nox # Run lint, tests, and code coverage

gunicorn sts.sts:conn_app # run app
```

## Using the token

```
$ python3
Python 3.7.4 (default, Jul  9 2019, 18:13:23)
[Clang 10.0.1 (clang-1001.0.46.4)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import boto3
>>> import requests
>>> r = requests.put(http://127.0.0.1:8000/token)
>>> creds = r.json()
>>> s3client = boto3.client('s3',
...   aws_access_key_id = creds['Credentials']['AccessKeyId'],
...   aws_secret_access_key = creds['Credentials']['SecretAccessKey'],
...   aws_session_token = creds['Credentials']['SessionToken'],
...   endpoint_url="http://10.248.2.44:8080",
...   region_name='')
>>> buckets = s3client.list_buckets()

```


## Updating requirements.txt

Make sure that `requirements-direct.txt` is up to date with the packages that
are directly used by STS (i.e., they are imported by the STS code).

Install `requirements-direct.txt` in a venv and use `pip freeze` to get the
new contents for requirements.txt:

```
python3 -m venv venv1
. venv1/bin/activate
pip install -r requirements-direct.txt
pip freeze
```

Also update `Dockerfile` with the pinned version of `gunicorn`.
