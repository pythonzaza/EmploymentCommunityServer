import multiprocessing

bind = '0.0.0.0:80'
workers = multiprocessing.cpu_count() * 2 + 1

backlog = 2048
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
daemon = True
debug = True
proc_name = 'CommunityServer'
pidfile = './log/gunicorn.pid'
errorlog = './log/gunicorn.log'
loglever = "info"
