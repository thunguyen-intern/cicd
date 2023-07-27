pipeline {
    // agent {
    //     label 'odoo1'
    // }
    agent any
    
    environment {
        DOCKER_COMPOSE = 'docker-compose.yml'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKER_IMAGE = 'hikari141/srv:latest'
        DOCKER_IMAGE_NAME = 'odoo_15'
        FAILED_STAGE = ''
    }

    stages {
        stage('Triggered-by-GitHub-commits') {
            steps {
                cleanWs()
                checkout scm
                sh "echo 'Cleaned Up Workspace For Project'"
                script {
                    sh "pip3 install -r agent_requirements.txt"
                }
            }

            post {
                failure {
                    script {
                        FAILED_STAGE = env.STAGE_NAME
                    }
                }
            }
        } 

        stage('Retrieve-Commit-Author') {
            steps {
                script {
                    Author_ID = sh(script: """git log --format="%an" -n 1""", returnStdout: true).trim()
                    Author_Email = sh(script: """git log --format="%ae" -n 1""", returnStdout: true).trim()
                    ID = sh(script: """git rev-parse HEAD""", returnStdout: true).trim()
                    uId = sh(script: "python3 retrieve_user_id.py ${Author_Email}", returnStdout: true).trim()
                    // branch = ((sh(script: """git log --format="%D" -n 1""", returnStdout: true).trim()).split(','))[1]
                    // sh "python3 notification.py start ${Author_ID}"
                    // branch
                }
            }
        }


        stage('Generate-Odoo-commands-for-Unit-test') {
            steps {
                echo "Generate Odoo commands for Unit test"
                script {
                    sh """
                        python3 unit_test.py > ./unit_test/test_utils.sh
                        chmod +x ./unit_test/test_utils.sh
                    """
                }
            }

            // post {
            //     failure {
            //         script {
            //             FAILED_STAGE = env.STAGE_NAME
            //         }
            //     }
            // }
        }

        stage('Generate-Odoo-commands-for-Upgrade-module') {
            steps {
                echo "Generate Odoo commands for Upgrade module"
                script {
                    sh """
                        python3 upgrade.py > ./unit_test/upgrade.sh
                        chmod +x ./unit_test/upgrade.sh
                    """
                }
            }

            // post {
            //     failure {
            //         script {
            //             FAILED_STAGE = env.STAGE_NAME
            //         }
            //     }
            // }
        }

        stage('Login-to-DockerHub') {
            steps {
                script {
                    // Log into Docker registry
                    sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                }
            }

            // post {
            //     failure {
            //         script {
            //             FAILED_STAGE = env.STAGE_NAME
            //         }
            //     }
            // }
        }

        stage('Odoo-Run-docker-compose') {
            steps {
                echo "Odoo Run docker-compose"
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

            // post {
            //     failure {
            //         script {
            //             FAILED_STAGE = env.STAGE_NAME
            //         }
            //     }
            // }
        }

        stage('Odoo-Unit-Test') {
            steps {
                echo "Odoo Unit Test"
                script {
                    def result=sh(script: "docker exec ${DOCKER_IMAGE_NAME} /mnt/extras/test_utils.sh", returnStdout: true).trim()
                    def res = result[-1]
                    if (res == '0') {
                        echo "success"
                    }
                    else {
                        error("Unit test failed")
                    }
                }
            }  
            // post {
            //     failure {
            //         script {
            //             FAILED_STAGE = env.STAGE_NAME
            //         }
            //     }
            // }  
        }

        stage('Odoo-Upgrade-Module') {
            steps {
                echo "Odoo Upgrade Module"
                script {
                    up_modules = "None"
                    res=sh(script: "python3 upgrade_process.py", returnStdout: true).trim()
                    if (res.isEmpty()) {
                        up_modules = "None"
                    }
                    else {
                        result = res.split('\n')
                        echo "${result}"
                        if (result.size() == 1) {
                            echo "true"
                            up_modules = result[0]
                        }
                        else {
                            missing_modules = result[0]
                            up_modules = result[-1]
                            echo "----------------------------------------------------------------"
                            // sh "python3 notification.py approval ${branch} ${Author_ID} ${missing_modules} ${uId} ${env.BUILD_URL} ${ID}"
                            input "Do you want to continue and ignore missing modules?"
                        }
                        sh "docker exec ${DOCKER_IMAGE_NAME} /mnt/extras/upgrade.sh"
                    }
                }
            }

            // post {
            //     failure {
            //         script {
            //             FAILED_STAGE = env.STAGE_NAME
            //         }
            //     }
            // }
        }

        stage('Push-Odoo-Docker-Image') {
            steps {
                sh "echo 'Push Odoo Docker Image'"
                sh "docker tag cicd-srv:latest hikari141/odoo:${ID}"
                sh "docker push hikari141/odoo:${ID}"
            }

            // post {
            //     failure {
            //         script {
            //             FAILED_STAGE = env.STAGE_NAME
            //         }
            //     }
            // }
        }

        stage('Deploy to agent') {
            agent {
                label 'odoo1'
            }
            steps {
                sh "docker run --name odoo_tmp -v /home/vagrant/server/Odoo:/home/odoo/.local/share/Odoo -h odoo --network=odoo hikari141/odoo:${ID}"
            }
        }
    }

    // post {
    //     success {
    //         script {
    //             sh "python3 notification.py success ${branch} ${currentBuild.currentResult} ${Author_ID} ${uId} ${ID} ${env.BUILD_URL} ${currentBuild.duration} ${up_modules}"
    //         }
    //     }
    //     failure {
    //         script {
    //             sh "python3 notification.py failure ${branch} ${currentBuild.currentResult} ${Author_ID} ${uId} ${ID} ${env.BUILD_URL} ${FAILED_STAGE}"
    //         }
    //     }

    //     aborted {
    //         script {
    //             sh "python3 notification.py aborted ${branch} ${currentBuild.currentResult} ${Author_ID} ${uId} ${ID} ${env.BUILD_URL}"
    //         }
    //     }
    // }
}
