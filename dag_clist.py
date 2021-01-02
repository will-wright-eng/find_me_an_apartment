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
clist.doc_md = """\
#### Task Documentation
The meat and potatoes of this dag, clist uses a wraper and pandas
to collect and manipulate craigslist housing listings, then load 
the csv to an S3 bucket. Ideally the format would be parquet but in 
its raw form the shema isn't compatible with parquet data types. 

#### Note
The `start_dag` and `email` nodes are placeholders, with 
minimal functionality, for additional opperations for that 
dag as well as a template for other projects.
"""

start_dag >> clist >> email
