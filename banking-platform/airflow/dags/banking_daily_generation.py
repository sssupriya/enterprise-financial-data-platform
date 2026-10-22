from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

with DAG(
    dag_id="banking_daily_generation",
    description="Generate synthetic banking transactions",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["banking", "data-engineering"],
) as dag:

    generate_banking_transactions = BashOperator(
        task_id="generate_banking_transactions",
        bash_command=(
            "python /opt/banking-platform/run_generation.py "
            "--date 2026-10-15"
        ),
        cwd="/opt/banking-platform",
        retries=0,
    )