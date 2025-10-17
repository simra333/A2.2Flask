pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'jenkins-setup', url: 'https://github.com/simra333/A2.2Flask.git'
            }
        }

        stage('Build') {
            steps {
                sh 'echo Building the application...'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t PythonApp:latest .'
            }
        }

        stage('Push Image') {
            steps {
                sh 'docker tag PythonApp:latest simraabid/PythonApp:latest'
                sh 'docker push simraabid/PythonApp:latest'
            }
        }
    }
}