// Library imports
@Library('jenkins-opta-groovy-lib') _
// Settings

def aws_account_id = ""
def my_sql_host = ""
def my_sql_redactions_host = ""
def my_sql_redactions_pwd = ""
def image_name = "activity-logger"
def functionName = "activity-logger"
def commitID = ""
def bucket_name = ""


def deployableBranches = [
  master: [
    account: '682426849792',
    my_sql_redactions_host: 'db-insurancereferrals-mysql-0.c0klaiigo90s.ca-central-1.rds.amazonaws.com',
    my_sql_redactions_pwd: 'ovSykvUbECUxnVvWu9Pz',
    my_sql_host: 'mysql.prodmsenv-k8s.optaservice.com',
    bucket_name: "opta-applications-prodmsenv"
  ],
  ct: [
    account: '532534578912',
    my_sql_redactions_host: 'db-insurancereferrals-mysql-0.clahquy1hpgw.ca-central-1.rds.amazonaws.com',
    my_sql_redactions_pwd: 'HJXCSztZxK1WJTDOi2Yo',
    my_sql_host: 'mysql.clienttestmsenv-k8s.optaservice.com',
    bucket_name: "opta-applications-clienttestmsenv"
  ],
  uat: [
    account: '076248129044',
    my_sql_redactions_host: 'db-insurancereferrals-mysql-0.cdeg3o0gldgw.ca-central-1.rds.amazonaws.com',
    my_sql_redactions_pwd: 'HTLxoWuOCZcc04idz2WI',
    my_sql_host: 'mysql.uatmsenv-k8s.optaservice.com',
    bucket_name: "opta-applications-uatmsenv"
  ],
  test: [
    account: '526376821361',
    my_sql_redactions_host: 'db-insurancereferrals-mysql-0.c3e2pqe9k29h.ca-central-1.rds.amazonaws.com',
    my_sql_redactions_pwd: 'nrq0aFaUfKBcLqwaCvNj',
    my_sql_host: 'mysql.testmsenv-k8s.optaservice.com',
    bucket_name: "opta-applications-testmsenv"
  ],
  dev: [
    account: '293927255465',
    my_sql_redactions_host: 'db-insurancereferrals-mysql-0.c0klaiigo90s.ca-central-1.rds.amazonaws.com',
    my_sql_redactions_pwd: 'NnVp1vZ4hjklJkMVpeQe',
    my_sql_host: 'mysql.devmsenv-k8s.optaservice.com',
    bucket_name: "opta-applications-devmsenv"
  ]
]

pipeline {
    agent any
    triggers {
        pollSCM ''
        bitbucketPush()
    }
    stages {
        stage("Setup Pipeline") {
            steps {
                script {
                    echo "Deploying to echo ${env.BRANCH_NAME}"
                    aws_account_id = deployableBranches[env.BRANCH_NAME].account
                    my_sql_host = deployableBranches[env.BRANCH_NAME].my_sql_host
                    my_sql_redactions_host = deployableBranches[env.BRANCH_NAME].my_sql_redactions_host
                    my_sql_redactions_pwd = deployableBranches[env.BRANCH_NAME].my_sql_redactions_pwd
                    bucket_name = deployableBranches[env.BRANCH_NAME].bucket_name
                    commitID = getGitCommitID()
                    echo "CommitID -> ${commitID}"
                    loginToECR()
                }
            }
        }
         stage('Deploy To ECR') {
            steps {
                script {
                    sh "./deploy.sh ${image_name} ${aws_account_id} ${my_sql_host} ${my_sql_redactions_host} ${my_sql_redactions_pwd} ${bucket_name}"
                }
            }
        }
        stage('Update Lambda Code') {
            steps {
                withAWS(region: 'ca-central-1', role: 'K8sClusterLifeAdm', roleAccount: "${aws_account_id}") {
                    script {
                        sh "aws lambda update-function-code --function-name ${functionName} --image-uri ${aws_account_id}.dkr.ecr.ca-central-1.amazonaws.com/${image_name}:${commitID}"
                    }
                }
            }
        }
    }
    post {
        failure {
            script {
                notifications.send currentBuild.result
            }
        }
    }
}

void loginToECR() {
    sh "eval \$(aws ecr get-login --no-include-email --region ca-central-1)"
}
String getGitCommitID() {
    return sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim() as String
}
