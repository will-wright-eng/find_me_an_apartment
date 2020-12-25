from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization

default_args = {
    'owner': 'willcasswrig',
    'depends_on_past': False,
    'email': ['william.cass.wright@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'dag_clist',
    default_args=default_args,
    description='grabs craigslist rental listings',
    schedule_interval='0 */12 * * *',
    start_date=days_ago(1)
)

start_dag = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)
clist = BashOperator(
    task_id='clist',
    bash_command='''python /home/pi/airflow/dags/src/main_clist.py''',
    dag=dag,
)
email = BashOperator(
    task_id='email',
    bash_command='''echo "sending email"
        python /home/pi/airflow/dags/src/main_email.py''',
    dag=dag,
)

dag.doc_md = __doc__
start_dag.doc_md = """\
#### Task Documentation
You can document your task using the attributes `doc_md` (markdown),
`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
rendered in the UI's Task Instance Details page.
![img]()
"""

start_dag >> clist >> email