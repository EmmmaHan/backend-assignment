import os


def get_db_uri():
    return "{}://{}:{}@{}:{}/{}".format(
    os.getenv("db_protocol","mysql+asyncmy"),
    os.getenv("db_user","root"),
    os.getenv("db_password","ffbb"),
    os.getenv("db_host","localhost"),
    os.getenv("db_port","3306"),
    os.getenv("db_name","bering_assignment"),
)
