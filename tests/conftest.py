"""Test settings: never touch a real S3 bucket or push to a real Git remote.

These are set before the app is imported. .env is loaded by the app but does not override
variables that are already set, so these win.
"""
import os

os.environ["S3_BUCKET_NAME"] = ""
os.environ["AWS_S3_BUCKET"] = ""
os.environ["CHATSAVE_GIT_URL"] = ""
os.environ["CHATSAVE_CAPTURE"] = "0"
os.environ["CHATSAVE_DATABASE_URL"] = ""  # tests use SQLite; PostgreSQL is tested separately
