pipeline {
    agent any

    stages {
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
    }
}