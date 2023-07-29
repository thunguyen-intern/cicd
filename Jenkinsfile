pipeline {
    agent {
        label 'odoo1'
    }
    
    environment {
        DOCKER_COMPOSE = 'docker-compose.yml'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        DOCKER_IMAGE_NAME = 'odoo_15'
        IMAGE = 'odoo'
        FAILED_STAGE = ''
        PSQL_CREDENTIALS = credentials('postgres')
        DATABASE = 'postgres'
    }

    stages {
        stage('Triggered By Github Commits') {
            steps {
                cleanWs()
                checkout scm
                sh "echo 'Cleaned Up Workspace For Project'"
                script {
                    // sh "sudo apt-get update"
                    // sh "sudo apt-get install -y python3-pip"
                    sh "pip3 install -r agent_requirements.txt"
                }
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

        stage('Generate Odoo Commands') {
            steps {
                echo "Generate Odoo Commands"
                script {
                    sh """
                        python3 unit_test.py > ./unit_test/test_utils.sh
                        chmod +x ./unit_test/test_utils.sh
                        python3 upgrade.py > ./unit_test/upgrade.sh
                        chmod +x ./unit_test/upgrade.sh
                    """
                }
            }
        }

        stage('Login Dockerhub') {
            steps {
                script {
                    // Log into Docker registry
                    sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                echo "Run Docker Compose"
                script {
                    sh '''
                        if [ "$(docker ps -aq)" ]; then
                            docker stop $(docker ps -aq)
                            docker rm $(docker ps -aq)
                        else
                            echo "No running containers to stop"
                        fi
                    '''
                    // def commitId = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    // def previousCommitId = sh(script: 'git rev-parse HEAD~1', returnStdout: true).trim()
                    
                    // def changes = sh(script: "git diff --name-only ${previousCommitId} ${commitId}", returnStdout: true).trim()
                    // if (changes.contains('Dockerfile')
                    //     || changes.contains('docker-compose.yml')
                    //     || changes.contains('odoo.conf')
                    //     || changes.contains('./nginx/')
                    //     ) {
                    //     sh 'docker compose build'
                    // }
                    // else {
                    //     echo "No Changes Detected"
                    // }
                    sh 'docker compose up -d'
                    sh 'docker ps'
                }
            }
        }

        stage('Odoo Unit Test') {
            steps {
                echo "Odoo Unit Test"
                script {
                    def result=sh(script: "docker exec ${DOCKER_IMAGE_NAME} /mnt/extras/test_utils.sh", returnStdout: true).trim()
                    def res = result[-1]
                    if (res == '0') {
                        echo "success"
                    }
                    else {
                        error("Unit Test Failed")
                    }
                }
            } 
        }

        stage('Backup Database & Odoo Upgrade Module') {
            steps {
                echo "Backup Database"
                script {
                    up_modules = ""
                    res=sh(script: "python3 upgrade_process.py", returnStdout: true).trim()
                    missing_modules = res.split('\n')[0].substring(8)
                    up_modules = res.split("\n")[1].substring(7)
                    echo "${missing_modules}"
                    echo "${up_modules}"
                }
                sshPublisher(
                    publishers: [
                        sshPublisherDesc(
                            configName: 'vagrant',
                            transfers: [
                                sshTransfer(
                                    cleanRemote: false,
                                    excludes: '',
                                    execCommand: 'chmod +x backup.sh && ./backup.sh && rm -f backup.sh',
                                    execTimeout: 120000,
                                    flatten: false,
                                    makeEmptyDirs: false,
                                    noDefaultExcludes: false,
                                    patternSeparator: '[, ]+',
                                    remoteDirectory: '',
                                    remoteDirectorySDF: false,
                                    removePrefix: '',
                                    sourceFiles: 'backup.sh'
                                )
                            ], 
                            usePromotionTimestamp: false,
                            useWorkspaceInPromotion: false,
                            verbose: false
                        )
                    ]
                )
                echo "Odoo Upgrade Module"
                script {
                    if (missing_modules.isEmpty()){
                        echo "No missing modules"
                    }
                    else {
                        sh "python3 notification.py approval ${branch} ${Author_ID} ${missing_modules} ${uId} ${env.BUILD_URL} ${ID}"
                        input "Do you want to continue and ignore missing modules?"
                    }
                    def result=sh(script: "docker exec ${DOCKER_IMAGE_NAME} /mnt/extras/upgrade.sh", returnStdout: true).trim()
                    def res = result[-1]
                    if (res == '0') {
                        echo "Upgrade module successfully"
                    }
                    else {
                        sshPublisher(
                            publishers: [
                                sshPublisherDesc(
                                    configName: 'vagrant',
                                    transfers: [
                                        sshTransfer(
                                            cleanRemote: false,
                                            excludes: '',
                                            execCommand: 'chmod +x recovery.sh && ./recovery.sh && rm -f recovery.sh',
                                            execTimeout: 120000,
                                            flatten: false,
                                            makeEmptyDirs: false,
                                            noDefaultExcludes: false,
                                            patternSeparator: '[, ]+',
                                            remoteDirectory: '',
                                            remoteDirectorySDF: false,
                                            removePrefix: '',
                                            sourceFiles: 'recovery.sh'
                                        )
                                    ],
                                    usePromotionTimestamp: false,
                                    useWorkspaceInPromotion: false,
                                    verbose: false
                                )
                            ]
                        )
                        error("Odoo upgrade failed")
                    }
                }
            }

            // post {
            //     always {
            //         sshPublisher(
            //             publishers: [
            //                 sshPublisherDesc(
            //                     configName: 'postgres',
            //                     transfers: [
            //                         sshTransfer(
            //                             cleanRemote: false,
            //                             excludes: '',
            //                             execCommand:
            //                             'cd backup_data && rm -f *',
            //                             execTimeout: 120000,
            //                             flatten: false,
            //                             makeEmptyDirs: false,
            //                             noDefaultExcludes: false,
            //                             patternSeparator: '[, ]+',
            //                             remoteDirectory: '',
            //                             remoteDirectorySDF: false,
            //                             removePrefix: '',
            //                             sourceFiles: ''
            //                         )
            //                     ],
            //                     usePromotionTimestamp: false,
            //                     useWorkspaceInPromotion: false, verbose: false
            //                 )
            //             ]
            //         )
            //     }
            //     failure {
            //         script {
            //             FAILED_STAGE = env.STAGE_NAME
            //         }
            //     }
            // }
        }

        stage('Push Image') {
            steps {
                echo "Push Image"
                script {
                    def img=sh(script: "docker inspect --format='{{.Image}}' '${DOCKER_IMAGE_NAME}'", returnStdout: true).trim()
                    sh "docker tag ${img} ${DOCKERHUB_CREDENTIALS_USR}/${IMAGE}:${ID}"
                    sh "docker push ${DOCKERHUB_CREDENTIALS_USR}/${IMAGE}:${ID}"
                }
                
            }
        }

        stage('Deployment') {
            steps {
                echo "Deployment"
                script {
                    def hosts = [
                        [host: 'tcp://192.168.56.11:2375', container: 'odoo1'],
                        [host: 'tcp://192.168.56.12:2375', container: 'odoo2'],
                        [host: 'tcp://192.168.56.13:2375', container: 'odoo3'],
                    ]
                    hosts.each { host ->
                        withEnv(["DOCKER_HOST=${host.host}"]) {
                            sh '''
                                if ! docker network ls | grep -q "odoo"; then
                                    docker network create -d bridge odoo
                                else
                                    echo "No need to create!"
                                fi
                            '''
                            def blue_srv=sh(script: "docker ps --format \"{{.Names}}\" --filter \"name=${host.container}\"", returnStdout: true).trim()
                            def green_srv = (blue_srv == 'blue') ? 'green' : 'blue'
                            sh "docker run --name ${green_srv} -v /home/vagrant/server/Odoo:/home/odoo/.local/share/Odoo -h ${green_srv} -d --network=odoo ${DOCKERHUB_CREDENTIALS_USR}/odoo:${ID}"
                            sh "sleep 10"

                            def result=sh(script: "docker exec ${green_srv} curl -I localhost:8069/web/database/selector", returnStdout: true).trim()                    
                            def http_code = result.substring(9, 12)
                            if (http_code == "200"){
                                def blue_img=sh(script: "docker inspect --format='{{.Image}}' ${blue_srv}", returnStdout: true).trim()
                                sh "mv /home/vagrant/proxy/${blue_srv}.conf /home/vagrant/proxy/${blue_srv}.conf.template"                        
                                sh "mv /home/vagrant/proxy/${green_srv}.conf.template /home/vagrant/proxy/${green_srv}.conf"
                            // sh "rm /etc/nginx/conf.d/${blue_srv}.conf"
                            // sh "ln -s /home/vagrant/proxy/${green_srv}.conf /etc/nginx/conf.d/"
                            // sh "sudo service nginx reload"
                                sh "docker restart nginx"
                                sh "sleep 10"
                                sh "docker stop ${blue_srv}"
                                sh "docker rm -f ${blue_srv}"
                                sh "docker rmi -f ${blue_img}"
                            }
                            else {
                                sh "docker stop ${green_srv}"
                                sh "docker rm -f ${green_srv}"
                                sh "docker rmi -f ${DOCKERHUB_CREDENTIALS_USR}/${IMAGE}:${ID}"
                            }
                        }
                    }
                }
                
            }
        }
    }
}
