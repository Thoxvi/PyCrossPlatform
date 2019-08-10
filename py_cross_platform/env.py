import platform

__all__ = [
    "IS_LINUX",
    "IS_MAC",
    "IS_WIN",

    "DEV_NULL",
]

os_name = platform.system()
IS_LINUX = (os_name == "Linux")
IS_MAC = (os_name == "Darwin")
IS_WIN = (os_name == "Windows")

if IS_WIN:
    DEV_NULL = "nul"
else:
    DEV_NULL = "/dev/null"
