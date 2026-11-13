from configparser import ConfigParser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(BASE_DIR / filename, encoding="utf-8")
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db

if __name__ == "__main__":
    print(config())