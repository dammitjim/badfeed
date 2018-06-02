from envparse import env


bind = env.str("GUNICORN_BIND")
workers = env.int("GUNICORN_WORKERS")
timeout = env.int("GUNICORN_TIMEOUT", default=30)
loglevel = env.str("GUNICORN_LOGLEVEL", default="error")

user = env.str("GUNICORN_USER")
group = env.str("GUNICORN_GROUP")


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):
    pass


def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spawning workers")


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
