pipeline {
    agent {
        docker {
            image 'python:3.9'
        }
    }

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
        stage('Test') {
            steps {
                sh 'python3 -m logger.test_flow_logger'
                sh 'python3 -m pip install -r requirements.txt'
            }
        }
    }
}