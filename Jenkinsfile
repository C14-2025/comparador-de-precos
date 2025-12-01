pipeline {
    agent any

    environment {
        VENV_PATH = '.venv'
        REPORTS_DIR = 'reports'

        // Env do Django
        SECRET_KEY = 'django-insecure-test-key-for-ci-only-do-not-use-in-production'
        DEBUG = 'False'
        ALLOWED_HOSTS = 'localhost,127.0.0.1'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Clonando o repositório :)'
                echo "Branch: ${env.GIT_BRANCH}"
                echo "Pipeline ativada por: ${currentBuild.getBuildCauses()[0].username ?: 'Github Webhook'}"
                checkout scm
            }
        }

        stage('Criando o ambiente virtual') {
            steps {
                echo 'Criando o ambiente virtual (.venv)'
                sh '''
                    rm -rf ${VENV_PATH}
                    python3 -m venv ${VENV_PATH}

                    . ${VENV_PATH}/bin/activate
                    pip install --upgrade pip setuptools wheel
                    echo "Ambiente virtual criado com sucesso!"
                '''
            }
        }

        stage('Instalando as dependencias') {
            steps {
                echo 'Instalando as dependencias do requirements.txt'
                sh '''
                    . ${VENV_PATH}/bin/activate
                    pip install -r requirements.txt

                    echo "Dependencias instaladas:"
                    pip list
                '''
            }
        }

        stage('Testando') {
            steps {
                echo 'Executando os testes'
                sh '''
                    . ${VENV_PATH}/bin/activate
                    python3 manage.py 
                    
                    coverage run manage.py test
                    coverage html -d ${REPORTS_DIR}
                '''
                echo 'Testes concluidos!'
            }
        }

        stage('Gerando artefato da build') {
            steps {
                sh '''
                    echo "Criando arquivo TAR da aplicação..."

                    ARTIFACT="comparador-precos-$BUILD_NUMBER.tar.gz"

                    tar -czf $ARTIFACT . \
                        --exclude=.venv \
                        --exclude=venv \
                        --exclude=env \
                        --exclude=*.pyc \
                        --exclude=__pycache__ \
                        --exclude=.git \
                        --exclude=htmlcov \
                        --exclude=reports \
                        --exclude=.pytest_cache \
                        --exclude=node_modules

                    echo "✅ Artefato criado: $ARTIFACT"
                    ls -lh $ARTIFACT
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/index.html'
            archiveArtifacts artifacts: 'comparador-precos-${BUILD_NUMER}.zip'
        }
    }
}
