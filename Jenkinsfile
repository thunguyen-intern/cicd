pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = 'docker-compose.yml'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKER_IMAGE = 'hikari141/srv:latest'
        DOCKER_IMAGE_NAME = 'srv'
        FAILED_STAGE = ''
        webhookUrl = 'https://chat.googleapis.com/v1/spaces/1UjtyUAAAAE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=GQpOlS3UHkR2zksm5rE8bUiCKCmrIbFsH6s_fUkqkFU'
    }

    stages {
        stage('Retrieve Commit Author') {
            steps {
                script {
                    Author_ID = sh(script: """git log --format="%an" -n 1""", returnStdout: true).trim()
                    ID = sh(script: """git rev-parse HEAD""", returnStdout: true).trim()
                    sh "python3 notification.py start ${BUILD_TAG} ${Author_ID} ${ID}"
                }
            }
        }

        stage('Triggered by GitHub commits') {
            steps {
                cleanWs()
                checkout scm
                sh "echo 'Cleaned Up Workspace For Project'"
            }

            post {
                failure {
                    script {
                        env.FAILED_STAGE = env.STAGE_NAME
                    }
                }
            }
        }

        stage('Generate Odoo commands for Unit test') {
            steps {
                echo "Generate Odoo commands for Unit test"
                script {
                    sh "python3 unit_test.py > ./odoo-ex-file/test_utils.sh"
                    sh "chmod +x ./odoo-ex-file/test_utils.sh"
                }
            }

            post {
                failure {
                    script {
                        env.FAILED_STAGE = env.STAGE_NAME
                    }
                }
            }
        }

        stage('Generate Odoo commands for Upgrade module') {
            steps {
                echo "Generate Odoo commands for Upgrade module"
                script {
                    sh "python3 upgrade.py > ./odoo-ex-file/upgrade.sh"
                    sh "chmod +x ./odoo-ex-file/upgrade.sh"
                }
            }

            post {
                failure {
                    script {
                        env.FAILED_STAGE = env.STAGE_NAME
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

            post {
                failure {
                    script {
                        env.FAILED_STAGE = env.STAGE_NAME
                    }
                }
            }
        }

        stage('Odoo Run docker-compose') {
            steps {
                echo "Odoo Run docker-compose"
                script {
                    sh 'docker compose down'
                    sh 'docker compose up -d'
                }
            }

            post {
                failure {
                    script {
                        env.FAILED_STAGE = env.STAGE_NAME
                    }
                }
            }
        }

        stage('Odoo Unit Test') {
            steps {
                echo "Odoo Unit Test"
                script {
                    def testStr = sh(script: "docker exec ${env.JOB_NAME}-${DOCKER_IMAGE_NAME}-1 /mnt/extras/test_utils.sh", returnStatus: true)
                    print(testStr)
                    String outputStr = testStr?.toString().trim()
                    print(outputStr)
                    def lines = outputStr.split('\n')
                    def sumLine = lines.find {
                        it.contains("odoo.tests.runner")
                    }
                    if (sumLine != null) {
                        echo "Test summary: ${sumLine}"
                    }
                    else {
                        echo "Failed to find test summary line in output"
                    }
                }
            }    

            post {
                failure {
                    script {
                        env.FAILED_STAGE = env.STAGE_NAME
                    }
                }
            }
        }

        stage('Odoo Upgrade Module') {
            steps {
                echo "Odoo Upgrade Module"
                script {
                    def missing_modules=sh(script: "python3 upgrade_process.py", returnStdout: true).trim()
                    if (missing_modules.isEmpty()) {
                        echo "true"
                    }
                    else {
                        sh "python3 notification.py approval ${BUILD_TAG} ${Author_ID} ${missing_modules} ${env.BUILD_URL} ${ID}"
                        input "Do you want to continue and ignore missing modules?"
                    }
                    sh "docker exec ${env.JOB_NAME}-${DOCKER_IMAGE_NAME}-1 /mnt/extras/upgrade.sh"
                }
            }

            post {
                failure {
                    script {
                        env.FAILED_STAGE = env.STAGE_NAME
                    }
                }
            }
        }

        stage('Push Odoo Docker Image') {
            steps {
                // Push odoo docker image
                
                sh "echo 'Push Odoo Docker Image'"
                sh "docker compose push"
            }

            post {
                failure {
                    script {
                        env.FAILED_STAGE = env.STAGE_NAME
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                sh "python3 notification.py success ${BUILD_TAG} ${currentBuild.currentResult} ${Author_ID} ${ID} ${env.BUILD_URL} ${currentBuild.duration} "
            }
        }
        failure {
            script {
                sh "python3 notification.py failure ${BUILD_TAG} ${currentBuild.currentResult} ${Author_ID} ${ID} ${env.BUILD_URL} ${FAILED_STAGE}"
            }
        }

        aborted {
            script {
                sh "python3 notification.py aborted ${BUILD_TAG} ${currentBuild.currentResult} ${Author_ID} ${ID} ${env.BUILD_URL}"
            }
        }
    }
}
