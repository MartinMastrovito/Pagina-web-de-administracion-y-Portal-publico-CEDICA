from core.board.issue import Issue
from src.core.database import db

def list_issues():
    issues = issue.query.all()

    return issues

def create_issue(**kwargs):
    issue = Issue(**kwargs)
    db.session.add(issue)
    db.session.commit()

    return issue