import json
import glob
from jinja2 import Template


def get_config(path_config: str) -> dict:
    with open(path_config) as f:
        data = json.load(f)
    return data


def elaborate_theme(setting: dict):
    with open("src/" + setting.get("template")) as f:
        template = Template("".join(f.readlines()))
    with open("src/" + setting.get('tokenColors')) as f:
        setting['token_colors'] = ''.join(f.readlines())
    raw_template = json.loads(template.render(setting))

    if setting.get('uiTheme', 'vs-dark'):
        with open(setting.get('git', "src/git/git_dark.json")) as f:
            git_str = json.load(f)
            raw_template['colors'].update(git_str)
    else:
        with open(setting.get('git', "src/git/git_basic.json")) as f:
            git_str = json.load(f)
            raw_template['colors'].update(git_str)

    output_template = json.dumps(raw_template, indent=4)
    with open("themes/" + setting['filename'], 'w') as f:
        f.write(output_template)


if __name__ == "__main__":
    settings = []
    for e in glob.glob("src/colors/*"):
        setting = get_config(e)
        elaborate_theme(setting)
        settings.append(
            {
                "label": setting["title"],
                "uiTheme": setting["uiTheme"],
                "path": "./themes/" + setting["filename"],
            }
        )
    with open('src/template/package.json.jinja') as f:
        template = Template("".join(f.readlines()))
    stt = get_config('setting.json')
    stt['themes'] = json.dumps(settings, indent=4)
    output_template = template.render(stt)

    with open("package.json", 'w') as f:
        f.write(output_template)
