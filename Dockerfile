# Fresquito: Weather API + pipeline (refactored)
FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3-pip

WORKDIR /app

# Install package and dependencies (install, not -e: no setup.py in pyproject-only project)
COPY pyproject.toml requirements.txt ./
COPY src ./src
RUN pip3 install --no-cache-dir .

# All CSV and generated artifacts live in data/
COPY data ./data
COPY interfaz ./interfaz

EXPOSE 5000

CMD ["fresquito"]
