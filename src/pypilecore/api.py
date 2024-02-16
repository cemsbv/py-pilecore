import logging
from time import sleep

from nuclei.client import NucleiClient
from requests import Response


def wait_until_ticket_is_ready(client: NucleiClient, ticket: Response) -> None:
    if ticket.status_code != 200:
        raise RuntimeError(rf"{ticket.text}")

    status = "STARTED"
    sleep_time = 0.05
    while status in ["PENDING", "STARTED", "RETRY"]:
        sleep_time = min(sleep_time * 2, 10)
        sleep(sleep_time)
        response = client.call_endpoint(
            "PileCore", "/get-task-status", schema=ticket.json(), return_response=True
        )
        if response.status_code != 200:
            raise RuntimeError(rf"{response.text}")
        status = response.json()["state"]

    if status == "FAILURE":
        raise RuntimeError(
            f'Status: {response.json()["msg"]}. {response.json()["msg"]}'
        )


def get_multi_cpt_api_result(client: NucleiClient, payload: dict) -> dict:
    """
    Wrapper around the PileCore endpoint "/compression/multiple-cpts/results".

    Parameters
    ----------
    client: NucleiClient
        client object created by [nuclei](https://github.com/cemsbv/nuclei)
    payload: dict
        the payload of the request, can be created by calling `create_grouper_payload()`
    """
    logging.info(
        "Calculating bearing capacities... \n"
        "Depending on the amount of pile tip levels and CPT's this can take a while."
    )
    ticket = client.call_endpoint(
        "PileCore",
        "/compression/multiple-cpts/results",
        schema=payload,
        return_response=True,
    )

    wait_until_ticket_is_ready(client=client, ticket=ticket)

    return client.call_endpoint("PileCore", "/get-task-result", schema=ticket.json())


def get_multi_cpt_api_report(client: NucleiClient, payload: dict) -> dict:
    """
    Wrapper around the PileCore endpoint "/compression/multiple-cpts/report".

    Parameters
    ----------
    client: NucleiClient
        client object created by [nuclei](https://github.com/cemsbv/nuclei)
    payload: dict
        the payload of the request, can be created by calling `create_grouper_payload()`
    """
    logging.info(
        "Generate report... \n"
        "Depending on the amount of pile tip levels and CPT's this can take a while."
    )
    ticket = client.call_endpoint(
        "PileCore",
        "/compression/multiple-cpts/report",
        schema=payload,
        return_response=True,
    )
    wait_until_ticket_is_ready(client=client, ticket=ticket)

    return client.call_endpoint("PileCore", "/get-task-result", schema=ticket.json())


def get_groups_api_result(client: NucleiClient, payload: dict) -> dict:
    """
    Wrapper around the PileCore endpoint "/grouper/group_cpts".

    Parameters
    ----------
    client: NucleiClient
        client object created by [nuclei](https://github.com/cemsbv/nuclei)
    payload: dict
        the payload of the request, can be created by calling `create_grouper_payload()`
    """
    logging.info(
        "Finding groups... \n"
        "Depending on the amount of pile tip levels and CPT's this can take a while."
    )
    ticket = client.call_endpoint(
        "PileCore",
        "/grouper/group_cpts",
        schema=payload,
        return_response=True,
    )

    wait_until_ticket_is_ready(client=client, ticket=ticket)

    return client.call_endpoint("PileCore", "/get-task-result", schema=ticket.json())


def get_optimize_groups_api_result(client: NucleiClient, payload: dict) -> dict:
    """
    Wrapper around the PileCore endpoint "/grouper/optimize_groups".

    Parameters
    ----------
    client: NucleiClient
        client object created by [nuclei](https://github.com/cemsbv/nuclei)
    payload: dict
        the payload of the request, can be created by calling `create_grouper_payload()`
    """
    logging.info(
        "Optimize groups... \n"
        "Depending on the amount of pile tip levels and CPT's this can take a while."
    )
    ticket = client.call_endpoint(
        "PileCore",
        "/grouper/optimize_groups",
        schema=payload,
        return_response=True,
    )

    wait_until_ticket_is_ready(client=client, ticket=ticket)

    return client.call_endpoint("PileCore", "/get-task-result", schema=ticket.json())


def get_groups_api_report(client: NucleiClient, payload: dict) -> bytes:
    """
    Wrapper around the PileCore endpoint "/grouper/generate_grouper_report".

    Parameters
    ----------
    client: NucleiClient
        client object created by [nuclei](https://github.com/cemsbv/nuclei)
    payload: dict
        the payload of the request, can be created by calling `create_grouper_report_payload()`
    """
    logging.info(
        "Generate report... \n"
        "Depending on the amount of pile tip levels and CPT's this can take a while."
    )
    ticket = client.call_endpoint(
        "PileCore",
        "/grouper/generate_grouper_report",
        schema=payload,
        return_response=True,
    )

    wait_until_ticket_is_ready(client=client, ticket=ticket)

    return client.call_endpoint("PileCore", "/get-task-result", schema=ticket.json())
