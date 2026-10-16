# Exercise 06: GitHub Actions CI

## Objective

Build an automated CI workflow that runs Python tests and builds a Docker image when code is pushed to main or a pull request targets main.

## Tools

- GitHub Actions
- Python 3.12
- pytest
- Docker

## Project structure

```text
.github/
  workflows/
    exercise-06-ci.yml
exercises/
  05-docker-compose-flask/
  06-github-actions-ci/
    README.md
    tests/
      test_app.py
```

## Pipeline stages

1. Check out the repository.
2. Set up Python 3.12.
3. Install the Flask application dependencies and pytest.
4. Run automated tests.
5. Build the Flask Docker image tagged `compose-flask:ci`.

## Automated tests

The tests cover:

- The Flask health endpoint.
- Successful visit handling using mocked Redis and MySQL dependencies.
- Graceful handling of a MySQL connection failure.

The unit tests use mocks, so they do not require live Redis or MySQL services.

## Run tests locally

From the repository root, run:

```powershell
python -m pip install -r .\exercises\05-docker-compose-flask\requirements.txt pytest
python -m pytest -v .\exercises\06-github-actions-ci\tests
```

## Build the Docker image locally

```powershell
docker build -t compose-flask:ci .\exercises\05-docker-compose-flask
docker images compose-flask
```

## Verification results

- Local test run: 3 tests passed.
- Local Docker image build: successful.

## Scope

This exercise implements continuous integration. It does not publish the image to a registry or deploy the application.

## Useful GitHub page

After pushing the workflow, open the repository Actions tab to inspect workflow runs and their logs.
