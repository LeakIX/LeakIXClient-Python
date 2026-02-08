import json
from datetime import datetime

import fire
from decouple import config

from leakix import Client
from leakix.field import Operator, UpdateDateField
from leakix.query import MustQuery, RawQuery

API_KEY = config("API_KEY")
DATETIME_FORMAT = "%Y-%m-%d"


class CLI:
    def bulk_export_to_json(
        self,
        query: str,
        filename: str,
        before: str | None = None,
        after: str | None = None,
    ):
        client = Client(api_key=API_KEY)

        queries = []
        queries.append(RawQuery(query))
        if before is not None:
            before_dt = datetime.strptime(before, DATETIME_FORMAT)
            before_dt_field = UpdateDateField(
                before_dt, operator=Operator.StrictlyGreater
            )
            queries.append(MustQuery(before_dt_field))
        if after is not None:
            after_dt = datetime.strptime(after, DATETIME_FORMAT)
            after_dt_field = UpdateDateField(
                after_dt, operator=Operator.StrictlySmaller
            )
            queries.append(MustQuery(after_dt_field))
        response = client.bulk_export(queries)
        if response.is_success():
            res = []
            for j in response.json():
                res.append(j.to_dict())
            with open(filename, "w") as f:
                f.write(json.dumps(res))
        else:
            raise Exception(
                "API error (code = %d, message = %s)"
                % (response.status_code(), response.json())
            )


if __name__ == "__main__":
    fire.Fire(CLI)
