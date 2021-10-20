import datetime
import logging

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.dataflow_operator import DataFlowJavaOperator

SCHEDULE = '0 8 * * *'
MODULE_NAME = 'composer-dataflow-test'
GCP_PROJECT = 'project-test'
date_now = datetime.datetime.now()



default_args = {
    'owner': 'airflow',
    'start_date': date_now,
    'concurrency': 1,
    'dataflow_default_options': {
        'project': GCP_PROJECT,        
        'region': 'us-east1',
        'workerZone': 'northamerica-northeast1-a',
        'tempLocation': 'gs://dataflow-bucket/temp',
        'stagingLocation': 'gs://dataflow-bucket/staging',
        'usePublicIps': 'false',
        'subnetwork': 'https://www.googleapis.com/compute/v1/projects/test/regions/northamerica-northeast1/subnetworks/can-sre-tools-npe-initial-0',
        'serviceAccount': '',
        'workerMachineType': 'n1-standard-1',
        'autoscalingAlgorithm': 'NONE',
        'defaultWorkerLogLevel': 'ERROR'
    }
}

migrationPipelineOptions = {
    'sequence': '1',
    'predecessor': '0',
    'isActive': True,
    'batch': {
        'executor': 'composer-test',
        'parameters': [
            {
                  'key': 'jar',
                  'value': 'gs://dataflow-bucket/jars/migration-dataflow-1.0.1-bundled.jar'
               }, 
               {
                'key': 'inputFileFolder',
                'value': 'gs://dataflow-bucket/input/abc.txt'
            },
            {
                'key': 'output',
                'value': 'gs://dataflow-bucket/output'
            },
            
               {
                'key': 'maxNumWorkers',
                'value': '10'
            },
            {
                'key': 'numWorkers',
                'value': '10'
            }
        ]
    }
}
with DAG(MODULE_NAME,
         catchup=False,
         default_args=default_args,
         schedule_interval=None,
         ) as dag:
    opr_start = BashOperator(task_id='start',
                             bash_command=" echo 'Start!' "
                             )

    migration_parameters = migrationPipelineOptions.get("batch").get("parameters")
    migration_new_params = {}
    for param in migration_parameters:
        migration_new_params[param["key"]] = param["value"]

    migration_jar = migration_new_params["jar"]
    migration_new_params.pop("jar")
    migration_task = DataFlowJavaOperator(
        task_id=str(MODULE_NAME + '-Update').lower(),
        jar=migration_jar,
        retries=1,
        options=migration_new_params
    )    

    opr_end = BashOperator(task_id='end',
                           bash_command=" echo 'End!' "
                           )

opr_start >> migration_task >> opr_end
