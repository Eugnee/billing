from asynctest import CoroutineMock
import time


class SlowCoroMock(CoroutineMock):
    def __call__(self, *args, **kwargs):
        time.sleep(1)
        return super().__call__(*args, **kwargs)
