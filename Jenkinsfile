pipeline {
    agent any
    
    environment {
        DOCKER_COMPOSE = 'docker-compose.yml'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKER_IMAGE_NAME = 'odoo_15'
        IMAGE = 'odoo'
        FAILED_STAGE = ''
        AGENT = 'odoo1'
        PSQL_CREDENTIALS = credentials('postgres')
        DATABASE = 'postgres'
    }

    stages {
        // stage('Triggered By Github Commits') {
        //     steps {
        //         cleanWs()
        //         checkout scm
        //         sh "echo 'Cleaned Up Workspace For Project'"
        //         script {
        //             sh "pip3 install -r agent_requirements.txt"
        //         }
        //     }
        // } 

        // stage('Retrieve Commit Author') {
        //     steps {
        //         script {
        //             Author_ID = sh(script: """git log --format="%an" -n 1""", returnStdout: true).trim()
        //             Author_Email = sh(script: """git log --format="%ae" -n 1""", returnStdout: true).trim()
        //             ID = sh(script: """git rev-parse HEAD""", returnStdout: true).trim()
        //             uId = sh(script: "python3 retrieve_user_id.py ${Author_Email}", returnStdout: true).trim()
        //             // branch = ((sh(script: """git log --format="%D" -n 1""", returnStdout: true).trim()).split(','))[1]
        //             // sh "python3 notification.py start ${Author_ID}"
        //             // branch
        //         }
        //     }
        // }


        // stage('Generate Odoo Unit Test Commands') {
        //     steps {
        //         echo "Generate Odoo Unit Test Commands"
        //         script {
        //             sh """
        //                 python3 unit_test.py > ./unit_test/test_utils.sh
        //                 chmod +x ./unit_test/test_utils.sh
        //             """
        //         }
        //     }
        // }

        // stage('Generate Odoo Upgrade Module Commands') {
        //     steps {
        //         echo "Generate Odoo Upgrade Module Commands"
        //         script {
        //             sh """
        //                 python3 upgrade.py > ./unit_test/upgrade.sh
        //                 chmod +x ./unit_test/upgrade.sh
        //             """
        //         }
        //     }
        // }

        // stage('Login Dockerhub') {
        //     steps {
        //         script {
        //             // Log into Docker registry
        //             sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
        //         }
        //     }
        // }

        // stage('Check And Remove Old Image') {
        //     steps {
        //         script {
        //             def imgExists = sh(script: "docker image ls --format '{{.Repository}}' | grep -w ${IMAGE} || true", returnStdout: true).trim()

        //             if (imgExists == '${DOCKER_IMAGE_NAME}') {
        //                 echo "Found '${IMAGE}' image. Removing..."

        //                 sh "docker rmi -f ${IMAGE}"
        //             }
        //             else {
        //                 echo "No '${IMAGE}' image found."
        //             }
        //         }
        //     }
        // }

        // stage('Run Docker Compose') {
        //     steps {
        //         echo "Run Docker Compose"
        //         script {
        //             sh '''
        //                 if [ "$(docker ps -aq)" ]; then
        //                     docker stop $(docker ps -aq)
        //                     docker rm $(docker ps -aq)
        //                 else
        //                     echo "No running containers to stop"
        //                 fi
        //             '''
        //             sh 'docker compose up -d'
        //             sh 'docker ps'
        //         }
        //     }
        // }

        // stage('Odoo Unit Test') {
        //     steps {
        //         echo "Odoo Unit Test"
        //         script {
        //             def result=sh(script: "docker exec ${DOCKER_IMAGE_NAME} /mnt/extras/test_utils.sh", returnStdout: true).trim()
        //             def res = result[-1]
        //             if (res == '0') {
        //                 echo "success"
        //             }
        //             else {
        //                 error("Unit test failed")
        //             }
        //         }
        //     } 
        // }

        // stage('Odoo Upgrade Module') {
        //     steps {
        //         echo "Odoo Upgrade Module"
        //         script {
        //             up_modules = "None"
        //             res=sh(script: "python3 upgrade_process.py", returnStdout: true).trim()
        //             if (res.isEmpty()) {
        //                 up_modules = "None"
        //             }
        //             else {
        //                 result = res.split('\n')
        //                 echo "${result}"
        //                 if (result.size() == 1) {
        //                     echo "true"
        //                     up_modules = result[0]
        //                 }
        //                 else {
        //                     missing_modules = result[0]
        //                     up_modules = result[-1]
        //                     echo "----------------------------------------------------------------"
        //                     // sh "python3 notification.py approval ${branch} ${Author_ID} ${missing_modules} ${uId} ${env.BUILD_URL} ${ID}"
        //                     input "Do you want to continue and ignore missing modules?"
        //                 }
        //                 sh "docker exec ${DOCKER_IMAGE_NAME} /mnt/extras/upgrade.sh"
        //             }
        //         }
        //     }
        // }

        // stage('Push Image') {
        //     steps {
        //         script {
        //             def img=sh(script: """docker inspect --format='{{.Image}}' '${DOCKER_IMAGE_NAME}'""", returnStdout: true).trim()
        //             sh "docker tag ${img} ${DOCKERHUB_CREDENTIALS_USR}/${IMAGE}:${ID}"
        //             sh "docker push ${DOCKERHUB_CREDENTIALS_USR}/${IMAGE}:${ID}"
        //         }
                
        //     }
        // }

        stage('SSH Agent') {
            steps {
                sshagent(credentials: ['vagrant1']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no vagrant@192.168.56.10 "echo hello"
                    '''
                }
            }
        }

        stage('Backup Database') {
            steps {
                sshagent(credentials: ['vagrant1']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no vagrant@192.168.56.10
                    '''
                    script {

                        withCredentials([usernamePassword(credentialsId: 'postgres', usernameVariable: '${PSQL_CREDENTIALS_USR}', passwordVariable: '${PSQL_CREDENTAILS_PSW}')]) {
                            def backupCommand="PGPASSWORD=\${PSQL_CREDENTIALS_PSW} pg_dump -h 192.168.56.10 -U ${PSQL_CREDENTIALS_USR} ${DATABASE} > backup.sql"
                            sh backupCommand
                            sh 'gzip backup.sql'
                            archiveArtifacts artifacts: 'backup.sql.gz', fingerprint: true
                        }
                    }
                }
            }
        }

        // stage('Deployment') {
        //     agent {
        //         label 'odoo1'
        //     }
        //     steps {
        //         sh '''
        //             if ! docker network ls | grep -q "odoo"; then
        //                 docker network create -d bridge odoo
        //             else
        //                 echo "No need to create!"
        //             fi
        //         '''
        //         script {
        //             def blue_srv=sh(script: 'docker ps --format "{{.Names}}" --filter "name=odoo"', returnStdout: true).trim()
                    
        //             def green_srv = (blue_srv == 'blue') ? 'green' : 'blue'
                    
        //             sh "docker run --name ${green_srv} -v /home/vagrant/server/Odoo:/home/odoo/.local/share/Odoo -h ${green_srv} -d --network=odoo ${DOCKERHUB_CREDENTIALS_USR}/odoo:${ID}"
        //             sh "sleep 10"

        //             def result=sh(script: "docker exec ${green_srv} curl -I localhost:8069/web/database/selector", returnStdout: true).trim()
                    
        //             def http_code = result.substring(9, 12)
                    
        //             if (http_code == "200"){
                        
        //                 def blue_img=sh(script: "docker inspect --format='{{.Image}}' ${blue_srv}", returnStdout: true).trim()

        //                 sh "mv /home/vagrant/proxy/${blue_srv}.conf /home/vagrant/proxy/${blue_srv}.conf.template"
                        
        //                 sh "mv /home/vagrant/proxy/${green_srv}.conf.template /home/vagrant/proxy/${green_srv}.conf"

        //                 sh "rm /etc/nginx/conf.d/blue_srv.conf"
        //                 sh "ln -s /home/vagrant/proxy/green_srv.conf /etc/nginx/conf.d/"
        //                 sh "sudo service nginx reload"
                        
        //                 sh "docker restart nginx"
        //                 sh "sleep 10"
        //                 sh "docker stop ${blue_srv}"
        //                 sh "docker rm -f ${blue_srv}"
        //                 sh "docker rmi -f ${blue_img}"
        //             }
                    
        //             else {
        //                 sh "docker stop ${green_srv}"
        //                 sh "docker rm -f ${green_srv}"
        //                 sh "docker rmi -f ${DOCKERHUB_CREDENTIALS_USR}/${IMAGE}:${ID}"
        //             }
        //         }
        //     }
        // }
    }
}
