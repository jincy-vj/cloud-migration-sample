
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


# Executing template file

gcloud dataflow jobs run test-df-template \
--gcs-location=gs://dataflow-bucket/temptest/templates/wordcountTemplate.json \
--region=northamerica-northeast1  \
--zone=northamerica-northeast1-a \
--parameters 
      inputFile=gs://dataflow-bucket/temptest/abc.txt,output=gs://dataflow-bucket/temptest/output 
      





