# Makefile for common task automation

.PHONY: install run clean test

# Installs project dependencies
install:
	pip install --upgrade pip
	pip install -r requirements.txt

# Runs the main project pipeline
run:
	python run.py

# Cleans generated files (database, reports, charts)
clean:
	rm -f data/payments.db
	rm -rf output logs hdfs_simulation

# Docker commands
build-docker:
	docker build -t riskstreamml .

run-docker:
	docker run --rm -v $(pwd)/output:/app/output -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs -v $(pwd)/hdfs_simulation:/app/hdfs_simulation riskstreamml

# Test command
test:
	python -m pytest tests/
