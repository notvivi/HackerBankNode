#Author: Tomanová Vilma
import socket

def send_tcp_command(host, port, command, timeout=5):
    """
    Opens TCP connection, sends command(s), receives full response.
    Returns decoded string.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))

            try:
                banner = s.recv(8192).decode("utf-8", errors="ignore")
            except socket.timeout:
                banner = ""

            s.sendall((command + "\n").encode("utf-8"))

            response = ""
            while True:
                try:
                    data = s.recv(4096)
                    if not data:
                        break
                    response += data.decode("utf-8", errors="ignore")
                except socket.timeout:
                    break

            return banner + response

    except socket.timeout:
        return "ERROR: Connection timeout"
    except Exception as e:
        return f"ERROR: {e}"
