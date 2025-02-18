FROM tensorflow/tensorflow:2.13.0-gpu

# Set a working directory inside the container
RUN mkdir -p /app && chown -R 1001:0 /app
RUN mkdir /app/deepface

# # Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*


COPY ./deepface /app/deepface
COPY ./requirements_local /app/requirements_local.txt
COPY ./process_video.py /app/
    

# install dependencies - deepface with these dependency versions is working
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r /app/requirements_local.txt

WORKDIR /app/deepface/api/src
EXPOSE 5000
