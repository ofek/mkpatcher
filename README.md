# mkpatcher

`mkpatcher` is a Python-Markdown extension allowing arbitrary scripts to modify MkDocs input files.

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
  - [Raw script](#raw-script)
  - [Scripts on filesystem](#scripts-on-filesystem)
- [License](#license)

## Installation

1. `pip install mkpatcher`
1. Include the extension in your `mkdocs.yml` config file:

    ```yaml
    ...
    markdown_extensions:
      - mkpatcher:
          ...
    ```

## Usage

This extension works as a pre-processor and will allow modifying the raw lines of Markdown before any other extension runs.

### Raw script

The `script` option takes arbitrary Python code and will provide the Markdown lines as a variable named `lines`.

You can modify the lines directly:

```yaml
...
markdown_extensions:
  - mkpatcher:
      script: |
        lines.extend(('', 'some footer', ''))
```

or you can shadow the variable:

```yaml
...
markdown_extensions:
  ...
  - mkpatcher:
      script: |
        lines = ['entirely', 'new']
        lines.append('markdown')
```

### Scripts on filesystem

The `location` option takes a path to either a single Python file or a directory containing multiple Python files.
If the location refers to a directory, the scripts will be loaded and eventually executed in lexicographical order
based on file names.

Each script must define a callable object named `patch` that accepts a single parameter which will be the Markdown lines.

You can modify the lines directly:

```python
def patch(lines):
    lines.extend(('', 'some footer', ''))
```

or you can return new lines:

```python
def patch(lines):
    new_lines = ['entirely', 'new']
    new_lines.append('markdown')
    return new_lines
```

## License

`mkpatcher` is distributed under the terms of both

- [Apache License, Version 2.0](https://choosealicense.com/licenses/apache-2.0)
- [MIT License](https://choosealicense.com/licenses/mit)

at your option.
