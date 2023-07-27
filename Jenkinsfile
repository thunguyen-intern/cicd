pipeline {
    agent any

    stages {
        stage('Pull Odoo Image') {
            steps {
                script {
                    docker.image().pull()
                }
            }
        }

        stage('Deploy to Blue') {
            steps {
                script {
                    // set the Docker Compose project name to 'blue'
                    sh "export COMPOSE_PROJECT_NAME=blue"
                    // run the Docker Compose file
                    sh "docker compose up -f docker-compose.yml -d"
                }
            }
        }

        stage('Run Tests') {
            steps {
                // insert your tests here
            }
        }

        stage('Switch Nginx to Blue') {
            steps {
                script {
                    // Replace the Nginx configuration to route traffic to the 'blue' environment
                    sh "sudo cp nginx/nginx.blue.conf /etc/nginx/nginx.conf"
                    sh "sudo service nginx reload"
                }
            }
        }

        stage('Deploy to Green') {
            steps {
                script {
                    // set the Docker Compose project name to 'green'
                    sh "export COMPOSE_PROJECT_NAME=green"
                    // run the Docker Compose file
                    sh "docker compose up -f docker-compose.yml -d"
                }
            }
        }

        stage('Run Tests') {
            steps {
                // insert your tests here
            }
        }

        stage('Switch Nginx to Green') {
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