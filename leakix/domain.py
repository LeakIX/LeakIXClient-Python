from serde import Model, fields


class L9Subdomain(Model):
    subdomain: fields.Str()
    distinct_ips: fields.Int()
    last_seen: fields.DateTime()
