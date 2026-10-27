# Electronic Voting & Registration System — Django REST Backend

An academic backend for managing electronic voting workflows, developed in **Python and Django** as a graduation project at **ESCOM, Instituto Politécnico Nacional (IPN)**.

The project implements HTTP endpoints for voter registration, candidate management, election sessions, authentication and access-code workflows, vote submission, and results retrieval. It also contains JWT, AES, and Paillier-related voting/result-processing logic.

> **Portfolio / academic project.** The repository is not presented as a production-ready or independently security-audited electronic voting platform.

## Technology stack

- **Backend:** Python 3.8.6, Django 3.1.3 (versions documented in the original project README)
- **API tooling:** Django REST Framework serializers and JSON responses
- **Database:** Django ORM; the original setup documents **MySQL 5.7.32**. The database engine is configurable via environment settings.
- **Authentication and cryptography:** JWT utility module, SHA-256 hashing, AES encryption/decryption utilities, and Paillier-related tallying logic
- **Supporting services:** email templates for passwords and access codes; CORS configuration
- **Testing:** Django test modules are included for login, voters, candidates, election sessions, and voting. Test execution has **not** been verified in this review.

## What the backend does

1. **Voters:** creates, reads, updates, and deletes voter records; includes voter-type handling and email-related registration logic.
2. **Candidates:** creates, retrieves, updates, and deletes candidate records.
3. **Election sessions (`jornadas`):** creates and manages election sessions and their candidate assignments.
4. **Authentication:** handles login, password-reset, and access-code endpoints.
5. **Voting and results:** processes vote-related requests, validates voting-related inputs and tokens, and exposes result-related operations. The code includes a `getResultadosByPaillier` calculation path.

## API routes

These routes are directly declared in `Backend/urls.py` and the corresponding application `urls.py` modules. Request bodies, response schemas, and authorization requirements should be checked in the views before integration.

| Path | Declared view | Methods observed in view |
| --- | --- | --- |
| `/candidatos/` | `getCandidato` | GET, POST |
| `/candidatos/<id>/` | `editCandidato` | PUT, DELETE |
| `/votantes/` | `getVotante` | GET, POST |
| `/votantes/<id>/` | `editVotante` | PUT, DELETE |
| `/jornadas/` | `getJornada` | GET, POST |
| `/jornadas/<id>/` | `editJornada` | GET, PUT, DELETE |
| `/login/` | `getLogin` | POST |
| `/login/restart-password/` | `restartPassword` | PUT |
| `/login/access-code/` | `accessCode` | POST |
| `/votaciones/<id>/` | `getVotaciones` | GET, POST |
| `/votaciones/resultados/<id>/` | `getResultados` | GET, POST |
| `/admin/` | Django admin | Django-managed |

The method list is based on conditional branches in the source; it is **not** a verified OpenAPI contract.

## Repository structure

```text
App/
  Administrador/    # Administrator model
  Candidato/        # Candidate models, serializers, views, tests
  Jornada/          # Election sessions, assignments, results
  Login/            # Login, access-code and password workflows
  Votaciones/       # Voting and results processing
  Votante/          # Voter records and registration workflows
Backend/            # Django configuration, URLs, ASGI/WSGI
Utils/              # AES, JWT, hashing and code-generation helpers
manage.py
script.sql
readme.md
```

## Local development — historical setup

The original project README specifies Python **3.8.6**, Django **3.1.3**, and MySQL **5.7.32**. These are historical versions; do not expose this project to the public internet without updating dependencies and reviewing security.

1. Create and activate a Python virtual environment compatible with the original project.
2. Install the project's required dependencies. **A pinned `requirements.txt` / lock file is not included in the uploaded snapshot**, so dependency resolution must be completed before setup can be considered reproducible.
3. Prepare a local MySQL database, then configure the database and email/environment variables expected by `Backend/settings.py` (which uses `python-decouple`). Do not commit credentials.
4. Once dependencies and configuration are available, run:

```bash
python manage.py migrate
python manage.py runserver
```

These are Django setup commands consistent with the original README; they were **not executed** during this documentation review.

## Testing

Test modules are present under several `App/*/tests/` directories. Once dependencies and local configuration are restored, tests may be run with:

```bash
python manage.py test
```

**No passing-test count or coverage percentage is claimed**, because the test suite has not been run as part of this audit.

## Security and maintenance notes

- The uploaded snapshot contains `DEBUG = True` in Django settings. Disable it for any nonlocal deployment.
- Audit the existing JWT, authentication, password handling, AES, and Paillier implementations before any security-sensitive use.
- Review dependencies and establish a reproducible dependency manifest.
- Protect configuration values, database credentials, signing keys, and email credentials using environment variables; review the repository history for accidental exposure.
- Add integration tests and verified request/response examples before presenting the API as deployment-ready.

## Academic context

Graduation project in **ESCOM, Instituto Politécnico Nacional (IPN)**. The repository showcases Python/Django backend development, domain modeling, relational persistence, application-level authentication workflows, REST-style endpoints, and nontrivial vote-processing logic.
