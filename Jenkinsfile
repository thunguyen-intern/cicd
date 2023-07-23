pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = 'docker-compose.yml'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKER_IMAGE = 'hikari141/srv:latest'
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

        // stage('Generate Odoo commands for Unit test') {
        //     steps {
        //         echo "Generate Odoo commands for Unit test"
        //         script {
        //             sh "python3 unit_test.py && mv test_utils.sh ./odoo-ex-file && chmod +x test_utils.sh"
        //         }
        //     }
        // }

        stage('Login to DockerHub') {
            steps {
                script {
                    // Log into Docker registry
                    sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                }
            }
        }

        stage('Odoo Unit Test') {
            steps {
                echo "--------------------------------------------------------------------------"
                script {
                    sh "docker compose up -d"
                    sh "docker exec -it cicd-srv-1 ls /mnt/extras"
                }
            }
        }

        stage('Push Odoo Docker Image') {
            steps {
                // Push odoo docker image
                
                sh "echo 'Push Odoo Docker Image'"
                sh "docker compose push"
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
