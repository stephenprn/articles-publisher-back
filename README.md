# Skeleton-back
Skeleton universal project (back-end) including:
- OAuth2 authentication

## Commands
- Create venv
```
python3 -m venv venv
```
- Install dependencies
```
pip install -r requirements.txt
```
- Store dependencies in `requirements.txt`
```
python -m pip freeze > requirements.txt
```
- Activate venv
```
source venv/bin/activate
```

## Project structure

### Models

Regroup all models corresponding to the SQL tables (user,...).

### Routes

All clusters of routes of the application.

### Services

Regroup main functions of the application usually called by the blueprints.

### Shared

Shared variables and data accessible from different parts of the application.