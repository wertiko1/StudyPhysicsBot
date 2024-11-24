import os
import uuid
import datetime
from typing import Dict

from loguru import logger

from .plots.calendar_map import CalendarHeatmap
from .plots.diagram_map import ChartData, PieChart


class StatisticView:
    def __init__(self) -> None:
        pass

    def get_calendar(self, data: Dict[datetime.datetime, int], title: str) -> str:
        heatmap_generator = CalendarHeatmap(title)
        return heatmap_generator.generate(data)

    def get_diagram(self, data: ChartData) -> str:
        chart = PieChart()
        output_file_path = f"cache/chart_{uuid.uuid4().hex}.png"
        chart.save(data, output_file_path)
        return output_file_path

    def delete(self, file_name: str) -> None:
        if os.path.exists(file_name):
            os.remove(file_name)
            logger.info(f"File {file_name} deleted.")
        else:
            logger.warning(f"File {file_name} not found.")
