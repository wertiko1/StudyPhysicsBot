import matplotlib.pyplot as plt
from typing import List, Optional, Union

from loguru import logger
from src.schemas import Colors


class ColorPalette:
    @staticmethod
    def from_palette(palette_name: str) -> List[str]:
        palette = getattr(plt.cm, palette_name, None)
        if palette is None:
            raise ValueError(f"Palette '{palette_name}' not found. Use one of the built-in Matplotlib palettes.")
        return [color for color in palette.colors]


class ChartData:
    def __init__(
            self,
            data: List[float],
            labels: List[str],
            colors: Optional[Union[List[str], str]] = None,
            title: Optional[str] = "Pie Chart"
    ) -> None:
        if len(data) != len(labels):
            raise ValueError("The number of values and the number of labels must match.")
        self.data = data
        self.labels = labels
        self.colors = colors
        self.title = title


class PieChart:
    def _draw(self, data: ChartData) -> None:
        colors = self._get_colors(data.colors)

        plt.figure(figsize=(6, 6))
        plt.pie(
            data.data,
            labels=data.labels,
            autopct='%d%%',
            startangle=90,
            colors=colors,
            wedgeprops={"edgecolor": "black"}
        )
        if data.title:
            plt.title(data.title)
        logger.info("Displaying the pie chart.")
        plt.show()

    def _get_colors(self, colors: Optional[Union[List[str], str]]) -> List[str]:
        if isinstance(colors, str):
            return ColorPalette.from_palette(colors)
        elif isinstance(colors, list):
            return colors
        return []

    def save(self, data: ChartData, file_name: str) -> None:
        self._draw(data)
        plt.savefig(file_name)
        logger.info(f"Chart saved as {file_name}")
        plt.close()


# Usage
if __name__ == '__main__':
    values: List[float] = [5, 5, 60, 30]
    categories: List[str] = [
        "Category A",
        "Category B",
        "Category C",
        "Category D"
    ]
    custom_colors = [Colors.RED, Colors.GREEN, Colors.BLUE, Colors.YELLOW]

    chart_data = ChartData(
        values,
        categories,
        colors=custom_colors,
        title="Pie Chart with Custom Colors"
    )

    chart = PieChart()
    chart.save(chart_data, "chart.png")
