pipeline {
    agent any

    environment {
        PYTHON_CMD = 'python3'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code from SCM...'
                checkout scm
            }
        }

        stage('Build & File Verification') {
            steps {
                echo 'Verifying repository structure and index.html existence...'
                script {
                    if (isUnix()) {
                        sh '''
                            echo "Checking for index.html on Linux/macOS agent..."
                            if [ ! -f "index.html" ]; then
                                echo "ERROR: index.html not found!"
                                exit 1
                            fi
                            echo "SUCCESS: index.html is present."
                        '''
                    } else {
                        bat '''
                            @echo off
                            echo Checking for index.html on Windows agent...
                            if not exist index.html (
                                echo ERROR: index.html not found!
                                exit /b 1
                            )
                            echo SUCCESS: index.html is present.
                        '''
                    }
                }
            }
        }

        stage('Automated HTML Element Tests') {
            steps {
                echo 'Executing unit test suite to validate required HTML form elements...'
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m unittest discover -s tests -p "test_*.py" -v || python -m unittest discover -s tests -p "test_*.py" -v
                        '''
                    } else {
                        bat '''
                            python -m unittest discover -s tests -p "test_*.py" -v
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution complete.'
        }
        success {
            echo 'SUCCESS: All HTML element tests passed successfully!'
        }
        failure {
            echo 'FAILURE: HTML tests failed or required elements/files are missing.'
        }
    }
}
