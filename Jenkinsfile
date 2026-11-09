// Pipeline de CI/CD con documentación y trazabilidad (Actividad 3.4.2)
pipeline {
    agent any

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
    }

    triggers {
        pollSCM('H/5 * * * *')   // revisa el repositorio cada 5 minutos
    }

    environment {
        VENV         = "${WORKSPACE}/venv"
        DOC_MIN      = '80'                        // % mínimo de docstrings
        GIT_CREDS    = 'github-creds'              // ID de credencial en Jenkins
        DOCS_BRANCH  = 'docs'                      // rama donde se versiona la doc
        NOTIFY_EMAIL = 'tu_correo@duocuc.cl'       // cambiar por el tuyo
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv "$VENV"
                    "$VENV/bin/pip" install --quiet --upgrade pip
                    "$VENV/bin/pip" install --quiet -r requirements.txt
                    "$VENV/bin/python" -m compileall -q -x 'venv|docs' .
                '''
            }
        }

        stage('Test') {
            steps {
                sh '"$VENV/bin/python" -m pytest -v --junitxml=reports/junit.xml tests/'
            }
            post {
                always { junit 'reports/junit.xml' }
            }
        }

        stage('Generate Documentation') {
            steps {
                sh '''
                    rm -rf docs && mkdir -p docs
                    doxygen Doxyfile
                '''
                // Si faltan docstrings o Doxygen deja advertencias, el build queda UNSTABLE
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh '"$VENV/bin/python" scripts/doc_report.py "$DOC_MIN" docs/doc-report.md'
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'docs/**', allowEmptyArchive: true, fingerprint: true
                }
            }
        }

        stage('Version Control') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.GIT_CREDS,
                                                  usernameVariable: 'GIT_USER',
                                                  passwordVariable: 'GIT_TOKEN')]) {
                    sh '''
                        SRC_COMMIT=$(git rev-parse --short HEAD)
                        REPO=$(git config --get remote.origin.url | sed -e 's#^https://##' -e 's#^.*@##')
                        TMP=$(mktemp -d)
                        cp -r docs/. "$TMP/"

                        git config user.name  "Jenkins CI"
                        git config user.email "jenkins@localhost"
                        git checkout --orphan "$DOCS_BRANCH-tmp"
                        git rm -rf --cached . > /dev/null
                        find . -mindepth 1 -maxdepth 1 ! -name .git ! -name venv -exec rm -rf {} +
                        cp -r "$TMP/." .
                        git add -A
                        git commit -m "docs: build #${BUILD_NUMBER} desde ${SRC_COMMIT}"
                        git push -f "https://${GIT_USER}:${GIT_TOKEN}@${REPO}" "HEAD:refs/heads/${DOCS_BRANCH}"
                        rm -rf "$TMP"
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                checkout scm   // volver al código después del stage anterior
                sh '''
                    "$VENV/bin/pip" install --quiet -r requirements.txt
                    if [ -f /tmp/flask-app.pid ]; then kill $(cat /tmp/flask-app.pid) 2>/dev/null || true; fi
                    JENKINS_NODE_COOKIE=dontKillMe APP_HOST=0.0.0.0 APP_PORT=5000 \
                        nohup "$VENV/bin/python" app.py > /tmp/flask-app.log 2>&1 &
                    echo $! > /tmp/flask-app.pid
                    sleep 3
                    curl -fsS http://localhost:5000/health
                    curl -fsS "http://localhost:5000/hello?name=Jenkins"
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline OK. Documentación en la rama '${DOCS_BRANCH}' y en los artefactos del build."
        }
        unstable {
            mail to: env.NOTIFY_EMAIL,
                 subject: "UNSTABLE: ${env.JOB_NAME} #${env.BUILD_NUMBER} - problemas de documentación",
                 body: "Revisa docs/doc-report.md en ${env.BUILD_URL}artifact/docs/doc-report.md"
        }
        failure {
            mail to: env.NOTIFY_EMAIL,
                 subject: "FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "El pipeline falló. Consola: ${env.BUILD_URL}console"
        }
    }
}
