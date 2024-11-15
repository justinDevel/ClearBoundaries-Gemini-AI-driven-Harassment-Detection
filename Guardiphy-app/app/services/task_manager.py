import asyncio
import concurrent.futures
import logging

logger = logging.getLogger(__name__)

class TaskManager:
    def __init__(self, max_workers=10):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

    async def run_async(self, func, *args, **kwargs):
        """Run a function, determining if it is sync or async, and update the task status."""

        try:
           
            if asyncio.iscoroutinefunction(func):
                logger.info(f"Running coroutine {func.__name__}")
                result = await func(*args, **kwargs)
            else:
                logger.info(f"Running synchronous function {func.__name__} in executor")
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(self.executor, func, *args, **kwargs)


            return result
        except Exception as e:
                logger.error(f"Error in task {func.__name__}: {e}")
                raise e

    def add_task(self, func, *args, **kwargs):
        """Add a task to the event loop without blocking other requests."""

        return asyncio.create_task(self.run_async(func, *args, **kwargs))



    async def wait_for_tasks(self):
        """Wait for all tasks to complete."""
        tasks = [task for task in asyncio.all_tasks() if not task.done()]
        await asyncio.gather(*tasks)

    def shutdown(self, wait=True):
        """Shutdown the executor."""
        logger.info("Shutting down the TaskManager executor.")
        self.executor.shutdown(wait=wait)


task_manager = TaskManager(max_workers=10)
