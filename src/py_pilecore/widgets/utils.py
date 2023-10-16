from __future__ import annotations

import json
import os
import urllib

import ipykernel

try:
    from jupyter_server import serverapp as app
except ImportError:
    try:
        from notebook import notebookapp as app
    except ImportError:
        app = None


def get_valid_basename(filename: str) -> str:
    filename = filename.replace(" ", "_")
    return os.path.basename(filename).split(".")[0]


# The notebook / jupyterlab solution is based on:
# https://stackoverflow.com/questions/12544056/how-do-i-get-the-current-ipython-jupyter-notebook-name/52187331#52187331


# The vscode solution is based on:
# https://stackoverflow.com/questions/70219603/get-jupyter-notebook-name-while-using-vscode
def get_notebook_filename(notebook_globals: dict | None) -> str | None:
    """Returns the filename of the Notebook or None if it cannot be determined
    NOTE: works only when the security is token-based or there is also no password
    """
    if app is not None:
        connection_file = os.path.basename(ipykernel.get_connection_file())
        kernel_id = connection_file.split("-", 1)[1].split(".")[0]

        for srv in app.list_running_servers():
            try:
                if (
                    srv["token"] == "" and not srv["password"]
                ):  # No token and no password, ahem...
                    req = urllib.request.urlopen(srv["url"] + "api/sessions")
                else:
                    req = urllib.request.urlopen(
                        srv["url"] + "api/sessions?token=" + srv["token"]
                    )
                sessions = json.load(req)
                for sess in sessions:
                    if sess["kernel"]["id"] == kernel_id:
                        return get_valid_basename(sess["notebook"]["path"])
            except KeyError:
                pass  # There may be stale entries in the runtime directory

    if notebook_globals is not None and "__vsc_ipynb_file__" in notebook_globals:
        return get_valid_basename(notebook_globals["__vsc_ipynb_file__"])

    return None
