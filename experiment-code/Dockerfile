# Replication image for the experiments of the paper (CPU only, linux/amd64).
# See DOCKER.md for what this image contains and how it relates to the
# environment used for the paper.
FROM ubuntu:22.04

# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive
# Print the output of the Python scripts immediately (docker logs)
ENV PYTHONUNBUFFERED=1

# Install common software and necessary dependencies.
# Python 3.10 is the system Python of Ubuntu 22.04 (the paper used 3.10.4).
RUN apt-get update && \
    apt-get install -y \
    git \
    pkg-config \
    curl \
    libhdf5-dev \
    python3 python3-dev python3-pip python3-wheel build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set python3 as the default python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Set the working directory in the container
WORKDIR /app

# Install the Python packages before copying the code, so that code changes
# do not invalidate this layer. requirements-lock.txt pins every package
# (resolved from requirements.txt, see DOCKER.md). PyTorch (used for the
# CRPS) is the CPU wheel of the same version from the PyTorch index, which
# avoids several GB of CUDA libraries.
COPY requirements-lock.txt /app/
RUN python3 -m pip install --no-cache-dir --no-deps \
        --index-url https://download.pytorch.org/whl/cpu torch==2.1.0+cpu && \
    python3 -m pip install --no-cache-dir -r requirements-lock.txt && \
    python3 -m pip check

# Copy the current directory contents into the container at /app
COPY . /app

# Download the third-party DaL helper modules (not redistributed, see fetch_dal.py)
RUN python3 fetch_dal.py

# Change directory to wluncert/
WORKDIR /app/wluncert

# Create the folders for temporary files and results
RUN mkdir -p /app/wluncert/tmp /app/wluncert/results/localflow

# Expose necessary ports for the Streamlit dashboards
EXPOSE 8083 8084

# Command to run the entrypoint script
ENTRYPOINT ["python3", "/app/entrypoint.py"]
