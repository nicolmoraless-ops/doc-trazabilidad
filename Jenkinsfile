// Pipeline de CI/CD con documentación y trazabilidad (Actividad 3.4.2)

// Deja la alerta en la consola y la envía por correo. Si el servidor SMTP
// no está configurado, el envío falla sin cambiar el resultado del build.
def notificar(String asunto, String cuerpo) {
    echo "ALERTA >> ${asunto}\n${cuerpo}"
    try {
        mail to: env.NOTIFY_EMAIL, subject: asunto, body: cuerpo
    } catch (err) {
        echo "No se pudo enviar el correo (configura SMTP en Administrar Jenkins > System): ${err.message}"
    }
}

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
                    // Se trabaja en una carpeta temporal aparte: el workspace no se toca
                    // y la rama docs conserva el historial de cada versión de la doc.
                    sh '''
                        SRC_COMMIT=$(git rev-parse --short HEAD)
                        REPO=$(git config --get remote.origin.url | sed -e 's#^https://##' -e 's#^.*@##')
                        URL="https://${GIT_USER}:${GIT_TOKEN}@${REPO}"
                        TMP=$(mktemp -d)
                        trap 'rm -rf "$TMP"' EXIT

                        if ! git clone -q --depth 50 --branch "$DOCS_BRANCH" "$URL" "$TMP" 2>/dev/null; then
                            git init -q "$TMP"
                            git -C "$TMP" checkout -q -b "$DOCS_BRANCH"
                        fi
                        find "$TMP" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
                        cp -r docs/. "$TMP/"

                        cd "$TMP"
                        git config user.name  "Jenkins CI"
                        git config user.email "jenkins@localhost"
                        git add -A
                        git commit -q -m "docs: build #${BUILD_NUMBER} desde ${SRC_COMMIT}" || echo "Sin cambios en la documentación"
                        git push -q "$URL" "HEAD:refs/heads/${DOCS_BRANCH}"
                        git log --oneline -3
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
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
            notificar("UNSTABLE: ${env.JOB_NAME} #${env.BUILD_NUMBER} - problemas de documentación",
                      "Revisa docs/doc-report.md en ${env.BUILD_URL}artifact/docs/doc-report.md")
        }
        failure {
            notificar("FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                      "El pipeline falló. Consola: ${env.BUILD_URL}console")
        }
    }
}
