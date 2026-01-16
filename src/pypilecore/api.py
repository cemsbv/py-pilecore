import logging
from time import sleep
from typing import Literal, overload

from nuclei.client import NucleiClient
from requests import Response


def wait_until_ticket_is_ready(
    client: NucleiClient, ticket: Response, verbose: bool = False
) -> None:
    if verbose:
        logging.info("Waiting for ticket to be ready")

    if ticket.status_code != 200:
        raise RuntimeError(rf"{ticket.text}")

    if verbose:
        logging.info("Ticket status: OK")
        logging.info(f"Ticket ID: {ticket.json()['id']}")

    status = "STARTED"
    sleep_time = 0.05

    while status in ["PENDING", "STARTED", "RETRY"]:
        # Exponential backoff
        sleep_time = min(sleep_time * 2, 10)
        if verbose:
            logging.info("Sleeping for %s seconds", sleep_time)
        sleep(sleep_time)

        # Get the status of the ticket
        if verbose:
            logging.info("Polling ticket status")
        status_response = client.call_endpoint(
            "PileCore",
            "/get-task-status",
            version="v4",
            schema=ticket.json(),
            return_response=True,
        )

        # Check if the status response is OK
        if status_response.status_code != 200:
            raise RuntimeError(rf"{status_response.text}")

        status = status_response.json()["state"]
        if verbose:
            logging.info("Ticket status: %s", status)

    # If the status is FAILURE, raise an error
    if status == "FAILURE":
        # Get the task-status failure message
        failure_message = status_response.json()["msg"]

        # Try to get the task-result failure message
        try:
            result_response = client.call_endpoint(
                "PileCore",
                "/get-task-result",
                version="v4",
                schema=ticket.json(),
                return_response=True,
            )
            failure_message = result_response.text

        # Raise the obtained failure message
        finally:
            raise RuntimeError(failure_message)


@overload
def get_task_result_pipeline(
    client: NucleiClient,
    endpoint: str,
    payload: dict,
    verbose: bool,
    response_type: Literal["dict"],
    save_failed_payload: bool,
    failed_payload_filename: str,
) -> dict: ...


@overload
def get_task_result_pipeline(
    client: NucleiClient,
    endpoint: str,
    payload: dict,
    verbose: bool,
    response_type: Literal["bytes"],
    save_failed_payload: bool,
    failed_payload_filename: str,
) -> bytes: ...


def get_task_result_pipeline(
    client: NucleiClient,
    endpoint: str,
    payload: dict,
    verbose: bool = False,
    response_type: Literal["dict", "bytes"] = "dict",
    save_failed_payload: bool = False,
    failed_payload_filename: str = "debug_payload.json",
) -> dict | bytes:
    """
    Execute a task and return the result.

    Parameters
    ----------
    client: NucleiClient
        client object created by [nuclei](https://github.com/cemsbv/nuclei)
    endpoint: str
        the endpoint to call
    payload: dict
        the payload of the request
    verbose: bool
        if True, print additional information to the console
    save_failed_payload: bool
        if True, save the payload to a file in case of failure
    failed_payload_filename: str
        the name of the file to save the failed payload to
    """

    try:
        ticket = client.call_endpoint(
            "PileCore",
            endpoint,
            version="v4",
            schema=payload,
            return_response=True,
        )

        wait_until_ticket_is_ready(client=client, ticket=ticket, verbose=verbose)

        response = client.call_endpoint(
            "PileCore", "/get-task-result", version="v4", schema=ticket.json()
        )
    except Exception as e:
        if save_failed_payload:
            # In case of failure, save the payload to a file for debugging
            with open(failed_payload_filename, "w") as f:
                from nuclei.client.utils import serialize_json_string

                f.write(serialize_json_string(payload))
        raise e

    return response


def get_multi_cpt_api_result(
    client: NucleiClient,
    payload: dict,
    verbose: bool = False,
    save_failed_payload: bool = False,
    failed_payload_filename: str = "pilecore_multi_cpt_result_debug_payload.json",
) -> dict:
    """
    Wrapper around the PileCore endpoint "/bearing/multiple-cpts/results".

    Parameters
    ----------
    client: NucleiClient
        client object created by [nuclei](https://github.com/cemsbv/nuclei)
    payload: dict
        the payload of the request, can be created by calling `create_grouper_payload()`
    verbose: bool
        if True, print additional information to the console
    """
    logging.info(
        "Calculating bearing capacities... \n"
        "Depending on the amount of pile tip levels and CPT's this can take a while."
    )
    return get_task_result_pipeline(
        client=client,
        endpoint="/bearing/multiple-cpts/results",
        payload=payload,
        verbose=verbose,
        response_type="dict",
        save_failed_payload=save_failed_payload,
        failed_payload_filename=failed_payload_filename,
    )


def get_multi_cpt_api_report(
    client: NucleiClient,
    payload: dict,
    verbose: bool = False,
    save_failed_payload: bool = False,
    failed_payload_filename: str = "pilecore_multi_cpt_report_debug_payload.json",
) -> bytes:
    """
    Wrapper around the PileCore endpoint "/bearing/multiple-cpts/report".

    Parameters
    ----------
    client: NucleiClient
        client object created by [nuclei](https://github.com/cemsbv/nuclei)
    payload: dict
        the payload of the request, can be created by calling `create_grouper_payload()`
    verbose: bool
        if True, print additional information to the console
    """
    logging.info(
        "Generate report... \n"
        "Depending on the amount of pile tip levels and CPT's this can take a while."
    )
    return get_task_result_pipeline(
        client=client,
        endpoint="/bearing/multiple-cpts/report",
        payload=payload,
        verbose=verbose,
        response_type="bytes",
        save_failed_payload=save_failed_payload,
        failed_payload_filename=failed_payload_filename,
    )


def get_groups_api_result(
    client: NucleiClient,
    payload: dict,
    verbose: bool = False,
    save_failed_payload: bool = False,
    failed_payload_filename: str = "pilecore_group_cpts_debug_payload.json",
) -> dict:
    """
    Wrapper around the PileCore endpoint "/grouper/group_cpts".

    Parameters
    ----------
    client: NucleiClient
        client object created by [nuclei](https://github.com/cemsbv/nuclei)
    payload: dict
        the payload of the request, can be created by calling `create_grouper_payload()`
    verbose: bool
        if True, print additional information to the console
    """
    logging.info(
        "Finding groups... \n"
        "Depending on the amount of pile tip levels and CPT's this can take a while."
    )
    return get_task_result_pipeline(
        client=client,
        endpoint="/grouper/group-cpts",
        payload=payload,
        verbose=verbose,
        response_type="dict",
        save_failed_payload=save_failed_payload,
        failed_payload_filename=failed_payload_filename,
    )


def get_groups_api_report(
    client: NucleiClient,
    payload: dict,
    verbose: bool = False,
    save_failed_payload: bool = False,
    failed_payload_filename: str = "pilecore_grouper_report_debug_payload.json",
) -> bytes:
    """
    Wrapper around the PileCore endpoint "/grouper/generate_grouper_report".

    Parameters
    ----------
    client: NucleiClient
        client object created by [nuclei](https://github.com/cemsbv/nuclei)
    payload: dict
        the payload of the request, can be created by calling `create_grouper_report_payload()`
    verbose: bool
        if True, print additional information to the console
    """
    logging.info(
        "Generate report... \n"
        "Depending on the amount of pile tip levels and CPT's this can take a while."
    )
    return get_task_result_pipeline(
        client=client,
        endpoint="/grouper/generate-grouper-report",
        payload=payload,
        verbose=verbose,
        response_type="bytes",
        save_failed_payload=save_failed_payload,
        failed_payload_filename=failed_payload_filename,
    )


def get_multi_cpt_api_result_tension(
    client: NucleiClient,
    payload: dict,
    verbose: bool = False,
    standard: Literal["NEN9997-1", "CUR236"] = "NEN9997-1",
    save_failed_payload: bool = False,
    failed_payload_filename: str = "pilecore_multi_cpt_tension_result_debug_payload.json",
) -> dict:
    """
    Wrapper around the PileCore endpoint "/uplift/[nen or cur]/multiple-cpts/results".

    Parameters
    ----------
    client: NucleiClient
        client object created by [nuclei](https://github.com/cemsbv/nuclei)
    payload: dict
        the payload of the request, can be created by calling `create_grouper_payload()`
    verbose: bool
        if True, print additional information to the console
    standard: str
        Norm used to calculate bearing capacities
    """
    logging.info(
        "Calculating bearing capacities... \n"
        "Depending on the amount of pile tip levels and CPT's this can take a while."
    )
    if standard == "NEN9997-1":
        endpoint = "/uplift/nen/multiple-cpts/results"
    else:
        endpoint = "/uplift/cur/multiple-cpts/results"
        payload.pop("construction_sequence", None)

    return get_task_result_pipeline(
        client=client,
        endpoint=endpoint,
        payload=payload,
        verbose=verbose,
        response_type="dict",
        save_failed_payload=save_failed_payload,
        failed_payload_filename=failed_payload_filename,
    )


def get_multi_cpt_api_report_tension(
    client: NucleiClient,
    payload: dict,
    verbose: bool = False,
    standard: Literal["NEN9997-1", "CUR236"] = "NEN9997-1",
    save_failed_payload: bool = False,
    failed_payload_filename: str = "pilecore_multi_cpt_tension_report_debug_payload.json",
) -> bytes:
    """
    Wrapper around the PileCore endpoint "/uplift/[nen or cur]/multiple-cpts/report".

    Parameters
    ----------
    client: NucleiClient
        client object created by [nuclei](https://github.com/cemsbv/nuclei)
    payload: dict
        the payload of the request, can be created by calling `create_grouper_payload()`
    verbose: bool
        if True, print additional information to the console
    standard: str
        Norm used to calculate bearing capacities
    """
    logging.info(
        "Generate report... \n"
        "Depending on the amount of pile tip levels and CPT's this can take a while."
    )

    if standard == "NEN9997-1":
        endpoint = "/uplift/nen/multiple-cpts/report"
    else:
        endpoint = "/uplift/cur/multiple-cpts/report"
        payload.pop("construction_sequence", None)

    return get_task_result_pipeline(
        client=client,
        endpoint=endpoint,
        payload=payload,
        verbose=verbose,
        response_type="bytes",
        save_failed_payload=save_failed_payload,
        failed_payload_filename=failed_payload_filename,
    )
