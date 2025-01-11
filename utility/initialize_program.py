"""Initialize everything here.

All things that will be done on beginning of the startup
will be put here.
"""
from os import environ, mkdir, listdir, remove
from os.path import isdir, join


# ======= HANDLE ENVIRONMENT ==========
# hide pygame shameless advertisement
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

# hide google annoying warning of grpc
# WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
# E0000 00:00:1736602988.212412   78941 init.cc:232] grpc_wait_for_shutdown_with_timeout() timed out.
environ["GRPC_VERBOSITY"] = "ERROR"
environ["GLOG_minloglevel"] = "2"

# ======= HANDLE CACHE =========
# create cache folder
if not isdir("cache"):
    mkdir("cache")

# delete all files in cache
# TODO: Have some proper cache handling
cache_files = listdir("cache/")
for cache_file in cache_files:
    cache_file_path = join("cache", cache_file)
    remove(cache_file_path)
