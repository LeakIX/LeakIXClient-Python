from datetime import datetime
from typing import Any

from serde.model import Model

class L9HttpEvent(Model):
    root: str
    url: str
    status: int
    length: int
    header: dict[str, str] | None
    title: str
    favicon_hash: str

class ServiceCredentials(Model):
    noauth: bool
    username: str
    password: str
    key: str
    raw: str | None

class SoftwareModule(Model):
    name: str
    version: str
    fingerprint: str

class Software(Model):
    name: str
    version: str
    os: str
    modules: list[SoftwareModule] | None
    fingerprint: str

class Certificate(Model):
    cn: str
    domain: list[str] | None
    fingerprint: str
    key_algo: str
    key_size: int
    issuer_name: str
    not_before: datetime
    not_after: datetime
    valid: bool

class GeoPoint(Model):
    lat: Any
    lon: Any

class GeoLocation(Model):
    continent_name: str | None
    region_iso_code: str | None
    city_name: str | None
    country_iso_code: str | None
    country_name: str | None
    region_name: str | None
    location: GeoPoint | None

class L9SSHEvent(Model):
    fingerprint: str
    version: int
    banner: str
    motd: str

class DatasetSummary(Model):
    rows: int
    files: int
    size: int
    collections: int
    infected: bool
    ransom_notes: list[str] | None

class L9LeakEvent(Model):
    stage: str
    type: str
    severity: str
    dataset: DatasetSummary

class L9SSLEvent(Model):
    detected: bool
    enabled: bool
    jarm: str
    cypher_suite: str
    version: str
    certificate: Certificate

class L9ServiceEvent(Model):
    credentials: ServiceCredentials
    software: Software

class Network(Model):
    organization_name: str
    asn: int
    network: str

class L9Event(Model):
    event_type: str
    event_source: str
    event_pipeline: list[str] | None
    event_fingerprint: str | None
    ip: str
    port: str
    host: str
    reverse: str
    mac: str | None
    vendor: str | None
    transport: list[str] | None
    protocol: str
    http: L9HttpEvent
    summary: str
    time: datetime
    ssl: L9SSLEvent | None
    ssh: L9SSHEvent
    service: L9ServiceEvent
    leak: L9LeakEvent | None
    tags: list[str] | None
    geoip: GeoLocation
    network: Network

class L9Aggregation(Model):
    summary: str | None
    ip: str
    resource_id: str
    open_ports: list[str]
    leak_count: int
    leak_event_count: int
    events: list[L9Event]
    plugins: list[str]
    geoip: GeoLocation
    network: Network
    creation_date: datetime
    update_date: datetime
    fresh: bool
