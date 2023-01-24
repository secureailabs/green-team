import asyncio
from typing import Any, Coroutine

coroutines = set()


def add_async_task(task_function: Coroutine[Any, Any, None]):
    """
    Add a task to the set of coroutines to be run

    :param task_function: the function to be run
    :type task_function: Coroutine[Any, Any, None]
    """
    task = asyncio.create_task(task_function)
    coroutines.add(task)
    task.add_done_callback(coroutines.discard)
