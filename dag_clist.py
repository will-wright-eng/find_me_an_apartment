'''py file docstring
Author: William Wright
'''

import datetime 

from airflow import DAG

from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'willcasswrig',
    'depends_on_past': False,
    'email': ['william.cass.wright@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': datetime.timedelta(minutes=1),
    'start_date':datetime.datetime(2020, 12, 1, 0, 0),
}

dag = DAG('dag_clist',
          default_args=args,
          description='grabs craigslist rental listings',
          schedule_interval=datetime.timedelta(0.5),
          catchup=False)

start_dag = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)
clist = BashOperator(
    task_id='clist',
    bash_command='''python /home/pi/src/main_clist.py''',
    dag=dag,
)
# template f'''email body
# execution date:\t\t{{ ds }}
# previous execution date:\t\t{{ prev_ds }}
# next execution date:\t\t{{ next_ds }}'''

email = BashOperator(
    task_id='email',
    bash_command='''python /home/pi/src/main_email.py''',
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
