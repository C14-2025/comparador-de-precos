pipeline{
    agent any

    environment{
        PYTHON-VERSION = '3.12.3'
    }

    stages{
        stage('Checkout'){
            steps{
                echo 'Clonando o repositório :)'
                checkout scm
            }
        }
    }
}