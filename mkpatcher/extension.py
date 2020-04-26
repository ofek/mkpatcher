import importlib
import logging
import os

from markdown import Extension
from markdown.preprocessors import Preprocessor

log = logging.getLogger(__name__)


class CompiledScript:
    def __init__(self, contents, name):
        self.contents = contents
        self.name = name
        self._code_object = None

    @property
    def compiled(self):
        if self._code_object is None:
            self._code_object = compile(self.contents, filename=self.name, mode='exec')

        return self._code_object


class LoadedScript:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(self.path).rsplit('.', 1)[0]
        self._patcher = None

    @property
    def patch(self):
        if self._patcher is None:
            spec = importlib.util.spec_from_file_location(self.name, self.path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            self._patcher = getattr(mod, 'patch', None)
            if not callable(self._patcher):
                log.error('Script `%s` has no callable named `patch`', self.path)
                self._patcher = lambda lines: None

        return self._patcher


class PatcherPreprocessor(Preprocessor):
    def __init__(self, config, md):
        self.raw_script = config.get('script', '')
        if self.raw_script:
            self.raw_script = CompiledScript(self.raw_script, 'script')

        self.scripts = []
        self.location = config.get('location', '')
        if self.location:
            self.location = os.path.normpath(self.location)

            if os.path.isfile(self.location):
                self.scripts.append(LoadedScript(self.location))
            elif os.path.isdir(self.location):
                for entry in sorted(os.listdir(self.location)):
                    path = os.path.join(self.location, entry)
                    if os.path.isfile(path):
                        self.scripts.append(LoadedScript(path))
            else:
                log.error('Unable to load script(s) from %s', self.location)

        super(PatcherPreprocessor, self).__init__()

    def run_raw_script(self, lines):
        local_vars = {'lines': lines}
        exec(self.raw_script.compiled, globals(), local_vars)

        return local_vars['lines']

    def run_scripts(self, lines):
        for script in self.scripts:
            new_lines = script.patch(lines)
            if new_lines:
                lines = new_lines

        return lines

    def run(self, lines):
        new_lines = list(lines)

        if self.raw_script:
            new_lines = self.run_raw_script(new_lines)
        elif self.scripts:
            new_lines = self.run_scripts(new_lines)

        return new_lines


class PatcherExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'script': ['', 'Raw code to execute - Default: ""'],
            'location': ['', 'Base path for script paths or path to a single script - Default: ""'],
        }

        super(PatcherExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        self.md = md
        md.registerExtension(self)
        config = self.getConfigs()
        patcher = PatcherPreprocessor(config, md)
        md.preprocessors.register(patcher, 'mkpatcher', 9000)


def makeExtension(*args, **kwargs):
    return PatcherExtension(*args, **kwargs)
