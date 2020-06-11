pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                echo '$PWD'
                sh 'ls -al'
                sh "docker-compose build"
                sh "docker-compose up -d"
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                echo '$PWD'
                sh 'ls -al'
                sh 'docker-compose run app sh -c "python manage.py test && flake8"'
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
            sh "docker-compose down"
        }
    }
}