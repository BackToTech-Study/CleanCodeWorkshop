from samples.WeatherApi.configurations.Dynamic import Dynamic


class LoggerConfiguration:

    @property
    def Level(self) -> bool:
        return self.Level

    @property
    def FileName(self) -> str:
        return self.FileName

    @property
    def MaxBytes(self) -> int:
        return self.MaxBytes

    @property
    def BackupCount(self) -> int:
        return self.BackupCount
