import socket

MCAST_GRP = "236.0.0.0"
MCAST_PORT = 3456


def udp_send(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.sendto(message.encode('utf-8'), (MCAST_GRP, MCAST_PORT))



