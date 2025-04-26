import socket
import concurrent.futures
from typing import List, Dict

class PortScanner:
    def __init__(self, timeout: float = 1.0):
        self.timeout = timeout
        self.common_ports = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL"
        }

    def scan_port(self, host: str, port: int) -> Dict:
        """Scan a single port"""
        result = {"port": port, "open": False, "service": "unknown"}
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                if s.connect_ex((host, port)) == 0:
                    result["open"] = True
                    result["service"] = self.common_ports.get(port, "unknown")
            return result
        except Exception as e:
            return {"port": port, "open": False, "error": str(e)}

    def scan_range(self, host: str, start_port: int, end_port: int) -> List[Dict]:
        """Scan a range of ports"""
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(self.scan_port, host, port) 
                     for port in range(start_port, end_port + 1)]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        return sorted(results, key=lambda x: x["port"])

    def scan_common_ports(self, host: str) -> List[Dict]:
        """Scan commonly used ports"""
        return [self.scan_port(host, port) for port in self.common_ports.keys()]