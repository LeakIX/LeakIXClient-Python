## MISC executables

### CLI - Command Line Interface

This is a WIP CLI, unreleased at the moment.

For a maintained CLI, have a look at
[LeakPy](https://github.com/Chocapikk/LeakPy).

Credits to the original author.

#### Examples

```
poetry run python \
    executable/cli.py \
      bulk_export_to_json \
      --before="2023-10-16" \
      --after="2023-10-18" \
      --query="+plugin:\"IOSEXPlugin\"" \
      --filename=export.json
```
