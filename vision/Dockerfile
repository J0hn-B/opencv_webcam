FROM python:3.13.0a4-slim-bullseye

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    bzip2 \
    g++ \
    git \
    graphviz \
    libgl1-mesa-glx \
    libhdf5-dev \
    openmpi-bin \
    wget \
    python3-tk && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /vision
