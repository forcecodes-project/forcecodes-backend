from fastapi import FastAPI
from sqladmin import Admin, ModelView

from database.models import Problem, User
from database.session import engine

app = FastAPI()
admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.ts_created]


class ProblemAdmin(ModelView, model=Problem):
    column_list = [Problem.id, Problem.title, Problem.ts_created]


admin.add_view(UserAdmin)
admin.add_view(ProblemAdmin)
