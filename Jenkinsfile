pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Simulates the checkout of code from the repository
                script {
                    echo 'Checking out code...'
                    // git url: 'https://github.com/Takk8IS/RiskStreamML.git'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Here you would add your actual test commands
                sh 'python -m pytest' // Example: if you had tests with pytest
                echo 'No specific tests configured, skipping actual test run.'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t riskstreamml:latest .'
            }
        }

        stage('Run Application (Container)') {
            steps {
                // Runs the application inside the container for validation
                sh 'docker run --rm -v $(pwd)/output:/app/output -v $(pwd)/data:/app/data -v $(pwd)/logs:/app/logs -v $(pwd)/hdfs_simulation:/app/hdfs_simulation riskstreamml:latest'
            }
        }

        stage('Clean Up') {
            steps {
                sh 'docker rmi riskstreamml:latest'
                sh 'make clean'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
