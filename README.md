
# Cloud Function to trigger dataflow

# Requirement
java
maven

#  Building the entire project

mvn clean compile

##  creating template file

  mvn compile exec:java -Dexec.mainClass=com.example.WordCount \
  -Dexec.cleanupDaemonThreads=false \
  -Dexec.args="--project=test-cloud-project \
  --stagingLocation=gs://dataflow-bucket/temptest/staging/  \
  --gcpTempLocation=gs://dataflow-bucket/temptest/temptest/temp/ \
  --tempLocation=gs://dataflow-bucket/temptest/temptest/temp  \
  --templateLocation=gs://dataflow-bucket/temptest/temptest/templates/wordcountTemplate.json \
  --runner=DataflowRunner \
  --region=northamerica-northeast1"
  # OR
  
  java -jar target/cloud-function-1.0.2-SNAPSHOT-bundled.jar   
  --project=cloud-migrationtest12  
  --serviceAccount=sa@cloud-migrationtest12.iam.gserviceaccount.com
  --tempLocation=gs://test-bucket/cloudfntemp/ 
  --stagingLocation=gs://test-bucket/test/cloudfnstaging 
  --gcpTempLocation=gs://test-bucket/cloudfntemp/ 
  --templateLocation=gs://test-bucket/test/template/wordcountTemplate 
  --usePublicIps=false 
  --region=northamerica-northeast1 
  --zone=northamerica-northeast1-a
  --subnetwork=https://www.googleapis.com/compute/v1/projects/project1/regions/us-east1/subnetworks/test-cloud-project
  
  


# Executing template file

gcloud dataflow jobs run test-df-template \
--gcs-location=gs://dataflow-bucket/temptest/templates/wordcountTemplate \
--region=northamerica-northeast1  \
--worker-zone=northamerica-northeast1-a \
--service-account-email=sa@cloud-migrationtest12.iam.gserviceaccount.com \
--parameters 
      inputFile=gs://dataflow-bucket/temptest/abc.txt,output=gs://dataflow-bucket/temptest/output 
      
      
      





