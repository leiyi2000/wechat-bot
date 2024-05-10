from typing import Callable, Any, List, Dict


class CommandRoute:
    """命令路由"""

    def __init__(
        self,
        name: str,
        prefix: str,
        func: Callable[..., Any],
        event_arg: bool,
        func_kwargs: Dict[str, Any],
    ) -> None:
        self.name = name
        self.prefix = prefix
        self.func = func
        self.event_arg = event_arg
        self.func_kwargs = func_kwargs

    def match(self, msg: str) -> bool:
        return msg.startswith(self.prefix)


class CommandRouter:
    """指令路由器"""

    def __init__(self):
        self.routes: List[CommandRoute] = []

    def add_route(self, route: CommandRoute):
        self.routes.append(route)

    def command(
        self,
        prefix: str,
        *,
        name: str = None,
        event_arg: bool = False,
        func_kwargs: Dict[str, Any] = {},
    ):
        def decorator(func: Callable[..., Any]):
            # 初始化一个命令路由
            route = CommandRoute(name or func.__name__, prefix, func, event_arg, func_kwargs)
            self.add_route(route)
            return func
        return decorator

    def matches(self, msg: str) -> List[CommandRoute]:
        return [route for route in self.routes if route.match(msg)]

    def include_router(self, router: "CommandRouter"):
        for route in router.routes:
            self.add_route(route)
