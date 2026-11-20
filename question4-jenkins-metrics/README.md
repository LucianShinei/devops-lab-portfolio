# Question 4 — Jenkins pipeline for a metrics exporter

## Write-up

**Approach.** Use the portfolio's delivery-metrics exporter and deterministic
test. Check out the source from GitHub, install the pinned dependency in a fresh
Python virtual environment, run the tests, and archive the staged deployment
files. Run the same job with its failure parameter enabled to demonstrate the
test gate.

**Tools.** GitHub and Git, Jenkins Declarative Pipeline, Python 3.9+,
the Prometheus Python client, unittest, and the Python standard library for ZIP
packaging. Use PowerShell for setup and verification on Windows.

```text
GitHub → Jenkins loads Jenkinsfile → Checkout → Install → Test
                                                         ├─ Pass → Stage files → Archive ZIP
                                                         └─ Fail → Failed build
```

## Jenkins job

Create a Pipeline job with **Pipeline script from SCM**, select **Git**, and
enter the portfolio's GitHub URL. Select branch `*/main` if the exercise is
merged there, or the exercise branch where it is published. Use script path
`question4-jenkins-metrics/Jenkinsfile`. The agent needs Git and Python with venv.

Run the job with `FORCE_TEST_FAILURE` disabled and review all four stages.
Download `delivery-metrics.zip` from the successful build and follow its
`deployment/RUN.md`. Rerun with the parameter enabled and verify the console
records the intentional failed assertion, skips deployment packaging, and ends
with `Finished: FAILURE`.
