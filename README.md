# URL Shortener

![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/jopplt/43de0052ef7377c883bb8f7547f3d767/raw/pytest-coverage-comment__main.json)

## Introduction

This project is a URL Shortener, a simple tool written in Python.
It is designed to convert long URLs into manageable short links that are easier to share and remember.
The URL Shortener uses a unique encoding algorithm to generate short URLs and can decode them back to the original URL.
The project is equipped with a comprehensive test suite ensuring its reliability and correctness.

## Software Architecture

The URL Shortener is a RESTful API written in Python.
It uses the FastAPI framework to handle HTTP requests and responses.
This application has been designed to be easily extensible and maintainable, and is divided in different layers, each one with a specific responsibility.
- **`entrypoints`**: Currently it contains only one entrypoint: the FastAPI application. It handles HTTP requests and responses, and it is the only layer that is aware of the HTTP protocol.
- **`adapters`**: It contains the implementation of the application interfaces required to let the application interact with external systems. Currently it contains only the Redis adapter, which is used to store the URLs.
- **`application`**: It contains the business logic of the application. It is the core of the application, and it is the only layer that is aware of the application domain. The application is designed to contain a set of handlers, each one being able to handle a specific request (command or query). This allows to easily extend the application by adding new handlers.
- **`domain`**: It contains the domain objects of the application. It is the layer that defines the behaviour of the application, in the form of models, commands and queries.

The `bootstrap.py` file is used to bootstrap the application, and it is responsible for the dependency injection.

The application is designed to be run as a standalone application or to be deployed in a container.
That offers the possibility to easily scale the application horizontally, by running multiple instances of the application behind a load balancer.
For that purpose, an example using kubernetes is provided in the `k8s` folder. It contains the kubernetes manifests to deploy the application in a kubernetes cluster, and a `skaffold.yaml` file to easily scaffold the application.

## Run locally


Install dependencies
```bash
poetry install
```
Start redis server:
```bash
docker run -d --rm --name redis -p 6379:6379 redis:7.0-alpine redis-server --save 60 1
```
Start the application:
```bash
poetry run gunicorn --chdir app -w 4 -k uvicorn.workers.UvicornWorker wsgi:api --bind 0.0.0.0:5001
```

## Run in docker
```bash
docker compose up -d --build --force-recreate
```

## Run in kubernetes
Requirements:
* Kubernetes cluster, such as [minikube](https://minikube.sigs.k8s.io/) or [k3d](https://k3d.io/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
* [skaffold](https://skaffold.dev/docs/install/)
* (optional) [Task](https://taskfile.dev/)

Make sure you're in the right kubernetes context (normally it is automatically set after installing minikube or k3d):
```bash
kubectl config current-context
```
Create the kubernetes cluster:
```bash
task k3d:create-cluster
```
Scaffold the application:
```bash
task skaffold:dev
```

## Usage
Use the application to create a short url:
```bash
curl -X PUT 0.0.0.0:5001/encode --header "Content-Type: application/json" --data '{"url":"https://google.com"}'
```

Try to decode the short url:
```bash
curl -X GET 0.0.0.0:5001/decode/nrfrgw
```