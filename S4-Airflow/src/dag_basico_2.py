from airflow.operators.python import PythonOperator
import random

def generar_numero():
    numero = random.randint(1, 100)
    print(f"Número generado: {numero}")

tarea_python = PythonOperator(
    task_id='generar_numero',
    python_callable=generar_numero,
    dag=dag
)

tarea >> tarea_python