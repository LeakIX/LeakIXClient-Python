from serde import Model, fields


class L9Subdomain(Model):
    subdomain: fields.Str()  # type: ignore[valid-type]
    distinct_ips: fields.Int()  # type: ignore[valid-type]
    last_seen: fields.DateTime()  # type: ignore[valid-type]
