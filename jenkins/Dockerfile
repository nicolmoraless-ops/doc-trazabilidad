# Jenkins LTS con las herramientas que usa el pipeline
FROM jenkins/jenkins:lts-jdk17
USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv python3-pip doxygen curl \
 && rm -rf /var/lib/apt/lists/*
USER jenkins
