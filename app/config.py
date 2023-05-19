import os

def get_db_uri():
    return "{}://{}:{}@{}:{}/{}".format(
    os.getenv("db_protocol","mysql+mysqlconnector"),
    os.getenv("db_user","root"),
    os.getenv("db_password","ffbb"),
    os.getenv("db_host","localhost"),
    os.getenv("db_port","3306"),
    os.getenv("db_name","bering_assignment"),
)


def get_test_db_uri():
    return "{}://{}:{}@{}:{}/{}".format(
    os.getenv("db_protocol","mysql+asyncmy"),
    os.getenv("db_user","root"),
    os.getenv("db_password","ffbb"),
    os.getenv("db_host","localhost"),
    os.getenv("db_port","3306"),
    os.getenv("db_name","bering_assignment_test"),
)

def get_sys_db_uri():
    if os.getenv("env","") == "test":
        return get_test_db_uri()
    else:
        return get_db_uri()

