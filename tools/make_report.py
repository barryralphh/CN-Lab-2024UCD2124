import os, glob, re
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image

NAME, ROLL = "Pradumn Yadav", "2024UCD2124"
SETUP = ("The network was built in software on an Ubuntu Linux machine. Each PC and router is a Linux network namespace, "
         "each switch is a Linux bridge, and cables are virtual Ethernet (veth) pairs. All commands were run live in a terminal window "
         "and the capture/analysis was done with the real Wireshark and tshark applications.")
EXPS = {
 "01": ("Understanding Network Commands",
        "To execute and understand 20 basic network commands.",
        "Network commands are used to inspect interfaces, addresses, routes, name resolution, open ports and reachability of a host. "
        "ip/ifconfig show interface configuration, ping/traceroute/tracepath test reachability and the path to a host, nslookup/dig/host query DNS, "
        "netstat/ss list sockets, arp/ip neigh show the ARP cache, curl/wget fetch web resources and nmap scans ports.",
        "Each of the 20 commands was run in a terminal on the Linux host and its output was captured.",
        "All 20 commands were executed and their output was observed, which shows how a host is configured and how to diagnose basic connectivity problems."),
 "02": ("Creating a Simple LAN with PCs and a Switch",
        "To create a simple Local Area Network with PCs and a switch and verify connectivity.",
        "A LAN connects hosts in the same IP subnet through a Layer-2 switch. Hosts find each other's MAC address with ARP and the switch learns which port each MAC address is on.",
        "Three PCs (pc1 192.168.10.11, pc2 192.168.10.12, pc3 192.168.10.13, all /24) were connected to one switch. IP addresses, switch ports, ping between all pairs, the ARP table and the switch MAC table were checked.",
        "All three PCs could reach each other; the ARP table and the switch MAC address table were populated as expected."),
 "03": ("Configuring a Router for Inter-network Communication",
        "To configure a router so that two different networks can communicate.",
        "A router forwards packets between different IP networks. Hosts use their default gateway for destinations outside their own subnet, and the router must have IP forwarding enabled.",
        "Two LANs, 10.0.1.0/24 (pc1) and 10.0.2.0/24 (pc2), were joined by a router (10.0.1.1 and 10.0.2.1). Ping was tried with forwarding disabled, then forwarding was enabled and ping, traceroute and the router table were checked.",
        "Communication between the two networks failed while forwarding was off and worked after it was enabled."),
 "04": ("Setting up a DHCP Server",
        "To set up a DHCP server that assigns IP addresses automatically.",
        "DHCP gives hosts an IP address, mask, gateway and DNS server automatically using Discover, Offer, Request and Acknowledge messages. The server keeps a lease for each client.",
        "A DHCP server (dnsmasq) on the router 10.0.1.1 was configured with the pool 10.0.1.100-150, gateway 10.0.1.1, DNS 8.8.8.8 and a 12 hour lease. Two clients requested addresses with dhclient and the leases and server log were checked.",
        "Both clients received addresses from the pool automatically and could ping each other."),
 "05": ("Static Routing",
        "To configure static routes on routers to control the path of network traffic.",
        "A static route is entered manually on a router and tells it which next hop to use for a destination network. Without routes to remote networks, packets cannot be delivered.",
        "Three routers R1, R2 and R3 were connected. Routing tables were checked, ping failed without routes, static routes were added on each router, ping and traceroute were verified, and the path was then changed to the direct R1-R3 link.",
        "Ping failed without routes and worked after static routes were added. The traffic path changed when the static route was changed."),
 "06": ("Network Address Translation (NAT)",
        "To understand how NAT lets private addresses communicate with an external network.",
        "NAT (masquerading) replaces the private source address of outgoing packets with the router's public address and keeps a translation table so replies can be sent back to the right host.",
        "A private host pc1 (192.168.1.10) reaches an external server (203.0.113.10) through a router whose outside address is 203.0.113.2. Ping and HTTP were tested without and with an iptables MASQUERADE rule, and the server log and translation table were examined.",
        "With NAT enabled the server saw the router's public address instead of the private one, and the translation table showed the active connections."),
 "07": ("Wireshark: Interface and Live Capture",
        "To become familiar with the Wireshark interface and capture and filter network traffic.",
        "Wireshark captures packets from a network interface and shows them with protocol decoding. Display filters such as icmp or tcp.port==8080 select the packets of interest.",
        "Traffic (ping and HTTP) was captured on the switch of the LAN, then opened in Wireshark and tshark. Capture details, the protocol hierarchy and filters for ICMP and TCP port 8080 were used.",
        "The capture was filtered by protocol and port, and packet details were inspected layer by layer in Wireshark."),
 "08": ("Wireshark: ARP",
        "To understand how the Address Resolution Protocol maps IP addresses to MAC addresses.",
        "ARP broadcasts a request asking who has an IP address, and the owner replies with its MAC address. The result is stored in the ARP cache.",
        "The ARP cache was shown before and after a ping, the host MAC addresses were listed, and the ARP request and reply were captured and examined in Wireshark.",
        "A ping caused an ARP request (broadcast) and an ARP reply (unicast), after which the cache contained the MAC address."),
 "09": ("Wireshark: ICMP and Ping",
        "To learn about ICMP and how ping is used for network diagnostics.",
        "ICMP carries control and error messages. Ping uses echo request and echo reply; other messages include time exceeded (TTL expired) and destination unreachable.",
        "Echo requests/replies, a TTL expired message, a large packet and an unreachable network were generated, captured and examined in Wireshark.",
        "The different ICMP message types were observed with their type and code fields."),
 "10": ("Wireshark: DHCP and Switch MAC Address Learning",
        "To understand the DHCP process and how a switch learns MAC addresses.",
        "A switch learns the source MAC address of each frame and the port it came from, then forwards unicast frames only to the correct port instead of flooding. DHCP uses broadcast Discover/Request and Offer/Ack messages.",
        "The switch MAC table was shown before and after three hosts obtained addresses with DHCP; the DHCP exchange was captured and unicast traffic was checked not to reach the third host.",
        "The switch table filled with the host MAC addresses and ports, unicast frames were not flooded to other hosts, and the DHCP four-step exchange was seen in Wireshark."),
}

def img(doc, path, caption):
    im = Image.open(path)
    w = 6.4
    doc.add_picture(path, width=Inches(w))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph(caption)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].italic = True
    p.runs[0].font.size = Pt(9)

doc = Document()
doc.styles["Normal"].font.name = "Calibri"
doc.styles["Normal"].font.size = Pt(11)
for s in doc.sections:
    s.left_margin = s.right_margin = Inches(0.8)
doc.add_heading("Computer Networks Lab File", 0)
doc.add_paragraph("Name: %s" % NAME)
doc.add_paragraph("Roll No: %s" % ROLL)
doc.add_heading("Index", 1)
t = doc.add_table(rows=1, cols=2)
t.style = "Light Grid Accent 1"
t.rows[0].cells[0].text = "Exp. No."
t.rows[0].cells[1].text = "Name of the Experiment"
for k, v in EXPS.items():
    r = t.add_row().cells
    r[0].text = str(int(k))
    r[1].text = v[0]

fig = 0
for k, (title, aim, theory, proc, concl) in EXPS.items():
    doc.add_page_break()
    doc.add_heading("Experiment %d: %s" % (int(k), title), 1)
    doc.add_heading("Aim", 2); doc.add_paragraph(aim)
    doc.add_heading("Theory", 2); doc.add_paragraph(theory)
    doc.add_heading("Setup and Procedure", 2)
    if k != "01":
        doc.add_paragraph(SETUP)
    doc.add_paragraph(proc)
    doc.add_heading("Output and Screenshots", 2)
    d = "exp%s/out" % k
    shots = sorted(glob.glob(d + "/[0-9][0-9]_*.png")) + sorted(glob.glob(d + "/WS_*.png"))
    for p in shots:
        fig += 1
        base = os.path.basename(p)
        txt = p[:-4] + ".txt"
        if base.startswith("WS_"):
            cap = "Figure %d: Wireshark - %s" % (fig, base[3:-4].replace("_", " "))
        elif os.path.exists(txt):
            first = open(txt, errors="replace").readline().strip()
            cap = "Figure %d: %s" % (fig, first.split("$", 1)[-1].strip()[:110])
        else:
            cap = "Figure %d: %s" % (fig, base[:-4])
        img(doc, p, cap)
    doc.add_heading("Conclusion", 2); doc.add_paragraph(concl)

os.makedirs("report", exist_ok=True)
doc.save("report/CN_Lab_Report_%s.docx" % ROLL)
print("report saved, figures:", fig)
