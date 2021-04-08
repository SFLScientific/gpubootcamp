#!/usr/bin/env python3

import os, sys
from IPython import embed_kernel
from jupyter_client.connect import write_connection_file

shell_port = int(os.environ.get("SHELL_PORT", 5001))
iopub_port = int(os.environ.get("IOPUB_PORT", 5002))
stdin_port = int(os.environ.get("STDIN_PORT", 5003))
control_port = int(os.environ.get("CONTROL_PORT", 5004))
hb_port = int(os.environ.get("HB_PORT", 5005))
kernel_key_path = os.environ.get("KERNEL_KEY_PATH", "/tmp/kernel-key")
kernel_name = os.environ.get("KERNEL_NAME", "")
try:
    kernel_id = sys.argv[1]
except IndexError:
    msg = "Kernel ID needs to be specified as first argument"
    raise RuntimeError(msg)

ip = "0.0.0.0"

if not kernel_id:
    msg = "Unable to determine kernel id. Please use KERNEL_ID variable"
    raise RuntimeError(msg)

connection_file = "/tmp/kernel-{}.json".format(kernel_id)

if not os.path.exists(kernel_key_path):
    msg = "Unable to find signature creadentials for running kernel. Please use KERNEL_KEY_PATH variable"
    raise RuntimeError(msg)

kernel_key_file = kernel_key_path + "/key"

if not os.path.exists(kernel_key_file):
    msg = "Unable to find {}".format(kernel_key_file)
    raise RuntimeError(msg)

with open(kernel_key_file, "rb") as f:
    key = f.readline()

write_connection_file(
    fname=connection_file,
    ip=ip,
    key=key,
    shell_port=shell_port,
    iopub_port=iopub_port,
    stdin_port=stdin_port,
    hb_port=hb_port,
    control_port=control_port
)

embed_kernel(connection_file=connection_file, ip=ip)
