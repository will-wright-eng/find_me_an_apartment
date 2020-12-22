from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
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
    # 'trigger_rule': 'all_success'
}

dag = DAG(
    'dag_clist',
    default_args=default_args,
    description='dag for executing main.py which grabs craigslist \
        rental listings',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1)
)

start_dag = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)
clist = BashOperator(
    task_id='clist',
    bash_command='''echo "collect craigslist listings"
        python main_clist.py''',
    dag=dag,
)
email = BashOperator(
    task_id='print_date',
    bash_command='''echo "sending email"
        python main_email.py''',
    dag=dag,
)

dag.doc_md = __doc__
task1.doc_md = """\
#### Task Documentation
You can document your task using the attributes `doc_md` (markdown),
`doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
rendered in the UI's Task Instance Details page.
![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
"""

# t2 = BashOperator(
#     task_id='sleep',
#     depends_on_past=False,
#     bash_command='sleep 5',
#     retries=3,
#     dag=dag,
# )


# templated_command = """
# {% for i in range(5) %}
#     echo "{{ ds }}"
#     echo "{{ macros.ds_add(ds, 7)}}"
#     echo "{{ params.my_param }}"
# {% endfor %}
# """

# t3 = BashOperator(
#     task_id='templated',
#     depends_on_past=False,
#     bash_command=templated_command,
#     params={'my_param': 'Parameter I passed in'},
#     dag=dag,
# )

# t1 >> [t2, t3]

start_dag >> clist >> email