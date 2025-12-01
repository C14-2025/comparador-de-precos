pipeline{
    agent any
    environment {
        VENV_PATH = '.venv'
        REPORTS_DIR = 'reports'
        
        // Env do Django
        SECRET_KEY = 'django-insecure-test-key-for-ci-only-do-not-use-in-production'
        DEBUG = 'False'
        ALLOWED_HOSTS = 'localhost,127.0.0.1'
    }    
    stages{
        stage('Checkout'){
            steps{
                echo 'Clonando o repositório :)'
                echo "Branch: ${env.GIT_BRANCH}"
                echo "Pipeline ativada por: ${currentBuild.getBuildCauses()[0].username ?: 'Github Webhook'}"
                checkout scm
            }
        }

        stage('Criando o ambiente virtual'){
            steps{
                echo 'Criando o ambiente virtual (.venv)'
                sh '''
                    # Deixa o ambiente limpo caso já exista uma venv anteriormente
                    rm -rf ${VENV_PATH}

                    # Criando a venv
                    python3 -m venv ${VENV_PATH}

                    # Ativando e atualizando o pip
                    . ${VENV_PATH}/bin/activate
                    pip install --upgrade pip setuptools wheel
                    echo " Ambiente virtual criado com sucesso! "

                '''
            }
        }

        stage('Instalando as dependencias'){
            steps{
                echo 'Instalando as dependencias do requirements.txt'
                sh '''
                . ${VENV_PATH}/bin/activate

                # instalando as dependencias :D
                pip install -r requirements.txt

                echo "dependencias instaladas:"
                pip list
                '''
            }
        }

        stage('Testando'){
            steps{
                echo 'Executando os testes'
                sh '''
                . ${VENV_PATH}/bin/activate
                coverage run manage.py test
                coverage html -d ${REPORTS_DIR}

                '''
                echo 'Testes concluidos!'
            }
        }

        stage('Gerando artefato da build'){
            steps{
                echo 'Preparando artefatos'
                sh '''
                    . ${VENV_PATH}/bin/activate
                    
                    pip install build wheel setuptools

                    python manage.py collectstatic --noinput || true

                    #
                    python -m build --outdir dist/
                    
                    # arquivo bonitinho da versao
                    echo "Build: ${BUILD_NUMBER}" > version.txt
                    echo "Branch: ${GIT_BRANCH}" >> version.txt
                    echo "Commit: ${GIT_COMMIT}" >> version.txt
                    echo "Data: $(date)" >> version.txt
                    
                    #criando a lista de dependencias
                    pip freeze > requirements-freeze.txt
                    
                    # até onde eu pesquisei artefato python é um zip então boa
                    echo "Criando arquivo ZIP da aplicação..."
                    zip -r dist/comparador-precos-${BUILD_NUMBER}.zip . \
                        -x "*.venv/*" \
                        -x "*venv/*" \
                        -x "*env/*" \
                        -x "*.pyc" \
                        -x "*__pycache__/*" \
                        -x "*.git/*" \
                        -x "*htmlcov/*" \
                        -x "*reports/*" \
                        -x "*.pytest_cache/*" \
                        -x "*dist/*" || true
                    
                    echo "Artefato pronto!"
                    ls -lh dist/
                '''
        }
    }
}

post{
    always{
        archiveArtifacts: 'reports/index.html'

        archiveArtifacts: 'dist/**/*'
    }
}