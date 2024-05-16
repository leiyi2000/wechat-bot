"""定时任务"""

from typing import Callable, Any, List
from asyncio import Task

import asyncio

from datetime import datetime, timedelta


class Job:
    def __init__(
        self,
        func: Callable[..., Any],
        seconds: int | None,
        minutes: int | None,
        hours: int | None,
        days: int | None,
        at: str | None,
    ) -> None:
        self.func = func
        # 距离多少时长后执行
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours
        self.days = days
        # 在某一时刻执行
        self.at = at
        self._interval = None
        self.last_run: datetime = datetime.now()
        self.next_run: datetime = self._get_next_run()

    def _are_you_ok(
        self,
        check_datetime: datetime,
        target_ymdhms: List[str | int],
    ) -> bool:
        if check_datetime < self.last_run:
            return False
        ymdhms = [
            check_datetime.year,
            check_datetime.month,
            check_datetime.day,
            check_datetime.hour,
            check_datetime.minute,
            check_datetime.second,
        ]
        for i in range(6):
            if target_ymdhms[i] != "*" and target_ymdhms[i] != ymdhms[i]:
                return False
        return True

    def _get_next_run(self):
        if self.interval is not None:
            run_datetime = self.last_run + timedelta(seconds=self.interval)
        else:
            # 解析at获取下次运行时间, (年, 月, 日, 时, 分, 秒) = * * * * * *
            target_ymdhms = self.at.split(" ")
            timedeltas = [
                timedelta(),
                # 懒得算了
                timedelta(days=360),
                timedelta(days=29),
                timedelta(days=1),
                timedelta(hours=1),
                timedelta(minutes=1),
            ]
            last_ymdhms = [
                self.last_run.year,
                self.last_run.month,
                self.last_run.day,
                self.last_run.hour,
                self.last_run.minute,
                self.last_run.second,
            ]
            ymdhms = []
            max_timedelta = timedelta()
            for i in range(6):
                if target_ymdhms[i] == "*":
                    ymdhms.append(last_ymdhms[i])
                else:
                    target_ymdhms[i] = int(target_ymdhms[i])
                    ymdhms.append(target_ymdhms[i])
                    max_timedelta = max(max_timedelta, timedeltas[i])
            run_datetime = datetime(*ymdhms)
            run_datetime += max_timedelta
            # 补救-2月特殊月份
            while not self._are_you_ok(run_datetime, target_ymdhms):
                run_datetime += timedelta(days=1)
        return run_datetime

    @property
    def interval(self):
        interval = self.seconds
        if self._interval is not None:
            return self._interval
        elif self.minutes:
            interval = self.minutes * 60
        elif self.hours:
            interval = self.hours * 60 * 60
        elif self.days:
            interval = self.days * 24 * 60 * 60
        self._interval = interval
        return self._interval

    async def run(self):
        self.refresh_next_run()
        if asyncio.iscoroutinefunction(self.func):
            return await self.func()
        else:
            return self.func()

    def refresh_next_run(self):
        self.last_run = self.next_run
        self.next_run = self._get_next_run()

    @property
    def ready(self) -> bool:
        return datetime.now() > self.next_run


class Schedule:
    def __init__(self) -> None:
        self.jobs: List[Job] = []
        self.tasks: List[Task] = []

    def job(
        self,
        seconds: int | None,
        minutes: int | None,
        hours: int | None,
        days: int | None,
        at: str | None,
    ):
        def decorator(func: Callable[..., Any]):
            job = Job(func, seconds, minutes, hours, days, days, at)
            self.jobs.append(job)
            return func

        return decorator

    async def run(self):
        while True:
            for job in self.jobs:
                if job.ready:
                    self.tasks.append(asyncio.create_task(job.run()))
            await asyncio.sleep(0.1)
            # 清理完成的任务
            self.tasks = [task for task in self.tasks if not task.done()]
