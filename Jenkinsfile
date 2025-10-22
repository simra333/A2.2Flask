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
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && python3 -m pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh '. venv/bin/activate && python -m logger.test_flow_logger'
                sh 'echo Test completed successfully!'
            }
        }
        stage('Docker Build') {
            steps {
                sh 'docker build -t pythonapp:latest .'
            }
        }
        stage('Docker Push') {
            steps {
                sh 'docker tag pythonapp:latest simraabid/pythonapp:latest'
                sh 'docker push simraabid/pythonapp:latest'
            }
        }
        stage('Deploy') {
            steps {
                sh 'echo Stopping old container...'
                sh 'docker stop pythonapp-container || true'
                sh 'docker rm pythonapp-container || true'
                
                sh 'echo Starting new container...'
                sh 'docker run -d --name pythonapp-container -p 5000:5000 pythonapp:latest'
            }
        }
    }

    post {
        success {
            sh 'echo Deployment successful!'
        }
        failure {
            sh 'echo Pipeline failed!'
        }
    }
}