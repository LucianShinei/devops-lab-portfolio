import shutil
from pathlib import Path


def main():
    lab = Path(__file__).resolve().parent
    repository = lab.parent
    deployment = repository / "deployment"
    deployment.mkdir(exist_ok=True)

    exporter = repository / "exercises" / "06-grafana-realtime-monitoring"
    for source in (exporter / "delivery_metrics.py", lab / "requirements.txt", lab / "RUN.md"):
        shutil.copy2(source, deployment / source.name)
        print(f"Staged {source.name} in {deployment}")

    archive = shutil.make_archive(
        str(repository / "delivery-metrics"), "zip", root_dir=repository, base_dir="deployment"
    )
    print(f"Created {archive}")


if __name__ == "__main__":
    main()
