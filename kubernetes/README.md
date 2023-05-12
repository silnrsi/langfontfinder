## How to run the language font finder locally with Docker Desktop's Kubernetes singlenode cluster

For testing Kubernetes deployment there are yaml files under `kubernetes`, that cover local developer testing. 

### Pre-requisites
On the host machine, install [Docker](https://docs.docker.com/get-docker/), then enable Kubernetes in the settings. Ensure you have built a help-keyman-app Docker image, and either tag it `docker.dallas.languagetechnology.org/keyman/help-keyman-app` or modify the `app-php` containers `image:` value to match you local copy's name. Other single node kubernetes apps are available too.

### Deploying to a desktop cluster
To deploy the dev version to the cluster do the following:
1. Ensure your `kubectl` context is set to `docker-desktop`, though the Docker Desktop systray icon or by running:  
```bash
$> kubectl config use-context docker-desktop
```
2. Create a keyman namespace if it does not already exist:
```bash
$> kubectl create ns wstech
```
3. Apply the configs for the resources and start the pod:
```bash
$> kubectl --namespace wstech apply \
       -f kubernetes/development-resources.yaml \
       -f kubernetes/service-deploy.yaml 
```
### Testing the site and `/api/deploy` webhook endpoint
The API can be reached on http://localhost:30080/docs via curl, and the deploy api is on http://localhost:30900/api/deploy, and can be activated like so:
```bash
$> curl --request POST \
   -H "Content-Type: application/json" \
   -H "X-Hub-Signature-256: sha256=d751978d36d12cab18046abb7af941ed73aac2d2a54db449513b3b21e13dd521" \
   --data '{"action":"push","ref":"refs/heads/main"}' \
   http://localhost:30900/api/deploy
```
This simulates enough of a GitHub webhook push event to pass validation on the responder.

### Clean up after testing

To remove the k8s deployment and resources, and delete everything do:
```bash
$> kubectl --namespace=keyman delete {svc,deploy,cm,secret,pvc}/help-keyman-com
```
Or just restart the deployment for further testing
```bash
$> kubectl --namespace=keyman rollout restart deploy/help-keyman-com
```
