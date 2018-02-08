pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'Setup virtual environment'
        script {
          sh """
          PATH=$WORKSPACE/venv/bin:/usr/local/bin:$PATH
          if [ ! -d "venv" ]; then
          virtualenv venv
          fi
          . venv/bin/activate
          pip install -r requirements.txt
          """
		}
		echo 'Install requirements.txt'
		script {
		  sh """
		  . venv/bin/activate
		  pip install -r requirements.txt
		  """
		}
		echo 'Migrate database'
        script {
          sh """
          . venv/bin/activate
		  python manage.py migrate --noinput
		  """
	    }
		echo 'Collect static'
        script {
          sh """
          . venv/bin/activate
          python manage.py collectstatic --noinput
		  """
	    }
      }
    }
	stage('Linting') {
	  steps {
	    echo 'Running linting'
	  }
	}
    stage('Test') {
      steps {
        echo 'This is the Testing Stage'
		script {
		  sh """
		  . venv/bin/activate
		  python coverage manage.py test
		  """
		}
      }
    }
    stage('Deploy') {
      steps {
        echo 'This is the Deploy Stage'
      }
    }
  }
}