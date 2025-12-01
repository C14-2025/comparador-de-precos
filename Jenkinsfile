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
                echo 'Preparando artefato da aplicação'
                sh '''
                    . ${VENV_PATH}/bin/activate
                    
                    # Instala dependências novamente (garante empacotamento completo)
                    if [ -f "requirements.txt" ]; then
                        pip install -r requirements.txt
                    fi
                    
                    # Collectstatic para Django (se existir)
                    if [ -f "manage.py" ]; then
                        python manage.py collectstatic --noinput || true
                    fi
                    
                    # Cria arquivo de versão
                    echo "Build: ${BUILD_NUMBER}" > version.txt
                    echo "Branch: ${GIT_BRANCH}" >> version.txt
                    echo "Commit: ${GIT_COMMIT}" >> version.txt
                    echo "Data: $(date)" >> version.txt
                    
                    # Freeze de dependências
                    pip freeze > requirements-freeze.txt
                    
                    mkdir -p dist
                    
                    # Limpa arquivos temporários
                    find . -name "*.pyc" -delete
                    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
                    
                    # Cria o ZIP do projeto
                    zip -r "dist/comparador-precos-${BUILD_NUMBER}.zip" . \
                        -x ".git/**" \
                        -x "${VENV_PATH}/**" \
                        -x "env/**" \
                        -x "venv/**" \
                        -x "dist/**" \
                        -x "test/**" \
                        -x "*.log" \
                        -x "*.sqlite3" \
                        -x ".pytest_cache/**" \
                        -x "htmlcov/**" \
                        -x ".coverage" \
                        -x "reports/**" \
                        -x ".env*" \
                        -x ".DS_Store"
                    
                    echo "Artefato criado: dist/comparador-precos-${BUILD_NUMBER}.zip"
                    ls -lh dist/
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/index.html'
            archiveArtifacts artifacts: 'dist/**/*'
        }
    }
}
