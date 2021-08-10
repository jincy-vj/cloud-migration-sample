
package com.example;

import com.example.Example.GCSEvent;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.HttpRequestInitializer;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.services.dataflow.Dataflow;
import com.google.api.services.dataflow.model.LaunchTemplateParameters;
import com.google.api.services.dataflow.model.RuntimeEnvironment;
import com.google.auth.http.HttpCredentialsAdapter;
import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.functions.BackgroundFunction;
import com.google.cloud.functions.Context;

import java.io.IOException;
import java.security.GeneralSecurityException;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

public class Example implements BackgroundFunction<GCSEvent> {
    private static final Logger logger = Logger.getLogger(Example.class.getName());

    @Override
    public void accept(GCSEvent event, Context context) throws IOException, GeneralSecurityException {
        logger.info("Event: " + context.eventId());
        logger.info("Event Type: " + context.eventType());


        HttpTransport httpTransport = GoogleNetHttpTransport.newTrustedTransport();
        JsonFactory jsonFactory = JacksonFactory.getDefaultInstance();

        GoogleCredentials credentials = GoogleCredentials.getApplicationDefault();
        HttpRequestInitializer requestInitializer = new HttpCredentialsAdapter(credentials);


        Dataflow dataflowService = new Dataflow.Builder(httpTransport, jsonFactory, requestInitializer)
                .setApplicationName("Google Dataflow function Demo")
                .build();

        logger.info("dataflowService: " + dataflowService);
        String projectId = "can-sre-tools-npe-c3ee";


        RuntimeEnvironment runtimeEnvironment = new RuntimeEnvironment();
        runtimeEnvironment.setBypassTempDirValidation(false);
        runtimeEnvironment.setTempLocation("gs://can-sre-tools-npe-gfs-canada/temptest/temp");
		runtimeEnvironment.setWorkerRegion("northamerica-northeast1");
		runtimeEnvironment.setWorkerZone("northamerica-northeast1-a");
		runtimeEnvironment.setSubnetwork("https:/www.googleapis.com/compute/v1/projects/efx-gcp-can-svpc-npe-21fe/regions/northamerica-northeast1/subnetworks/can-sre-tools-npe-initial-0");
		
        LaunchTemplateParameters launchTemplateParameters = new LaunchTemplateParameters();
        launchTemplateParameters.setEnvironment(runtimeEnvironment);
        launchTemplateParameters.setJobName("test1");


        Map<String, String> params = new HashMap<String, String>();
            params.put("inputFile", "gs://can-sre-tools-npe-gfs-canada/temptest/abc.txt");
            params.put("output", "gs://can-sre-tools-npe-gfs-canada/temptest/output");
            launchTemplateParameters.setParameters(params);
         
        Dataflow.Projects.Templates.Launch launch = dataflowService.projects().templates().launch(projectId, launchTemplateParameters);
	    launch.setGcsPath("gs://can-sre-tools-npe-gfs-canada/temptest/templates/");
        launch.execute();
        //throw new UnsupportedOperationException("Not supported yet.");
    }

    public static class GCSEvent {
        String bucket;
        String name;
        String metageneration;
    }


}
