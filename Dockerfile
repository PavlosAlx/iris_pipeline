# Use the official Airflow image with Python 3.11
FROM apache/airflow:2.6.3-python3.11

# Copy our requirements.txt into the image
COPY requirements.txt /opt/airflow/requirements.txt

# Switch to the airflow user (so pip won’t complain about root)
USER airflow

# Install into the user site (home/.local), which is on PYTHONPATH
RUN pip install --no-cache-dir --user -r /opt/airflow/requirements.txt

# Ensure that user‐installed scripts are on PATH
ENV PATH="/home/airflow/.local/bin:${PATH}"

# Switch back just in case
USER airflow
