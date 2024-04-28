Notes

- Need to provision an AI service resource for billing
- When creating the ACI (Azure container instance)
  - Choose the same subscription, resource group as the provisioned AI service rescource
  - Image
    - image source: other registry
    - image type: public
    - image: mcr.microsoft.com/azure-cognitive-services/textanalytics/language:latest (example)
  - Need to change the container TCP port from 80 to 5000
  - Three ENVs are required when creating the container instance
    - ApiKey: <the api key> - mark as secure
    - Billing: <the AI service resource endpoint> - mark as secure
    - Eula: accept
- Deployment
  - takes 5-10 min
  - when it's ready
    - Status: Running
    - IP Address: public IP, can be used to access the container
    - FQDN: the fully qualified domain name, can be used to access the container
- Also can deploy locally:
  - `$ docker run --rm -it -p 5000:5000 --memory 12g --cpus 1 mcr.microsoft.com/azure-cognitive-services/textanalytics/language:latest Eula=accept Billing=<yourEndpoint> ApiKey=<yourKey>`
- Test
  - `$ sh script_container_test.sh`
  ```json
  {"documents":[{"id":"1","detectedLanguage":{"name":"English","iso6391Name":"en","confidenceScore":0.98},"warnings":[]},{"id":"2","detectedLanguage":{"name":"French","iso6391Name":"fr","confidenceScore":1.0},"warnings":[]}],"errors":[],"modelVersion":"2023-12-01"}%
  ```
