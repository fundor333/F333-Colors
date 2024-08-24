import click
import json


def get_config(path_config: str) -> dict:
    with open(path_config) as f:
        data = json.load(f)
    return data


def set_config(path_config: str, data: dict) -> None:
    with open(path_config, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_version(config: dict) -> (int, int, int):
    version = config['version']
    a, b, c = version.split('.')
    return int(a), int(b), int(c)


def set_version(path_config: str, config: dict, a: int, b: int, c: int):
    config['version'] = f"{a}.{b}.{c}"
    set_config(path_config=path_config, data=config)


@click.group()
def version():
    pass


@version.command()
def hotfix(**kwargs):
    config = get_config('setting.json')
    a, b, c = get_version(config)
    set_version('setting.json', config, a, b, c + 1)


@version.command()
def minor(**kwargs):
    config = get_config('setting.json')
    a, b, c = get_version(config)
    set_version('setting.json', config, a, b + 1, 0)


@version.command()
def major(**kwargs):
    config = get_config('setting.json')
    a, b, c = get_version(config)
    set_version('setting.json', config, a + 1, 0, 0)


if __name__ == '__main__':
    version()
