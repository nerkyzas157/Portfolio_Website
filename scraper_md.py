import markdown
import markdown.extensions.fenced_code
from pygments.formatters import HtmlFormatter
import requests


def scrapy(github_url: str, branch: str = "main") -> str:
    try:
        repo_path = github_url.split("nerkyzas157/")[1]
        url = f"https://raw.githubusercontent.com/nerkyzas157/{repo_path}/{branch}/README.md"

        response = requests.get(url)

        data = response.text
        return data
    except requests.exceptions.RequestException as err:
        return f"Failed to retrieve or process the content: {err}"


def md_data(data, style: str = "emacs"):
    md_template_string = markdown.markdown(data, extensions=["fenced_code"])

    formatter = HtmlFormatter(style=style, full=True, cssclass="codehilite")
    css_string = formatter.get_style_defs()

    md_css_string = "<style>" + css_string + "</style>"
    md_template = md_css_string + md_template_string
    return md_template
