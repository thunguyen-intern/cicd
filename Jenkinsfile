pipeline {
    agent any

    environment {
        DOCKER_CONTAINER = './Dockerfile'
        DOCKER_COMPOSE = 'docker-compose.yml'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        GIT_CREDENTIALS = credentials('1')
        PROJECT_URL = 'git@github.com:thunguyen-intern/unit-test.git'
        // webhookUrl = 'https://chat.googleapis.com/v1/spaces/1UjtyUAAAAE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=GQpOlS3UHkR2zksm5rE8bUiCKCmrIbFsH6s_fUkqkFU'
    }

    stages {
        stage('Retrieve Commit Author') {
            steps {
                script {
                    Author_ID = sh(script: """git log --format="%an" -n 1""", returnStdout: true).trim()
                    ID = sh(script: """git rev-parse HEAD""", returnStdout: true).trim()
                    // sh "python3 notification.py start ${BUILD_TAG} ${Author_ID}"
                }
            }
        }

        stage('Triggered by GitHub commits') {
            steps {
                cleanWs()
                checkout scm
                sh "echo 'Cleaned Up Workspace For Project'"
            }
        }

        stage('Build Odoo Docker Image') {
            steps {
                // Build the Docker image
                checkout scm
                sh "echo 'Build Odoo Docker Image'"
                // sh "docker build -t "
                script {
                    // sh "docker build -t ${DOCKER_IMAGE} ."
                    dockerImage = docker.build("hikari141/odoo-setup:${env.BUILD_ID}")
                }
            }
        }

        stage('Odoo Unit Test') {
            steps {
                // Run Odoo Unit Test
                sh "echo 'Odoo Unit Test'"
                sh "docker run -d --name db -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=novobi -e POSTGRES_DB=db -t postgres:13"
                script {
                    dockerImage.withRun("-d --name odoo-setup -p 8069:8069 -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=novobi -e POSTGRES_DB=db --link db:db -u odoo") {
                        sh """
                            cd /opt/odoo/unit_test/
                            bash test_utils.sh
                        """
                    }
                    // sh "docker exec -it chat-srv-1 bash"
                }
            }
        }

        stage('Odoo Upgrade Module') {
            steps {
                // Run Odoo Upgrade module
                sh "echo 'Odoo Upgrade module'"
                script {
                    dockerImage.inside {
                        sh "echo 'sth'"
                    }
                }
            }
        }

        stage('Login to DockerHub') {
            steps {
                script {
                    // Log into Docker registry
                    sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                }
            }
        }

        stage('Push Odoo Docker Image') {
            steps {
                // Push odoo docker image
                
                sh "echo 'Push Odoo Docker Image'"
                sh "docker push hikari141/odoo-setup:${env.BUILD_ID}"
            }
        }
    }

    // post {
    //     always {
    //         script {
    //             sh "python3 notification.py ${BUILD_TAG} ${currentBuild.currentResult} ${Author_ID} ${ID} ${env.BUILD_URL} ${currentBuild.duration} "
    //         }
    //     }
    // }
}
