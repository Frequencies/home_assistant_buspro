"""Network helpers shared by Buspro setup and config flows."""

import socket


def local_ip_for_gateway(host, port):
    """Return the local IPv4 address selected for the gateway route."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as route_socket:
        route_socket.connect((host, port))
        return route_socket.getsockname()[0]
