import os
import os.path as osp
from configparser import ConfigParser


class Config:
    parser: ConfigParser
    fp: any

    def __init__(self, path: str, defaults: dict[(str, str), str] = None) -> None:
        self.parser = ConfigParser()

        if not osp.isfile(path):
            os.makedirs(osp.dirname(osp.abspath(path)), exist_ok=True)
            open(path, 'x', encoding="utf-8").close() # Create file if not exist

        self.fp = open(path, 'r+', encoding="utf-8")
        self.fp.seek(0)
        self.parser.read_file(self.fp)
        self.setDefaultValues(defaults)

    def __del__(self) -> None:
        self.fp.seek(0)
        self.parser.write(self.fp)
        self.fp.close()

    def setDefaultValues(self, defaults: dict[(str, str), str]) -> None:
        for (section, option), value in defaults.items():
            if not self.parser.has_section(section):
                self.parser.add_section(section)
            if not self.parser.has_option(section, option):
                self.parser.set(section, option, value)

    def getValue(self, section: str, option: str, default: str = None) -> str:
        return self.parser.get(section, option, fallback=default)

    def setValue(self, section: str, option: str, value: str) -> None:
        self.parser.set(section, option, value)

    def getValues(self, section: str, default: list[str, str] = None) -> list[str, str] | None | list[tuple[str, str]]:
        if not self.parser.has_section(section):
            return default
        return self.parser.items(section)

    def setValues(self, section: str, values: list[str, str]) -> None:
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        for (option, value) in values:
            self.parser.set(section, option, value)
