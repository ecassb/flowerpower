def _get_executor(mode: str, max_tasks: int = 10, num_cpus: int = 4):
    shutdown = None
    if mode == "local":
        remote_executor = executors.SynchronousLocalTaskExecutor()
    elif mode == "multiprocessing":
        remote_executor = executors.MultiProcessingExecutor(max_tasks=max_tasks)
    elif mode == "multithreading":
        remote_executor = executors.MultiThreadingExecutor(max_tasks=max_tasks)
    elif mode == "dask":
        from dask import distributed

        from hamilton.plugins import h_dask

        cluster = distributed.LocalCluster()
        client = distributed.Client(cluster)
        remote_executor = h_dask.DaskExecutor(client=client)
        shutdown = cluster.close
    else:
        import ray

        from hamilton.plugins import h_ray

        remote_executor = h_ray.RayTaskExecutor(num_cpus=4)
        shutdown = ray.shutdown
    return remote_executor, shutdown
