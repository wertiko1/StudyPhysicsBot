import datetime
import uuid
import calendar
from typing import Any, Literal

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap, ColorConverter
from matplotlib.patches import Polygon
from pandas import Series, DatetimeIndex


class CalendarHeatmap:
    def __init__(self, title_template: str = "Total completed: {count}"):
        """
        Класс для генерации тепловых карт-календарей.

        Параметры:
            title_template (str):
                Шаблон заголовка для тепловой карты.
                Может содержать `{count}`, который заменится на сумму значений.
        """
        self.title_template = title_template

    @staticmethod
    def yearplot(
            data: Series,
            *,
            how: str | None = "sum",
            vmin: float | None = 0,
            vmax: float | None = None,
            cmap: str = "Greens",
            fillcolor: str = "whitesmoke",
            linewidth: float = 1,
            linecolor: str | None = None,
            months: dict[int, str] | None = None,
            days: dict[int, str] | None = None,
            monthly_border: bool = False,
            mode: Literal["year", "last365"] = "last365",
            ax: Axes | None = None,
            **kwargs: Any,
    ) -> Axes:
        """
        Внутренний метод для построения тепловой карты за год.
        """
        data = data.astype("int64")
        end_date = data.index.max() if not data.empty else pd.Timestamp.today()
        if mode == "last365":
            start_date = end_date - pd.DateOffset(days=365 - 30)
        else:
            start_date = pd.Timestamp(f"{end_date.year}-01-01")

        by_day = (
            data.resample("D")
            .agg(how)
            .reindex(pd.date_range(start=start_date, end=end_date, freq="D"))
            .fillna(0)
        )

        if vmin is None:
            vmin = by_day.min()
        if vmax is None:
            vmax = by_day.max()
        if ax is None:
            ax = plt.gca()
        if linecolor is None:
            linecolor = ax.get_facecolor()
            if ColorConverter().to_rgba(linecolor)[-1] == 0:
                linecolor = "white"
        kwargs |= {"linewidth": linewidth, "edgecolors": linecolor}
        if months is None:
            months = dict(enumerate(calendar.month_abbr, start=1))
        if days is None:
            days = dict(enumerate(calendar.day_abbr, start=1))
        index: DatetimeIndex = by_day.index
        by_day = pd.DataFrame(
            {
                "dbs": by_day,
                "fill": 1,
                "day": index.dayofweek,
                "week": ((index - by_day.index[0]).days // 7) + 1,
            }
        )

        plot_data = by_day.pivot(
            index="day", columns="week", values="dbs"
        ).values[::-1]
        fill_data = by_day.pivot(
            index="day", columns="week", values="fill"
        ).values[::-1]

        plot_data = np.ma.masked_where(np.isnan(plot_data), plot_data)
        fill_data = np.ma.masked_where(np.isnan(fill_data), fill_data)

        ax.pcolormesh(fill_data, vmin=0, vmax=1, cmap=ListedColormap([fillcolor]))
        ax.pcolormesh(plot_data, vmin=vmin, vmax=vmax, cmap=cmap, **kwargs)

        ax.set(xlim=(0, plot_data.shape[1]), ylim=(0, plot_data.shape[0]))
        ax.set_aspect("equal")
        ax.spines[:].set_visible(False)
        ax.xaxis.set_tick_params(which="both", length=0)
        ax.yaxis.set_tick_params(which="both", length=0)

        xticks = {}
        months_in_order = list(range(start_date.month, 13)) + list(
            range(1, end_date.month + 1)
        )
        for month in months_in_order:
            group = by_day[index.month == month]
            first = group.index.min()
            last = group.index.max()
            x0 = (first - index[0]).days // 7
            x1 = (last - index[0]).days // 7
            xticks[months[month]] = x0 + (x1 - x0 + 1) / 2
            if monthly_border:
                p = [(x0, 0), (x0, 7), (x1 + 1, 7), (x1 + 1, 0), (x0, 0)]
                ax.add_artist(
                    Polygon(
                        p,
                        edgecolor="black",
                        facecolor="None",
                        linewidth=1,
                        zorder=20,
                        clip_on=False,
                    )
                )

        xticks[months[months_in_order[0]]] = 0.5
        xticks[months[months_in_order[-1]]] = 48

        ax.set_xticks(list(xticks.values()))
        ax.set_xticklabels(xticks.keys())
        ax.set_yticks([6 - i + 0.5 for i in days.keys()])
        ax.set_yticklabels(days.values(), rotation="horizontal", va="center")

        return ax

    def generate(
            self, data: dict[datetime.datetime, int]
    ) -> str:
        """
        Генерирует тепловую карту-календарь и сохраняет ее в файл.

        Параметры:
            dbs (dict[datetime.datetime, int]):
                Данные для построения тепловой карты (даты и значения).

        Возвращает:
            str: Путь к сохраненному изображению.
        """
        series_data = pd.Series(data)
        series_data.index = pd.to_datetime(series_data.index)

        plt.figure(figsize=(7, 3))

        self.yearplot(
            series_data,
            months={
                1: "", 2: "", 3: "", 4: "", 5: "", 6: "",
                7: "", 8: "", 9: "", 10: "", 11: "", 12: "",
            },
            days={
                0: "Пн", 1: "", 2: "Ср", 3: "", 4: "Пт", 5: "", 6: "Вс",
            },
        )
        plt.title(self.title_template.format(count=series_data.sum()))

        output_file_path = f"heatmap_{uuid.uuid4().hex}.png"
        plt.savefig(output_file_path)
        plt.close()

        return output_file_path


# Usage
if __name__ == "__main__":
    example_data = {
        datetime.datetime(2024, 8, 1): 5,
        datetime.datetime(2024, 8, 2): 8,
        datetime.datetime(2024, 8, 3): 2,
    }

    heatmap_generator = CalendarHeatmap(title_template="Выполнено задач: {count}")

    heatmap_path = heatmap_generator.generate(example_data)

    print(f"Heatmap saved at: {heatmap_path}")
