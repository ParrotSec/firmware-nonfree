from debian_linux.config import ConfigParser, SchemaItemList, SchemaItemBoolean

class Config(dict):
    config_name = "defines"

    top_schemas = {
        'base': {
            'packages': SchemaItemList(),
        },
        'upstream': {
            'exclude': SchemaItemList()
        }
    }

    package_schemas = {
        'base': {
            'files': SchemaItemList(),
            'support': SchemaItemList(),
            'copy': SchemaItemBoolean(),
        }
    }

    def __init__(self):
        self._read_base()

    def _read_base(self):
        config = ConfigParser(self.top_schemas)
        config.read("debian/config/%s" % self.config_name)

        packages = config['base',]['packages']

        for section in iter(config):
            real = (section[-1],) + section[:-1]
            self[real] = config[section]

        for package in packages:
            self._read_package(package)

    def _read_package(self, package):
        config = ConfigParser(self.package_schemas)
        config.read("debian/config/%s/%s" % (package, self.config_name))

        for section in iter(config):
            if len(section) > 1:
                real = (section[-1], package, '_'.join(section[:-1]))
            else:
                real = (section[-1], package)
            s = self.get(real, {})
            s.update(config[section])
            self[real] = s
