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
            steps{
                echo 'Preparando artefatos para distribuição'
                sh '''
                    . ${VENV_PATH}/bin/activate
                    
                    # Coletar arquivos estáticos do Django
                    python manage.py collectstatic --noinput || true
                    
                    # Criar arquivo de versão
                    echo "Build: ${BUILD_NUMBER}" > version.txt
                    echo "Branch: ${GIT_BRANCH}" >> version.txt
                    echo "Commit: ${GIT_COMMIT}" >> version.txt
                    echo "Data: $(date)" >> version.txt
                    
                    # Criar arquivo requirements-freeze.txt (versões exatas)
                    pip freeze > requirements-freeze.txt
                    
                    # Criar ZIP da aplicação
                    echo "Criando arquivo ZIP da aplicação..."
                    apt-get update && apt-get install -y zip
                    zip -r comparador-precos-${BUILD_NUMBER}.zip . \
                        -x "*.venv/*" \
                        -x "*venv/*" \
                        -x "*env/*" \
                        -x "*.pyc" \
                        -x "*__pycache__/*" \
                        -x "*.git/*" \
                        -x "*htmlcov/*" \
                        -x "*reports/*" \
                        -x "*.pytest_cache/*" \
                        -x "*node_modules/*" || true
                    
                    echo "✅ Artefatos preparados!"
                    ls -lh comparador-precos-${BUILD_NUMBER}.zip
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
