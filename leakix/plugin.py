from enum import Enum

from serde import Model, fields


class APIResult(Model):
    name: fields.Str()  # type: ignore[valid-type]
    description: fields.Str()  # type: ignore[valid-type]


class Plugin(Enum):
    """
    The list of plugins can be found on https://leakix.net/plugins. Some plugins are only available to paid users. Have
    a look at https://leakix.net/pricing for a detailled list.
    """

    ApacheStatusHttpPlugin = "ApacheStatusHttpPlugin"
    BitbucketPlugin = "BitbucketPlugin"
    CheckMkPlugin = "CheckMkPlugin"
    ConfigJsonHttp = "ConfigJsonHttp"
    ConfluenceVersionIssue = "ConfluenceVersionIssue"
    Consul = "Consul"
    CouchDbOpenPlugin = "CouchDbOpenPlugin"
    DeadMon = "DeadMon"
    DockerRegistryHttpPlugin = "DockerRegistryHttpPlugin"
    DotDsStoreOpenPlugin = "DotDsStoreOpenPlugin"
    DotEnvConfigPlugin = "DotEnvConfigPlugin"
    ElasticSearchOpenPlugin = "ElasticSearchOpenPlugin"
    ExchangeVersion = "ExchangeVersion"
    FortiOSPlugin = "FortiOSPlugin"
    GitConfigHttpPlugin = "GitConfigHttpPlugin"
    GrafanaOpenPlugin = "GrafanaOpenPlugin"
    HiSiliconDVR = "HiSiliconDVR"
    HttpNTLM = "HttpNTLM"
    JenkinsOpenPlugin = "JenkinsOpenPlugin"
    JiraPlugin = "JiraPlugin"
    KafkaOpenPlugin = "KafkaOpenPlugin"
    LaravelTelescopeHttpPlugin = "LaravelTelescopeHttpPlugin"
    Log4JOpportunistic = "Log4JOpportunistic"
    MetabaseHttpPlugin = "MetabaseHttpPlugin"
    MongoOpenPlugin = "MongoOpenPlugin"
    MysqlOpenPlugin = "MysqlOpenPlugin"
    PaloAltoPlugin = "PaloAltoPlugin"
    PhpInfoHttpPlugin = "PhpInfoHttpPlugin"
    PhpStdinPlugin = "PhpStdinPlugin"
    ProxyOpenPlugin = "ProxyOpenPlugin"
    QnapVersion = "QnapVersion"
    RedisOpenPlugin = "RedisOpenPlugin"
    SmbPlugin = "SmbPlugin"
    SonarQubePlugin = "SonarQubePlugin"
    SonicWallSMAPlugin = "SonicWallSMAPlugin"
    SophosPlugin = "SophosPlugin"
    SymfonyProfilerPlugin = "SymfonyProfilerPlugin"
    SymfonyVerbosePlugin = "SymfonyVerbosePlugin"
    TraversalHttpPlugin = "TraversalHttpPlugin"
    veeaml9 = "veeaml9"
    WpUserEnumHttp = "WpUserEnumHttp"
    YiiDebugPlugin = "YiiDebugPlugin"
    ZimbraPlugin = "ZimbraPlugin"
    ZookeeperOpenPlugin = "ZookeeperOpenPlugin"
    ZyxelVersion = "ZyxelVersion"
