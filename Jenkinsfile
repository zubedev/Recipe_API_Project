pipeline {
    agent { dockerfile true }

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                docker-compose build
                docker-compose up -d
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                docker-compose run app sh -c "python manaype.py test && flake8"
            }
        }
        // stage('Deploy') {
        //     steps {
        //         echo 'Deploying....'
        //     }
        // }
    }

    post {
        always {
            docker-compose down
        }
    }
}