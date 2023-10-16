import json

from ipywidgets import Text, VBox

from .base import BaseCoreWidget
from .style import layouts, styles


class ProjectInformationWidget(BaseCoreWidget):
    name = "project_information"

    @property
    def values(self) -> dict:
        return dict(
            project_id=self.project_id.value,
            project_name=self.project_name.value,
            author=self.author.value,
            project_remark=self.project_remark.value,
        )

    def _load_cache(self) -> None:
        with open(self.widget_cache_path, "r") as cache_file:
            values = json.load(cache_file)
            self.project_id.value = values["project_id"]
            self.project_name.value = values["project_name"]
            self.project_remark.value = values["project_remark"]
            self.author.value = values["author"]

    def _init_ipywidget(self) -> VBox:
        self.project_id = Text(
            value="21305",
            description="project ID",
            tooltip="The project ID",
            layout=layouts["text"],
            style=styles["project_information"],
            continuous_update=False,
        )

        self.project_remark = Text(
            value=None,
            placeholder="Additional project information for in the report",
            description="project remark",
            tooltip="Additional project information for in the report",
            continuous_update=False,
        )

        self.author = Text(
            value="N. Uclei",
            description="author",
            tooltip="Author of the report",
            layout=layouts["text"],
            style=styles["project_information"],
            continuous_update=False,
        )

        self.project_name = Text(
            value="Automated pile design",
            description="project name",
            tooltip="The project name",
            layout=layouts["text"],
            style=styles["project_information"],
            continuous_update=False,
        )

        def handle_project_id_change(change: dict) -> None:
            self._cache_values()

        def handle_author_change(change: dict) -> None:
            self._cache_values()

        def handle_project_name_change(change: dict) -> None:
            self._cache_values()

        self.project_id.observe(handle_project_id_change, names="value")
        self.project_name.observe(handle_project_name_change, names="value")
        self.author.observe(handle_author_change, names="value")

        return VBox([self.project_id, self.project_name, self.author])
