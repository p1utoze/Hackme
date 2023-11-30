from fastapi.templating import Jinja2Templates
from pathlib import Path


def get_templates():
    template_dir = Path(__file__).parent.parent / "templates"
    print(template_dir)
    return Jinja2Templates(directory=template_dir)


# templates = get_templates()
# print(templates.get_template("dashboard.html"))
