from airflow import DAG
from airflow.operators.python_operator import PythonOperator 
from airflow.utils.dates import days_ago
# from airflow.operators.email import EmailOperator
from airflow.exceptions import AirflowException

import bots.get_category  
import bots.get_product_info  
import bots.combine_products  

def run_get_category():
    get_category.main()

def run_get_product_info():
    get_product_info.main()

def run_combine_products():
    combine_products.main()

# gửi email nếu có lỗi
# def send_failure_email(context):
#     subject = f"Airflow Task {context['task_instance'].task_id} Failed"
#     body = f"""
#     Task {context['task_instance'].task_id} failed in DAG {context['dag'].dag_id}.
#     Error: {context['exception']}
#     """
#     email_operator = EmailOperator(
#         task_id='send_failure_email',
#         to='quynhnhitran.info@gmail.com',
#         subject=subject,
#         html_content=body
#     )
#     email_operator.execute(context)

default_args = {
    'owner': 'quynhnhitran',
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=10),
    'on_failure_callback': send_failure_email,
}

with DAG(
    'daily_data_collection_pipeline',
    default_args=default_args,
    description='DAG for data collection pipeline',
    schedule_interval='0 7 * * *',
    catchup=False,
) as dag:

    # Tạo các tác vụ
    task_get_category = PythonOperator(
        task_id='get_category',
        python_callable=run_get_category,
    )

    task_get_product_info = PythonOperator(
        task_id='get_product_info',
        python_callable=run_get_product_info,
    )

    task_combine_products = PythonOperator(
        task_id='combine_products',
        python_callable=run_combine_products,
    )

    # # Gửi email báo cáo khi hoàn thành
    # send_completion_email = EmailOperator(
    #     task_id='send_completion_email',
    #     to='quynhnhitran.info@gmail.com',
    #     subject='DAG daily_data_collection_pipeline Completed',
    #     html_content='<p>The daily_data_collection_pipeline DAG has completed successfully.</p>',
    # )

    # Thiết lập thứ tự chạy của DAG
    task_get_category >> task_get_product_info >> task_combine_products 
    # task_get_category >> task_get_product_info >> task_combine_products >> send_completion_email
