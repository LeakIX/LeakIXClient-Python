# LeakIX Python Client

The official Python client for the [LeakIX](https://leakix.net) API, for
security research and reconnaissance. It provides a synchronous `Client`
and an asynchronous `AsyncClient`, a typed query builder, and typed
response models.

## Quick start

```bash
uv add leakix
```

```python
from leakix import Client, Scope

client = Client(api_key="<your-key>")
resp = client.search("+plugin:GitConfigHttpPlugin", scope=Scope.LEAK)
print(resp.json())
```

Get an API key from <https://leakix.net/settings>.

See the [API reference](reference.md) for the full surface.
