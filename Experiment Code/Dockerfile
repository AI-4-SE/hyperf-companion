# Use an official Python runtime as a parent image
FROM ubuntu:22.04

# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install common software
RUN apt-get update && apt-get install -y \
    software-properties-common \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Setting up environment
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.9 python3.9-dev python3-pip python3-wheel build-essential
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set python3 as the default python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Install any needed packages specified in requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

# Reinstall jax with other version, doesnt work inside requierments.txt cause of faulty pip version conficts
RUN python -m pip install jax==0.4.14 && \
    python -m pip install jaxlib==0.4.13

# Change directory to wluncert/
WORKDIR /app/wluncert

# Run experiment, each job needs 3 cores set higher if your maschine allows it
RUN python main.py  --experiment multitask --jobs 1 --reps 30 --store

# Run analysis of experiments
RUN python modelinsights.py

# Command to run the streamlit dashboard
CMD ["streamlit", "run", "playground/insights-dashboard.py"]