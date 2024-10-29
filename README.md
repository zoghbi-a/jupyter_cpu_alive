# Content
`jupyter_cpu_alive` is a jupyter server extension that updates the server's `api_last_activity` based on CPU usage. This is useful to keep the server alive so it is not culled when running inside jupyterhub.

# Install
Install with `pip install jupyter_cpu_alive`.

Then run jupyterlab.

The extension is configured with two environment variables:
- `JUPYTER_CPU_ALIVE_PERCENT_MIN` defines the minimum CPU activity, above which the CPU is considered active. The default is 70%.
- `JUPYTER_CPU_ALIVE_INTERVAL` gives the interval in second for checking for activity and updating the `api_last_activity`.