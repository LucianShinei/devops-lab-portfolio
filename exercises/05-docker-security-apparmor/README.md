# Exercise 5: Docker Security with AppArmor and Python

## Objective
Secure a Flask application in Docker with AppArmor, apply the profile through
the Docker SDK for Python, and test restricted actions.

## Files
- `app.py`: Flask application listening on port 5000.
- `Dockerfile`: Builds the `flask-apparmor` image.
- `my-apparmor-profile`: Named AppArmor profile and access restrictions.
- `apply_apparmor.py`: Builds, starts, and inspects the secured container.
- `test_restricted_actions.py`: Tests restricted file access and Bash execution.
- `requirements.txt`: Docker SDK dependency.

## Environment note
AppArmor must be active in the Linux kernel, and the profile must be loaded
before starting the container. In this WSL setup, use the dedicated Docker
daemon configured for AppArmor rather than the Docker Desktop daemon.

## Build and load the profile

```bash
sudo mount -t securityfs securityfs /sys/kernel/security
sudo cp my-apparmor-profile /etc/apparmor.d/my-apparmor-profile
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
sudo aa-status
