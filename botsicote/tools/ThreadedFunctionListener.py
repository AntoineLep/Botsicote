import queue
import logging
import time
from threading import Thread


class ThreadedFunctionListener(Thread):
    """
    Management of threaded function
    """

    def __init__(self, target, *args, **kwargs):
        """
        Initialize a threaded function listener

        :param target: Function to execute in threaded context
        :param args: List of arguments to be passed to the threaded function
        :param kwargs: List of named arguments to be passed to the threaded function
        """
        Thread.__init__(self)
        self._queue = queue.Queue()
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._repeat = False
        self._repeat_delay = 0
        self._stop_requested = True

    def start(self):
        """
        Start the function in a thread
        """
        self._stop_requested = False
        super(ThreadedFunctionListener, self).start()

    def stop(self, timeout=None):
        """
        Stop the thread execution

        :param timeout: Max time to wait before stopping the thread
        """
        self._stop_requested = True
        self.join(timeout)

    def flush_first_queue_item(self):
        """
        Get the first item of the queue. This item will be no longer available in the queue after this call

        :return: The first item of the queue
        """
        if not self._queue.empty():
            return self._queue.get()
        return None

    def flush_all_queue_items(self):
        """
        Get all items of the queue. The queue will be empty after this call

        :return: All items of the queue
        :rtype: list
        """
        items = []

        while not self._queue.empty():
            items.append(self._queue.get())

        return items if items != [] else None

    def set_repeat(self, repeat):
        """
        Set the repeat option of the thread.
        If set to True, the thread will loop on the function and store the results of each executions.
        If set to False (default), the thread will execute only once the function and store the result

        :param repeat: Repeat option of the thread
        :type repeat: bool
        """
        self._repeat = repeat

    def set_repeat_delay(self, repeat_delay):
        """
        Set the repeat delay.

        :param repeat_delay: Number of second to wait between each threaded function call
        :type repeat_delay: int
        """
        self._repeat_delay = repeat_delay

    def run(self):
        try:
            if self._target:
                while not self._stop_requested:
                    result = self._target(*self._args, **self._kwargs)
                    if result is not None:
                        self._queue.put(result)
                    if not self._repeat:
                        break
                    if self._repeat_delay > 0:
                        time.sleep(self._repeat_delay)
        except BaseException as e:
            logging.error("An unhandled error occurred in ThreadedFunctionListener. The thread execution is stopped.")
            logging.error(str(e))
        finally:
            del self._target, self._args, self._kwargs
