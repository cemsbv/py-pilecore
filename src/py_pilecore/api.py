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
        raise RuntimeError(f'{response.json()["msg"]}\n{response.json()["traceback"]}')


def get_multi_cpt_api_result(client: NucleiClient, payload: dict) -> dict:
    ticket = client.call_endpoint(
        "PileCore",
        "/compression/multiple-cpts/results",
        schema=payload,
        return_response=True,
    )

    wait_until_ticket_is_ready(client=client, ticket=ticket)

    return client.call_endpoint("PileCore", "/get-task-result", schema=ticket.json())


def get_multi_cpt_api_report(client: NucleiClient, payload: dict) -> dict:
    ticket = client.call_endpoint(
        "PileCore",
        "/compression/multiple-cpts/report",
        schema=payload,
        return_response=True,
    )
    wait_until_ticket_is_ready(client=client, ticket=ticket)

    return client.call_endpoint("PileCore", "/get-task-result", schema=ticket.json())
