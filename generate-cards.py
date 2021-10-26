#!/usr/bin/env python3

from pathlib import Path

import yaml
import pybars
from weasyprint import HTML


def build_template(file):
    with open(file) as index_file:
        html_text = index_file.read()

        template_compiler = pybars.Compiler()
        return template_compiler.compile(html_text)


def load_yaml_file(p: Path):
    with p.open('r') as stream:
        return yaml.safe_load(stream)


def term_entry(_, value):
    value = value.strip()
    res = '&nbsp;' if value.upper() == 'TODO' else value
    return pybars.strlist([res])

def main():
    data_path = Path('data')
    template_path = Path('template')
    out_file_path = Path('out')

    game_data = load_yaml_file(data_path / 'game.yml')

    template = build_template(template_path / 'index.html')
    html_source = template(game_data, helpers={'term_entry': term_entry})

    html_dom = HTML(string=html_source, base_url=str(template_path))

    out_file_path.mkdir(parents=True, exist_ok=True)
    html_dom.write_pdf(out_file_path / 'game.pdf')


if __name__ == '__main__':
    main()
