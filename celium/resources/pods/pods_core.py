from typing import Any

from celium.models.executor import ExecutorFilterQuery, Executor
from celium.utils.machine import get_corrected_machine_names


class _PodsCore:
    ENDPOINT = "/pods"
    EXECUTORS_ENDPOINT = "/executors"

    def _list_executors_params(self, filter_query: ExecutorFilterQuery | dict | None = None) -> tuple[list[Any], dict[str, Any]]:
        if isinstance(filter_query, dict):
            filter_query = ExecutorFilterQuery.model_validate(filter_query)
        # Fix machine names
        params = filter_query.model_dump(mode='json', exclude_none=True) if filter_query else None
        if params and "machine_names" in params:
            corrected_machines = get_corrected_machine_names(params["machine_names"])
            if len(corrected_machines) > 0:
                params["machine_names"] = ",".join(corrected_machines)
        return (
            ["GET", self.EXECUTORS_ENDPOINT],
            { "params": params }
        )
    
    def _parse_list_executors_response(self, data: list[dict[str, Any]]) -> list[Executor]:
        return sorted([Executor.model_validate(r) for r in data], key=lambda x: x.uptime_in_minutes or 0, reverse=True)