from datetime import datetime
from airflow.models import DAG,Variable
from airflow.operators.python_operator import PythonOperator 
from bots.Python_Helper import call


default_args = {

    'owner':'quynhnhitran',
    'start_date':datetime(2024,11,13)
}

with DAG(
    dag_id='PythonOperatorDemo1',
    default_args=default_args,
    schedule_interval=None) as dag:

    start_dag = PythonOperator(
        task_id = 'start_dag',
        python_callable=call
    )

    start_dag