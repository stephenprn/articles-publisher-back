#!/bin/sh

export FLASK_ENV=development

# Avoid https checking flask oauth2
export AUTHLIB_INSECURE_TRANSPORT=true

# sqlaclhemy settings
export SQLALCHEMY_DATABASE_URI=sqlite:///application.db

# jwt
export SECRET_KEY=super-secret
export JWT_AUTH_URL_RULE=/auth/login
export JWT_AUTH_USERNAME_KEY=email

echo "env variables config done"