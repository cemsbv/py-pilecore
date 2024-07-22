import logging
from time import sleep

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
            version="v3",
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
                version="v3",
                schema=ticket.json(),
                return_response=True,
            )
            failure_message = result_response.text

        # Raise the obtained failure message
        finally:
            raise RuntimeError(failure_message)


def get_multi_cpt_api_result(
    client: NucleiClient, payload: dict, verbose: bool = False
) -> dict:
    """
    Wrapper around the PileCore endpoint "/compression/multiple-cpts/results".

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
    ticket = client.call_endpoint(
        "PileCore",
        "/compression/multiple-cpts/results",
        version="v3",
        schema=payload,
        return_response=True,
    )

    wait_until_ticket_is_ready(client=client, ticket=ticket, verbose=verbose)

    return client.call_endpoint(
        "PileCore", "/get-task-result", version="v3", schema=ticket.json()
    )


def get_multi_cpt_api_report(
    client: NucleiClient, payload: dict, verbose: bool = False
) -> dict:
    """
    Wrapper around the PileCore endpoint "/compression/multiple-cpts/report".

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
    ticket = client.call_endpoint(
        "PileCore",
        "/compression/multiple-cpts/report",
        version="v3",
        schema=payload,
        return_response=True,
    )
    wait_until_ticket_is_ready(client=client, ticket=ticket, verbose=verbose)

    return client.call_endpoint(
        "PileCore", "/get-task-result", version="v3", schema=ticket.json()
    )


def get_groups_api_result(
    client: NucleiClient, payload: dict, verbose: bool = False
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
    ticket = client.call_endpoint(
        "PileCore",
        "/grouper/group_cpts",
        version="v3",
        schema=payload,
        return_response=True,
    )

    wait_until_ticket_is_ready(client=client, ticket=ticket, verbose=verbose)

    return client.call_endpoint(
        "PileCore", "/get-task-result", version="v3", schema=ticket.json()
    )


def get_optimize_groups_api_result(
    client: NucleiClient, payload: dict, verbose: bool = False
) -> dict:
    """
    Wrapper around the PileCore endpoint "/grouper/optimize_groups".

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
        "Optimize groups... \n"
        "Depending on the amount of pile tip levels and CPT's this can take a while."
    )
    ticket = client.call_endpoint(
        "PileCore",
        "/grouper/optimize_groups",
        version="v3",
        schema=payload,
        return_response=True,
    )

    wait_until_ticket_is_ready(client=client, ticket=ticket, verbose=verbose)

    return client.call_endpoint(
        "PileCore", "/get-task-result", version="v3", schema=ticket.json()
    )


def get_groups_api_report(
    client: NucleiClient, payload: dict, verbose: bool = False
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
    ticket = client.call_endpoint(
        "PileCore",
        "/grouper/generate_grouper_report",
        version="v3",
        schema=payload,
        return_response=True,
    )

    wait_until_ticket_is_ready(client=client, ticket=ticket, verbose=verbose)

    return client.call_endpoint(
        "PileCore", "/get-task-result", version="v3", schema=ticket.json()
    )
