FROM nvidia/cuda:12.2.0-cudnn8-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    curl \
    wget \
    vim \
    htop \
    tmux \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir \
    torch==2.1.0 \
    transformers==4.35.0 \
    langchain==0.1.0 \
    langgraph==0.0.20 \
    openai==1.3.0 \
    jupyter==1.0.0 \
    jupyterlab==4.0.0 \
    ipywidgets==8.1.0 \
    matplotlib==3.8.0 \
    pandas==2.1.0 \
    numpy==1.24.0 \
    scikit-learn==1.3.0 \
    requests==2.31.0 \
    pydantic==2.5.0 \
    python-dotenv==1.0.0

# Install vector databases
RUN pip3 install --no-cache-dir \
    pymilvus==2.3.0 \
    pinecone-client==2.2.0 \
    chromadb==0.4.0

# Install monitoring tools
RUN pip3 install --no-cache-dir \
    prometheus-client==0.19.0 \
    opentelemetry-api==1.21.0 \
    opentelemetry-sdk==1.21.0

# Create working directory
WORKDIR /workspace

# Set up Jupyter
RUN jupyter notebook --generate-config && \
    echo "c.NotebookApp.token = ''" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = True" >> ~/.jupyter/jupyter_notebook_config.py

# Expose Jupyter port
EXPOSE 8888

# Start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
