# Task Scheduler 

This project demonstrates a task scheduler built with Python and Flask, containerized with Docker, and orchestrated using Kubernetes with Argo CD, including a MariaDB database.

## Prerequisites

Before starting, ensure you have the following installed on your system:
- **Docker**: For creating and managing containers.
- **Kubernetes Cluster**: Minikube, or any Kubernetes cluster you have access to.
- **kubectl**: For interacting with your Kubernetes cluster.
- **Access to a Terminal/Command Prompt**: For executing commands.
- **Argo CD**: Interacting with your Kubernetes cluster using Argo CD.
  
## Setup Instructions

### Step 1: Clone the Repository

Clone this repository to your local machine using the following commands:

`git clone https://github.com/UncleWeeds/DevOps-MLOps-Assignment`

`cd DevOps-MLOps-Assignment` 

### Step 2: Start Your Kubernetes Cluster

Ensure your Kubernetes cluster is running. If you're using Minikube, you can start it with the following command:

`minikube start`

### Step 3: Local Setup for Task 1 (Without Docker and Kubernetes)

Before proceeding with Docker and Kubernetes, you can test the Flask application locally by following these steps:

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

`export FLASK_APP=run.py`

`export FLASK_ENV=development`

`flask run`

For testing purposes, You can use these commands:

To test all the tasks:

`curl -X GET http://127.0.0.1:5000/tasks/`

To create a Normal Task:

`curl -X POST http://127.0.0.1:5000/tasks/ 
-H 'Content-Type: application/json' 
-d '{"name": "One-time Task", "execution_time": "2024-03-07T20:30:00"}'`

For Recurring Tasks: 

`curl -X POST http://127.0.0.1:5000/tasks/ 
-H 'Content-Type: application/json' 
-d '{"name": "Daily Task", "execution_time": "2024-03-07T20:35:00", "recurrence": "daily"}'`

To get a single task: 

`curl -X GET http://127.0.0.1:5000/tasks/1`

To delete a task: 

`curl -X DELETE http://127.0.0.1:5000/tasks/<id>`


### Step 4: Docker Setup

Before deploying the application, you'll need to build a Docker image. Ensure Docker is installed and running on your system. Then, follow these steps:

**Build the Docker Image**

   Navigate to the root directory of the project where the `Dockerfile` is located, and run the following command to build your Docker image:

   `docker build -t task-scheduler .`

   `docker run -p 5000:5000 task-scheduler` (This command runs the task-scheduler Docker image as a container, mapping port 5000 of the container to port 5000 on your host, allowing you to access the application at http://localhost:5000.)

### Step 5: Kubernetes Setup

After setting up Docker and building your image, the next step is to deploy the application to a Kubernetes cluster. This guide assumes you have a running Kubernetes cluster and `kubectl` configured to communicate with your cluster.

**Deploy the Application**

   Use the provided Kubernetes YAML files to deploy the Task Scheduler application and its required components. Navigate to the `kubernetes` directory and apply the configurations:

  `kubectl apply -f scheduler.yaml`

  `kubectl port-forward svc/task-scheduler-service 5000:5000` ( This command forwards port 5000 of the task-scheduler-service service to port 5000 on your localhost. You can now access the Task Scheduler application at port 5000.)


  ### Step 6: Configure Argo CD

1. **Install Argo CD**

   `kubectl create namespace argocd`
   
   `kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`

3. **Access Argo CD UI**

     `kubectl port-forward svc/argocd-server -n argocd 8080:443`

4. **Login to Argo CD**

      Retrieve the initial admin password:

     `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo`

     Use `admin` as the username and the retrieved password to log in.


  ### Step 7: Set Up Argo CD Application

  Apply the Argo CD Application
  
  Navigate to the directory containing argo-application.yaml and apply it:

  `kubectl apply -f argo-application.yaml`


  ### Step 8: Verify Deployment

1. Check Deployment and Pods

Ensure that Argo CD has synchronized the application:  

`kubectl get deployment`

`kubectl get pods`

2. Access the Application

Check out the Argo CD running in localhost:8080 and check if it is showing the current cluster.

3. Test Automated Deployment:

    Make a Change in scheduler.yaml:
   
   For example, update the replicas count:

        spec:
           replicas: 2  # Change from 1 to 2

Commit and Push the Change:

`git add scheduler.yaml`

`git commit -m "Updated replicas count to 2"`

`git push origin main`

Observe Argo CD UI:

    Watch for the application to detect the change and automatically sync.
    
    You should see the number of pods increase according to the updated replica count.


## Task 3: Implementing a Canary Release with Argo Rollouts

1. Apply the Rollout Configuration (Navigate to the dir)

`kubectl apply -f rollout.yaml`

### Step 10: Trigger a Rollout

1. Update Application and Build New Docker Image ( I already did this so no need to do this part, I image has already been pushed to Docker hub)

Make necessary changes, build, and push a new Docker image:

`docker build -t uweeds/task-scheduler:v2 .`

`docker push uweeds/task-scheduler:v2`

2. Update rollout.yaml

Update the image in rollout.yaml:

    spec:

      template:
  
         spec:
         
           containers:
      
           - name: task-scheduler
      
             image: uweeds/task-scheduler:v2 (I have already placed it in v2 to check it out, if you want to try you can remove the v2 and try the uweeds/task-scheduler:latest to check if the rollout is working or not)


3. Commit and Push Changes

   Update the repository:

   `git add kubernetes/rollout.yaml`
   
   `git commit -m "Updated rollout to use task-scheduler v2"`

   `git push origin main`



4. Apply Updated Rollout

Apply the updated rollout configuration:

`kubectl apply -f kubernetes/rollout.yaml`

### Step 11: Monitor the Rollout

1. Install Argo Rollouts Plugin

Install the Argo Rollouts plugin:

`curl -LO https://github.com/argoproj/argo-rollouts/releases/download/v1.1.0/kubectl-argo-rollouts-linux-amd64`

`chmod +x ./kubectl-argo-rollouts-linux-amd64`

`sudo mv ./kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts`

2. Monitor Rollout

Use the plugin to watch the rollout:

`kubectl argo rollouts get rollout task-scheduler-rollout --watch`

## Cleanup Instructions

1. Delete the Rollout:

    This will stop the pods managed by the Argo Rollouts.

   `kubectl delete rollout task-scheduler-rollout`

2. Delete the Deployment:

    This will stop the pods managed by the Kubernetes Deployment.

   `kubectl delete deployment task-scheduler-deployment`

3. Verify Deletion:

    Check that all pods are terminated.

   `kubectl get pods`

4. kubectl delete service task-scheduler-service

   `kubectl delete service task-scheduler-service`

5. Delete Namespaces

`kubectl delete namespace argocd`

`kubectl delete namespace argo-rollouts`

6. Delete Remaining ReplicaSets and Pods

Ensure all remaining ReplicaSets and pods are forcefully deleted:

  Delete ReplicaSets:

  `kubectl delete replicaset -l app=task-scheduler --force --grace-period=0`

  Delete Pods:

  `kubectl delete pods -l app=task-scheduler --force --grace-period=0`

7. Final Verification

Confirm that all resources have been deleted:

  Check Remaining Resources:

 `kubectl get all -l app=task-scheduler`

 Check Remaining Namespaces:

 `kubectl get namespaces`















































