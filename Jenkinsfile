node {
    stage ("Setup") {
        cleanWs()
        checkout scm
    }

    def environment = docker.build("infinity-sw")
    sh "mkdir jenkins_output"

    try {
        environment.inside('-v $WORKSPACE/jenkins_output:/home/ian/jenkins') {
            stage ("Build") {
                // do stuff here
            }

            stage ("Test") {
                try {
                    sh 'echo "Testing..."'
                    sh 'whoami'
                    sh """
                    #!/bin/bash
                    python3 -m pytest --junitxml=/home/jenkins/test_report.xml  
                    """
                } finally {
                    sh 'echo "Done testing..."'
                    junit('jenkins_output/test_report.xml')
                }

            }
        }
        
    } finally {
        sh 'echo "Cleaning up..."'
        deleteDir()
    }

}   