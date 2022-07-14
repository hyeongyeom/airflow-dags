# test파일 사용X

from datetime import timedelta
from textwrap import dedent

import pendulum
from datetime import datetime, timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from airflow.models import Variable

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization


kst = pendulum.timezone("Asia/Seoul")
AIRFLOW_ENV = Variable.get("AIRFLOW_ENV")
try:
    email_for_report = Variable.get(
        key="email_for_report", deserialize_json=True)
except KeyError:
    if AIRFLOW_ENV == "DEVELOPMENT":
        email_for_report = ['example1@gmail.com']
    elif AIRFLOW_ENV == "STAGING":
        email_for_report = ['example2@gmail.com']
    elif AIRFLOW_ENV == "PRODUCTION":
        email_for_report = ['example3@gmail.com']
    else:
        email_for_report = ['example4@gmail.com']

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': email_for_report,
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success',
}
with DAG(
    'err_test',
    default_args=default_args,
    schedule_interval="3 18 * * *",
    catchup=False,
    start_date=datetime(2022, 7, 10, tzinfo=kst),
) as dag:

    err_test = BashOperator(
        task_id='err_test',
        bash_command='{{ var.json.ssh_secret.desktop}} "source Desktop/Environments/TestServer_env/bin/activate && cd ./Desktop/testServer && python3 test.py"',

    )

    [err_test]
