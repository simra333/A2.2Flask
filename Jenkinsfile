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
        stage('Test') {
            steps {
                sh 'python3 -m logger.test_flow_logger'
            }
        }
    }
}