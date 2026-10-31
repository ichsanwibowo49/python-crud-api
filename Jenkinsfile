pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t python-crud-api:latest .'
            }
        }

        stage('Check Python Syntax') {
            steps {
                sh 'docker run --rm python-crud-api:latest python -m py_compile app.py'
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    docker stop production-api-container || true
                    docker rm production-api-container || true
                    docker volume create production-api-data

                    docker run -d \
                        --name production-api-container \
                        -p 5000:5000 \
                        -v production-api-data:/var/lib/backend_data \
                        python-crud-api:latest
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    for attempt in 1 2 3 4 5 6 7 8 9 10; do
                        if docker exec production-api-container python -c "from urllib.request import urlopen; response = urlopen('http://localhost:5000/health', timeout=2); print(response.read().decode())"; then
                            exit 0
                        fi
                        sleep 2
                    done

                    docker logs production-api-container
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline, deployment, and health check completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the Console Output.'
        }
    }
}
