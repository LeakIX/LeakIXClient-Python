# LeakIX python client

[![PyPI version](https://img.shields.io/pypi/v/leakix)](https://pypi.org/project/leakix/)
[![Python versions](https://img.shields.io/pypi/pyversions/leakix)](https://pypi.org/project/leakix/)

Supported Python versions: 3.11, 3.12, 3.13, 3.14

Official LeakIX python client

## Install

```
pip install leakix
```

To run tests, use `make test`.

## Documentation

Docstrings are used to document the library.
Types are also used to inform the user on what type of objects the functions are
expecting.

Each API response is encoded in either a `SuccessResponse` object or a
`ErrorResponse`.
The methods `is_success()` or `is_error()` exist on each API response.
You can get the actual response by using the method `json()` on the response object.

The output are events described in
[l9format](https://github.com/LeakIX/l9format-python).
When you have an object of type `l9Event` (or the longer
`l9format.l9format.L9Event`), you can refer to
[L9Event](https://github.com/LeakIX/l9format-python/blob/main/l9format/l9format.py#L158)
model class for the available fields.

For instance, to access the IP of an object `event` of type `L9Event`, you can
use `event.ip`.

Each object can be transformed back into a Python dictionary/JSON using the method `to_dict()`.
For instance, for the response of the subdomains endpoint, you can get back individual JSON by using:

```python
def example_get_subdomains():
    response = CLIENT.get_subdomains("leakix.net")
    for subdomain in response.json():
        print(subdomain.to_dict())
```

## Support

Feel free to open an issue if you have any question.
You can also contact us on `support@leakix.net`.

If you need commercial support, have a look at https://leakix.net/plans.

## Examples

See the [example/](example/) directory for complete usage examples:

- [Sync client](example/example_client.py)
- [Async client](example/example_async_client.py)
