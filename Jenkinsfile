pipeline {
    agent any

  parameters {
        string(name: 'PR_URL', defaultValue: 'https://github.com/RameshKrishnanNaraKrish/react-project-webapp/pull/7', description: 'URL of the Pull Request (e.g., https://github.com/owner/repo/pull/123)')
    }

    environment {
        GITHUB_API_URL = 'https://api.github.com/repos'
        GITHUB_TOKEN = credentials('github')  // Use Jenkins credentials for GitHub token
    }

    stages {
      stage('Validate and Extract PR Details') {
            steps {
                script {
                    if (!params.PR_URL) {
                        error "PR_URL parameter is required!"
                    }

                    def matcher = params.PR_URL =~ /https:\/\/github\.com\/([^\/]+)\/([^\/]+)\/pull\/(\d+)/
                    if (!matcher.matches()) {
                        error "Invalid PR URL format. Expected format: https://github.com/owner/repo/pull/123"
                    }

                    env.OWNER = matcher[0][1]
                    env.REPO = matcher[0][2]
                    env.PR_ID = matcher[0][3]

                    echo "Extracted Owner: ${env.OWNER}"
                    echo "Extracted Repo: ${env.REPO}"
                    echo "Extracted PR ID: ${env.PR_ID}"
                }
            }
        }

        stage('Checkout Repository') {
            steps {
                git branch: 'main', url: "https://github.com/${env.OWNER}/${env.REPO}.git"
            }
        }

        stage('Revert PR') {
            steps {
                script {
                    // Checkout the repository
                    checkout scm

                    // Set up Python environment (assuming Python and pip are available)
                    //sh 'python3 -m venv venv'
                    //sh 'source venv/bin/activate && pip install requests'

                    echo "OWNER: ${env.OWNER}"
                    echo "REPO: ${env.REPO}"
                    echo "PR_ID: ${env.PR_ID}"

                    // Run the Python script to revert the PR
                    sh """
                        python3 revert_pr.py ${env.OWNER} ${env.REPO} ${env.PR_ID} ${env.GITHUB_TOKEN}
                    """
                }
            }
        }
    }
}
