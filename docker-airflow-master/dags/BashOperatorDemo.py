from datetime import datetime
from airflow.models import DAG,Variable
from airflow.operators.bash_operator import BashOperator 

default_args = {
    'owner':'quynhnhitran',
    'start_date':datetime(2024,11,13)
}

with DAG(
    dag_id = "BashOperatorDemo1",
    default_args=default_args,
    schedule_interval=None) as dag:

    start_dag=BashOperator(
        task_id="start_dag",
        bash_command="date"
    )

    start_dag