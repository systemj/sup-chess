# Global ARGs
ARG gunicorn_port=8000
ARG prometheus_multiproc_dir=/var/tmp/prometheus
ARG python_venv_base=/opt/venv
ARG workdir=/app

### base container image
FROM python:3.9-slim-bullseye AS base
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt upgrade -y 


### build container
FROM base AS build
ARG python_venv_base
ENV PATH="$python_venv_base/bin:$PATH"

# setup virtual environment
RUN python -m venv ${python_venv_base}

# install requirements
COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt


### final container
FROM base AS final
ARG gunicorn_port
ARG prometheus_multiproc_dir
ARG python_venv_base
ARG user
ARG workdir

ENV PATH="${python_venv_base}/bin:$PATH" 
ENV gunicorn_port="${gunicorn_port}"
ENV prometheus_multiproc_dir="${prometheus_multiproc_dir}"
ENV GUNICORN_CMD_ARGS="--config gunicorn_config.py --workers 4 --bind 0.0.0.0:${gunicorn_port}"

# Copy virtual environment from build
COPY --from=build ${python_venv_base} ${python_venv_base}

# Install additional package dependencies here
RUN apt install -y gnuchess

# Copy in application files
WORKDIR ${workdir}
COPY *.py ./
COPY app ./app

# Set default user, port, and command
EXPOSE ${gunicorn_port}
USER ${user}
CMD ["gunicorn", "wsgi:app"]
