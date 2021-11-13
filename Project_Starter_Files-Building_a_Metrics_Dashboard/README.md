[//]: # (Image References)

[image1]: ./answer-img/Exposing_Grafana.png
[image2]: ./answer-img/verify_the_monitoring_installation.png
[image3]: ./answer-img/dataSourcePrometheus2.png
[image4]: ./answer-img/dataSourcePrometheus.png
[image5]: ./answer-img/jaegerSpan.png
[image6]: ./answer-img/jaegerGrafana.png
[image7]: ./answer-img/SLIs.png  
[image8]: ./answer-img/SLIs2.png
[image9]: ./answer-img/pods.png


**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

* Run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation
![][image2]  
![][image9]  
## Setup the Jaeger and Prometheus source
* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.  
```
kubectl port-forward -n monitoring service/prometheus-kube-prometheus-prometheus 9090
kubectl port-forward -n monitoring prometheus-grafana-588475b7c6-mgs49  3000 (Check pod name with kubectl get pods --namespace=monitoring)
# Add an ingress to cluster
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.3/deploy/static/provider/cloud/deploy.yaml
```
* Create “all-in-one” Jaeger instance - When you have the Jaeger Operator deployed in the observability namespace, create a Jaeger instance:  
```
kubectl apply -n observability -f - <<EOF
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
 name: simplest
EOF
```  
![][image1]  
## Create a Basic Dashboard
* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.  
![][image3] 
![][image4] 
## Describe SLO/SLI
* Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.  
A Service-Level Indicator (SLI) is a specific metric used to measure the performance of a service. SLI is a general metric to measure uptime and latency.  But truly what we require within the conclusion is a genuine estimation.  based on an SLO of monthly uptime and request-response time. In this case,  SLI would be the actual measurement of the uptime. Perhaps during that year, you actually achieved 99.5% uptime and request-response time or 97.3% uptime and request response time. These measurements are SLI. Notice that the above example is a ratio which is a measurement to a given amount of time (the measured uptime and request-response time per year).   
## Creating SLI metrics.
* It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs. 
A Service-Level Indicator (SLI) is a specific metric used to measure the performance of a service. These metrics are relevant and built around the Four Golden Signals (latency, Failure rate, uptime, Network and Resource capcity)

  * The SLO will be latency. The SLI will be the response time of requests.   
  * The SLO will be Failure rate. The SLI for that will be he amount of failures in a unit of time.  
  * The SLO will be uptime. The SLI for that will be time a service is active.  
  * The SLO will be Network capcity. The SLI indicates the average bandwidth in a specifi period of time.  
  * The SLO will be Resource capcity. The SLI for that will be he amount of CPU and RAM usage.

## Create a Dashboard to measure our SLIs
* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.  
![][image7]

## Tracing our Flask App
*  Create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here.
```
kubectl port-forward svc/backend-service 8081:8081 (then head to http://localhost:8081/api)

# Run some request to the api endpoint
for i in 0 1 2 3 4 5 6 7 8 9; do curl localhost:8081/api; done

# Call Jaeger UI
kubectl port-forward -n observability  service/simplest-query --address 0.0.0.0 3002:16686
```
![][image5]   
## Jaeger in Dashboards
* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.
![][image6] 
## Report Error
*TODO:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue.

TROUBLE TICKET

Name: Request endpoint star fail throw `405 Method Not Allowed`

Date: Nov 13 2021, 17:30 PM

Subject: Backend can't acces MongoDB

Affected Area: Backend Service

Severity: High

Description:  As we port-forwarding the application accessing /star endpoint, it throw 405 error which is caused by the mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb URL is not exist in the cluster. We need to make the MongoDB URL available for the cluster.


## Creating SLIs and SLOs
* Create an SLO guaranteeing that our application has a 99.95% uptime per month. Name three SLIs that you would use to measure the success of this SLO.  
   - Latency: The response time of requests should less than 30ms within a month.
   - Failure rate: Ensure that the status code 2xx rates are around 97%.
   - Uptime: Uptime nedd to be approximate 99 percent within a month and response time should be around 500 milliseconds.
   
## Building KPIs for our plan
* Now that we have our SLIs and SLOs, create KPIs to accurately measure these metrics. We will make a dashboard for this, but first write them down here.  
   - Latency: Response time.  
   - Failure rate: Errors per second / response rate per second.    
   - Uptime: Sucessful requests during pod uptime.  
   - Network capcity: successful request per second /  request per second.  
   - Resource capcity: CPU, RAM usage per pod.  
## Final Dashboard
* Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  
![][image7]  
![][image8]  
* Uptime: Uptime of each pod.  
* Requests per second: Number of successful Flask requests per second.  
* Errors per second: Number of failed (non HTTP 200) responses per second.  
* Total requests per minute: The total number of requests measured within one minute.    
* Average response time [30s]: The average response time measured over 30 seconds.   
* Memory usage: The memory usage of the Flask app.  
* CPU usage: The CPU usage of the Flask app as measured over 30 seconds.   
* Jaeger Spans: Tracing Backend Service using Jaeger.  
