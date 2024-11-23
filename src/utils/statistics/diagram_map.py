import os
import matplotlib.pyplot as plt
from typing import List, Optional, Union
from loguru import logger


class Colors:
    RED: str = "#FF5733"
    GREEN: str = "#33FF57"
    BLUE: str = "#3357FF"
    YELLOW: str = "#F5FF33"
    PURPLE: str = "#800080"
    ORANGE: str = "#FFA500"
    PINK: str = "#FFC0CB"
    CYAN: str = "#00FFFF"
    MAGENTA: str = "#FF00FF"
    LIME: str = "#00FF00"
    TEAL: str = "#008080"
    BROWN: str = "#A52A2A"
    GRAY: str = "#808080"
    LIGHT_BLUE: str = "#ADD8E6"
    DARK_BLUE: str = "#00008B"
    LIGHT_GREEN: str = "#90EE90"
    DARK_GREEN: str = "#006400"
    GOLD: str = "#FFD700"
    SILVER: str = "#C0C0C0"
    BEIGE: str = "#F5F5DC"
    INDIGO: str = "#4B0082"
    VIOLET: str = "#EE82EE"
    TURQUOISE: str = "#40E0D0"
    CORAL: str = "#FF7F50"
    IVORY: str = "#FFFFF0"
    MINT: str = "#98FF98"
    PEACH: str = "#FFDAB9"


class ColorPalette:
    @staticmethod
    def from_palette(palette_name: str) -> List[str]:
        """
        Returns a list of colors from a Matplotlib palette.
        :param palette_name: The name of the palette (e.g., 'Paired', 'Set2').
        :return: List of colors from the selected palette.
        :raises ValueError: If the palette is not found.
        """
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
        """
        Initializes dbs for the chart.

        :param data: A list of values for the chart.
        :param labels: A list of labels for each value.
        :param colors: Custom colors (list) or the name of a built-in palette.
        :param title: The title of the chart.
        :raises ValueError: If the number of values and labels do not match.
        """
        if len(data) != len(labels):
            raise ValueError("The number of values and the number of labels must match.")
        self.data = data
        self.labels = labels
        self.colors = colors
        self.title = title


class PieChart:
    def __init__(self) -> None:
        pass

    def draw(self, data: ChartData) -> None:
        """
        Draws a pie chart.

        :param data: A ChartData object containing the dbs for the chart.
        """
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

    def save(self, data: ChartData, file_name: str) -> None:
        """
        Saves the pie chart to a file.

        :param data: A ChartData object with the dbs for the chart.
        :param file_name: The name of the file to save the chart.
        """
        self.draw(data)
        plt.savefig(file_name)
        logger.info(f"Chart saved as {file_name}")
        plt.close()

    def delete_file(self, file_name: str) -> None:
        """
        Deletes the chart file.

        :param file_name: The name of the file to delete.
        """
        if os.path.exists(file_name):
            os.remove(file_name)
            logger.info(f"File {file_name} deleted.")
        else:
            logger.warning(f"File {file_name} not found.")

    def _get_colors(self, colors: Optional[Union[List[str], str]]) -> List[str]:
        """
        Retrieves a list of colors. If a palette name is provided, it fetches colors from that palette.

        :param colors: A list of colors or the name of a palette.
        :return: A list of colors.
        """
        if isinstance(colors, str):
            return ColorPalette.from_palette(colors)
        elif isinstance(colors, list):
            return colors
        return []


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
    chart.delete_file("chart.png")
