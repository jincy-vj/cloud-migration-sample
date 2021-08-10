import datetime
import logging

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.dataflow_operator import DataFlowJavaOperator

SCHEDULE = '0 8 * * *'
MODULE_NAME = 'gfs-canada-test'
GCP_PROJECT = 'can-sre-tools-npe-c3ee'
YESTERDAY = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())

date_now = datetime.datetime.now()
CREATED_DATE = date_now.strftime('%Y-%m-%dT%H:%M:%S')
delete_date_now = date_now - datetime.timedelta(days=1)
DELETE_DATE = delete_date_now.strftime('%Y-%m-%d')


default_args = {
    'owner': 'airflow',
    'start_date': YESTERDAY,
    'concurrency': 1,
    'dataflow_default_options': {
        'project': GCP_PROJECT,        
        'region': 'us-east1',
        'workerZone': 'northamerica-northeast1-a',
        'tempLocation': 'gs://can-sre-tools-npe-gfs-canada/dataflowtemp',
        'stagingLocation': 'gs://can-sre-tools-npe-gfs-canada/can-sre-tools-npe-billingservice-dataflow-jars',
        'usePublicIps': 'false',
        'subnetwork': 'https://www.googleapis.com/compute/v1/projects/efx-gcp-can-svpc-npe-21fe/regions/northamerica-northeast1/subnetworks/can-sre-tools-npe-initial-0',
        'serviceAccount': 'nscpm-gfs-canada-it-cistocdm@can-sre-tools-npe-c3ee.iam.gserviceaccount.com',
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
                  'value': 'gs://dataflow-bucket/jars/migration-dataflow-17.0.1.1-bundled.jar'
               }, 
               {
                'key': 'inputFileFolder',
                'value': 'gs://dataflow-bucket/input/abc.txt'
            },
            {
                'key': 'GCSProjectId',
                'value': 'project-test'
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
         schedule_interval=SCHEDULE,
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
