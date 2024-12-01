import os

from loguru import logger


class LogSetup:
    def __init__(self, log_path: str = "logs/logs.log", log_level: str = "DEBUG") -> None:
        self.log_path = log_path
        self.log_level = log_level
        self._configure_logger()

    def _rotation_by_size(self, message, file):
        if os.path.getsize(file.name) >= 5 * 1024 * 1024:
            base_name, ext = os.path.splitext(file.name)
            existing_logs = sorted(
                [f for f in os.listdir(os.path.dirname(file.name)) if
                 f.startswith(base_name) and f.endswith('.zip')],
                key=lambda x: int(x.split('_')[-1].split('.')[0]) if '_' in x else 0
            )
            new_index = len(existing_logs) + 1
            zip_name = f"{base_name}_{new_index}.zip"
            os.rename(file.name, file.name + '.tmp')
            os.system(f"zip -m {zip_name} {file.name}.tmp")
            return True
        return False

    def _configure_logger(self):
        logger.add(
            self.log_path,
            level=self.log_level,
            rotation=self._rotation_by_size,
            compression=None
        )
