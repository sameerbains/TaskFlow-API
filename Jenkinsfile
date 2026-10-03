pipeline {
    agent any

    environment {
        IMAGE_NAME = 'taskflow-api'
        CONTAINER_NAME = 'taskflow-jenkins'
        DEPLOY_PORT = '5002'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building TaskFlow API Docker image...'
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests...'
                sh 'python3 -m pytest -v'
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Running Flake8 code quality analysis...'
                sh 'python3 -m flake8 app.py tests --max-line-length=100'
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Running Bandit security scan...'
                sh 'python3 -m bandit -r app.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying TaskFlow API...'
                sh '''
                    docker rm -f ${CONTAINER_NAME} 2>/dev/null || true
                    docker run -d \
                      --name ${CONTAINER_NAME} \
                      -p ${DEPLOY_PORT}:5000 \
                      ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Release') {
            steps {
                echo 'Creating release image...'
                sh 'docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest'
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Checking deployed application health...'
                sh '''
                    sleep 3
                    curl --fail http://127.0.0.1:${DEPLOY_PORT}/health
                    docker ps --filter name=${CONTAINER_NAME}
                '''
            }
        }
    }

    post {
        success {
            echo 'TaskFlow CI/CD pipeline completed successfully.'
        }

        failure {
            echo 'TaskFlow CI/CD pipeline failed. Check the stage logs.'
        }
    }
}
