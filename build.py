import json
import jinja2

COLOR_SETTINGS = [
    "src/colors_green.json",
    "src/colors_red.json",
    "src/colors_blue.json",
]


def get_config(path_config: str) -> dict:
    with open(path_config) as f:
        data = json.load(f)
    return data


def elaborate_theme(setting: dict):
    with open("src/" + setting.get("template")) as f:
        template = jinja2.Template("".join(f.readlines()))
    with open("src/" + setting.get('tokenColors')) as f:
        setting['token_colors'] = ''.join(f.readlines())
    output_template = template.render(setting)
    with open("themes/" + setting['filename'], 'w') as f:
        f.write(output_template)


for e in COLOR_SETTINGS:
    setting = get_config(e)
    elaborate_theme(setting)
