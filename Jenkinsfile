pipeline {
    agent any

    environment {
        APP_VERSION = 'v1.0'
        DOCKER_IMAGE = "simraabid/pythonapp:${APP_VERSION}"
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
                sh '''
                    cd /home/A2.2Flask
                    docker build -t ${DOCKER_IMAGE} .
                '''
                }
            }
        stage('vulnerability scanning') {
            steps {
                sh '''
                    # Install and run Trivy
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy image --severity HIGH,CRITICAL ${DOCKER_IMAGE}
                '''
            }
        }
        stage('Docker Push') {
            steps {
                sh 'docker push ${DOCKER_IMAGE}'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl set image deployment/pythonapp-deployment pythonapp=${DOCKER_IMAGE}
                    kubectl rollout status deployment/pythonapp-deployment
                    kubectl get pods
                    kubectl get services
                '''
            }
        }
    }

    post {
        always {
            sh '''
                echo "Final Pipeline Status:"
                kubectl get all
                kubectl logs -l app=pythonapp --tail=100 || true
            '''
        }
        success {
            sh 'echo Deployment successful!'
        }
        failure {
            sh '''
                echo Pipeline failed! Checking logs...
                kubectl describe pods -l app=pythonapp
                kubectl logs -l app=pythonapp --tail=200
            '''
        }
    }
}