from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterEqualFunction
from flask_appbuilder.fields import QuerySelectField
from flask_appbuilder.views import ModelView
from flask_appbuilder.widgets import ListBlock, ShowBlockWidget
from flask import g
from . import appbuilder, db
from .models import TaskRecord, TaskType, TaskStatus

#Below import is for charts
import calendar
from flask_appbuilder.charts.views import (
    DirectByChartView, DirectChartView, GroupByChartView
)
from flask_appbuilder.models.group import aggregate_avg, aggregate_sum, aggregate_count, aggregate

def get_user():
    return g.user.username

class TasksView(ModelView):
    datamodel = SQLAInterface(TaskRecord)
    base_permissions = ["can_list", "can_show","menu_access"]

    #label_columns = {"result_url": "Result"}

    list_columns = ["task_id", "user_name", "task_status", "task_type", "task_subject",
"task_describtion", "create_date", "update_date", "comments"]
    search_columns = ["task_id", "user_name", "task_status", "task_type", "task_subject",
"task_describtion", "create_date", "update_date", "comments"]

    show_fieldsets = [
        ("Summary", {"fields": ["task_id", "user_name", "task_status", "task_type", "task_subject",
"task_describtion", "create_date", "update_date", "comments"]}),
        ("Description", {"fields": ["description"], "expanded": True}),
    ]
    #base_order = ("log_id", "asc")
    base_order = ("task_id", "desc")
    base_filters = [["user_name", FilterEqualFunction, get_user]]

class TasksEditView(ModelView):
    datamodel = SQLAInterface(TaskRecord)
    base_permissions = ["can_list", "can_show","menu_access","can_add","can_edit","can_delete"]

    #label_columns = {"result_url": "Result"}

    list_columns = ["task_id", "user_name", "task_status", "task_type", "task_subject",
"task_describtion", "create_date", "update_date", "comments"]
    search_columns = ["task_id", "user_name", "task_status", "task_type", "task_subject",
"task_describtion", "create_date", "update_date", "comments"]

    show_fieldsets = [
        ("Summary", {"fields": ["task_id", "user_name", "task_status", "task_type", "task_subject",
"task_describtion", "create_date", "update_date", "comments"]}),
        ("Description", {"fields": ["description"], "expanded": True}),
    ]
    #base_order = ("log_id", "asc")
    base_order = ("task_id", "desc")
    base_filters = [["user_name", FilterEqualFunction, get_user]]


class TaskTypeEditView(ModelView):
    datamodel = SQLAInterface(TaskType)
    related_views = [TasksView]

class TaskStatusEditView(ModelView):
    datamodel = SQLAInterface(TaskStatus)
    related_views = [TasksView]

def pretty_month_year(value):
    return calendar.month_name[value.month] + " " + str(value.year)

class TaskDayChartView(GroupByChartView):
    datamodel = SQLAInterface(TaskRecord)
    chart_title = "Tasks Per Day"
    chart_type = 'LineChart'
    definitions = [
        {
            "label": "Tasks Sum",
            "group": "create_date",
            "series": [
                (aggregate_count, "task_id"),
            ],
        },
#        {
#            "label": "EC2 Test Per Run",
#            "group": "test_date",
#            "series": [
#                "cases_total",
#                "cases_pass",
#                "cases_fail",
#                "cases_cancel",
#                "cases_other",
#            ],
#        },
#        {
#            "group": "month_year",
#            "formatter": pretty_month_year,
#            "series": [
#                (aggregate_sum, "cases_total"),
#                (aggregate_sum, "cases_fail"),
#            ],
#        },
]

db.create_all()
appbuilder.add_view(TasksView, "TasksList", icon="fa-folder-open-o",category="TasksList")
appbuilder.add_view(
    TasksEditView, "Edit Tasks List", icon="fa-envelope", category="Management"
)

appbuilder.add_view(
    TaskTypeEditView, "Edit Task Types", icon="fa-envelope", category="Management"
)
appbuilder.add_view(
    TaskStatusEditView, "Edit Task Status List", icon="fa-envelope", category="Management"
)
appbuilder.add_separator("Management")

appbuilder.add_view(
    TaskDayChartView, "Task Per Day", icon="fa-folder-open-o", category="DataAnalyze"
)


