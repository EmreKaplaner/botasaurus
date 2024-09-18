from bottle import run, BaseRequest
from .env import is_in_kubernetes, is_worker, is_master

BaseRequest.MEMFILE_MAX = 100 * 1024 * 1024  # 100 MB Max Data Payload

# Import routes based on the context (master, worker, or task)
if is_master:
    from . import master_routes
elif is_worker:
    from . import worker_routes
else:
    from . import task_routes

from .executor import executor

def run_backend():
    # Load and start the executor
    executor.load()
    executor.start()

    # Set host to '0.0.0.0' when in Kubernetes or Docker, and '127.0.0.1' otherwise
    host = '0.0.0.0'  # Ensure it binds to all interfaces for Docker accessibility
    debug = False

    # Start the Bottle server
    run(
        host=host,
        port=8000,
        debug=debug
    )

# Ensure the backend runs if this script is executed directly
if __name__ == "__main__":
    run_backend()
