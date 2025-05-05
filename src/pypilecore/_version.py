from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("py-pilecore")
# during CI
except PackageNotFoundError:
    __version__ = "1.1.1"
