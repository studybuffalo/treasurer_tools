pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }
  stages {
    stage('Build') {
      steps {
        echo 'Setup virtual environment'
        script {
          sh 'pipenv install --dev'
        }
        echo 'Migrate database'
        script {
          sh 'pipenv run python manage.py migrate --noinput'
        }
        echo 'Collect static'
        script {
          sh 'pipenv run python manage.py collectstatic --noinput'
        }
      }
    }
    stage('Test') {
      steps {
        echo 'This is the Testing Stage'
        script {
          sh 'pipenv run python manage.py jenkins --enable-coverage --settings=config.settings.test'
        }
        /*
        script {
          sh """
          . venv/bin/activate
           --rcfile=.pylintrc --output-format=parseable --reports=no treasurer_tools > reports/pylint.txt || exit 0
          """
        }
        cobertura(autoUpdateHealth: true, autoUpdateStability: true, coberturaReportFile: 'reports/coverage.xml')
        junit 'reports/junit.xml'
        step([
          $class: 'WarningsPublisher',
          parserConfigurations: [[
            parserName: 'PyLint',
            pattern: 'reports/pylint.txt'
          ]],
          unstableTotalAll: '0',
          usePreviousBuildAsReference: true
        ])
      }
      */
    }
    stage('Deploy') {
      steps {
        echo 'This is the Deploy Stage'
        sshPublisher(
          failOnError: true,
          publishers: [
            sshPublisherDesc(
              configName: 'cshp_ab_expenses',
              transfers: [sshTransfer(
                excludes: '',
                execCommand: '''source ~/Env/expenses/bin/activate
                  cd treasurer_tools
                  git pull
                  pip install -r requirements.txt
                  python manage.py collectstatic --noinput
                  sudo /bin/systemctl restart uwsgi || exit 0''',
                execTimeout: 120000,
                flatten: false,
                makeEmptyDirs: false,
                noDefaultExcludes: false,
                patternSeparator: '[, ]+',
                remoteDirectory: '',
                remoteDirectorySDF: false,
                removePrefix: '',
                sourceFiles: ''
              )],
              usePromotionTimestamp: false,
              useWorkspaceInPromotion: false,
              verbose: false
            )
          ]
        )
      }
    }
  }
}
