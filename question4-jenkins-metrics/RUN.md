# Run the delivery-metrics exporter

Extract the ZIP and open PowerShell in its deployment folder. Python 3.9 or later is required.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe delivery_metrics.py
```

Open http://localhost:8000/metrics or query it in another PowerShell window with
`Invoke-RestMethod http://localhost:8000/metrics`. The exporter generates sample
delivery metrics once per second. Press Ctrl+C to stop it.
