class _Config():
    __conf = {}
    _write_once = []

    def __init__():
        # TODO: 根据env更新配置项
        pass

    def __getattr__(self, key):
        return self.__conf.get(key, None)

    def __setattr__(self, __name: str, __value) -> None:
        if __value is None:
            raise AttributeError
        if __name in self._write_once and __name in self.__conf:
            raise AttributeError
        self.__conf[__name] = __value


Config = _Config
