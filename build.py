import json
import jinja2
import glob


def get_config(path_config: str) -> dict:
    with open(path_config) as f:
        data = json.load(f)
    return data


def elaborate_theme(setting: dict):
    with open("src/" + setting.get("template")) as f:
        template = jinja2.Template("".join(f.readlines()))
    with open("src/" + setting.get('tokenColors')) as f:
        setting['token_colors'] = ''.join(f.readlines())
    raw_template = json.loads(template.render(setting))

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
        template = jinja2.Template("".join(f.readlines()))
    output_template = template.render({"themes": json.dumps(settings, indent=4)})

    with open("package.json", 'w') as f:
        f.write(output_template)
