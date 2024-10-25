import asyncio
import time

class AsyncBuffer:
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AsyncBuffer, cls).__new__(cls)
            cls._instance._data = {}
            cls._instance._access_time = {}
            cls._instance._cleanup_task = asyncio.create_task(cls._instance._cleanup())
        return cls._instance

    def __init__(self, timeout=3600):
        self.timeout = timeout

    async def _cleanup(self):
        while True:
            current_time = time.time()
            keys_to_delete = [key for key, timestamp in self._access_time.items() if current_time - timestamp > self.timeout]
            async with self._lock:
                for key in keys_to_delete:
                    del self._data[key]
                    del self._access_time[key]
            await asyncio.sleep(self.timeout)

    async def get(self, key, default=None):
        async with self._lock:
            if key in self._data:
                value = self._data[key]
                self._access_time[key] = time.time()
                return value
            else:
                return default

    async def set(self, key, value):
        async with self._lock:
            self._data[key] = value
            self._access_time[key] = time.time()

    async def delete(self, key):
        async with self._lock:
            if key in self._data:
                del self._data[key]
                del self._access_time[key]

    async def contains(self, key):
        async with self._lock:
            return key in self._data

    async def length(self):
        async with self._lock:
            return len(self._data)

    async def clear(self):
        async with self._lock:
            self._data.clear()
            self._access_time.clear()
