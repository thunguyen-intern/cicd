pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = 'docker-compose.yml'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKER_IMAGE_BLUE = 'odoo_15_blue'
        DOCKER_IMAGE_GREEN = 'odoo_15_green'
    }

    stages {
        stage('Cleanup') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Docker Login') {
            steps {
                script {
                    // Log into Docker registry
                    sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                }
            }
        }

        stage('Docker Compose') {
            steps {
                script {
                    sh '''
                        if [ "$(docker ps -aq)" ]; then
                            docker stop $(docker ps -aq)
                            docker rm $(docker ps -aq)
                        else
                            echo "No running containers to stop"
                        fi
                    '''
                    sh 'docker compose up -d'
                    sh 'docker ps'
                }
            }
        }

        stage('Deploy Blue') {
            steps {
                script {
                    // set the Docker Compose project name to 'blue'
                    sh "export COMPOSE_PROJECT_NAME=blue"
                    // run the Docker Compose file
                    sh "docker compose up -d"
                }
            }
        }

        stage('Blue: Run Tests') {
            steps {
                // insert your tests here
                sh "echo 'Hello!'"
            }
        }

        stage('Switch Blue/Green') {
            steps {
                script {
                    // Replace the Nginx configuration to route traffic to the 'blue' environment
                    sh "sudo cp nginx/nginx.blue.conf /etc/nginx/nginx.conf"
                    sh "sudo service nginx reload"
                }
            }
        }

        stage('Deploy Green') {
            steps {
                script {
                    // set the Docker Compose project name to 'green'
                    sh "export COMPOSE_PROJECT_NAME=green"
                    // run the Docker Compose file
                    sh "docker compose up -d"
                }
            }
        }

        stage('Green: Run Tests') {
            steps {
                // insert your tests here
                sh "echo 'Hello World!'"
            }
        }

        stage('Switch Green/Blue') {
            steps {
                script {
                    // Replace the Nginx configuration to route traffic to the 'green' environment
                    sh "sudo cp nginx/nginx.green.conf /etc/nginx/nginx.conf"
                    sh "sudo service nginx reload"
                }
            }
        }

        stage('Cleanup Blue') {
            steps {
                script {
                    // Remove the 'blue' environment
                    sh "export COMPOSE_PROJECT_NAME=blue"
                    sh "docker compose down"
                }
            }
        }
    }
}