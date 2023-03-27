from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
import os


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.email == os.environ.get(
            "MAIL_USERNAME"
        )
