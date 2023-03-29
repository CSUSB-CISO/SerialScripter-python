import nmap
import networkx as nx
import matplotlib.pyplot as plt

# Run Nmap scan and parse results
nm = nmap.PortScanner()
nm.scan('192.168.1.0/24', arguments='-sP')

# Create network diagram
G = nx.Graph()

for host in nm.all_hosts():
    G.add_node(host)
    for proto in nm[host].all_protocols():
        lport = nm[host][proto].keys()
        for port in lport:
            if nm[host][proto][port]['state'] == 'open':
                G.add_edge(host, f"{proto}/{port}")

# Draw network diagram
pos = nx.spring_layout(G, seed=42)  # or other layout
node_color = '#FFC947'
edge_color = '#6D4C41'
node_size = 800
font_size = 10
edge_width = 2
font_color = 'white'
plt.figure(figsize=(10, 8))
nx.draw(G, pos, with_labels=True, node_color=node_color, edge_color=edge_color, node_size=node_size,
        font_size=font_size, font_color=font_color, width=edge_width)
nx.draw_networkx_edge_labels(G, pos, font_size=font_size-2, font_color=font_color,
                             edge_labels={(u,v): f"{u}:{v}" for u,v in G.edges()})
plt.axis('off')
plt.show()
