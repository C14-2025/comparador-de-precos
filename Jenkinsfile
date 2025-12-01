pipeline{
    agent any
    environment {
        VENV_PATH = '.venv'
        
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
                echo 'Ativando o ambiente virtual'
                sh ".${VENV_PATH}/bin/activate"
                echo 'Executando os testes'
                sh '''
                python manage.py test produto.tests --verbosity=2
                '''
                echo 'Testes concluidos!'
            }
        }
    }
}