import tkinter as tk
from tkinter import ttk
import math

# Define the Airport class
class Airport:
    def __init__(self, code, city, state, lon, lat):
        self.code = code
        self.city = city
        self.state = state
        self.lon = lon
        self.lat = lat

# Define the Haversine formula
def haversine(lon1, lat1, lon2, lat2):
    R = 6371.0
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat, dlon = lat2_rad - lat1_rad, lon2_rad - lon1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Define the AirportGraph class
class AirportGraph:
    def __init__(self):
        self.airports = {}
        self.edges = {}

    def add_airport(self, code, city, state, lon, lat):
        self.airports[code] = Airport(code, city, state, lon, lat)
        self.edges[code] = []

    def add_edge(self, code1, code2):
        dist = haversine(
            self.airports[code1].lon, self.airports[code1].lat,
            self.airports[code2].lon, self.airports[code2].lat
        )
        self.edges[code1].append((code2, dist))
        self.edges[code2].append((code1, dist))

    def bfs(self, start, goal):
        #start is the from_airport, goal is the to_airport
        #visited is used to store the Visited nodes;queue is used to store the Current node and its path to it
        visited, queue = set(), [(start, [start])]

        # When the queue is not empty, continue looping
        while queue:

            # Pop the first element of the queue and get the current node and its path to it
            current, path = queue.pop(0)

            # If the current node is the target node, return the path
            if current == goal:
                return path

            # Traverse all neighbors of the current node
            for neighbor, _ in self.edges[current]:
                # If the neighbor node is not visited
                # Add the neighbor node and its path to the queue
                # The path is the current path plus the neighbor node
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []

    def dfs(self, start, goal, path=None, visited=None):
        # Initialize the path and visited set if not provided
        if path is None:
            path, visited = [start], set()
        # Base case: if the start node is the goal, return the current path
        if start == goal:
            return path

        # Mark the current node as visited
        visited.add(start)
        # Iterate through all neighbors of the current node
        for neighbor, _ in self.edges[start]:
            # If the neighbor has not been visited
            #Add neighbor nodes based on the current path
            if neighbor not in visited:
                new_path = self.dfs(neighbor, goal, path + [neighbor], visited)
                if new_path:
                    return new_path
        return []

    def dijkstra(self, start, goal):
        # Import the heapq module for the priority queue (min-heap)
        import heapq
        # Initialize the priority queue with the start node and its initial cost (0)
        # queue stores tuples in the format (cost, current_node, path)
        # visited is a set to keep track of the nodes we've already visited
        queue, visited = [(0, start, [])], set()
        # Loop while there are still nodes to explore in the queue
        while queue:
            cost, current, path = heapq.heappop(queue)
            # Skip the node if it has already been visited
            if current in visited:
                continue
            # Add the current node to the path, Mark the current node as visited
            path = path + [current]
            visited.add(current)
            # If the current node is the goal, return the path and the total cost
            if current == goal:
                return path, cost
            # Explore the neighbors of the current node
            for neighbor, dist in self.edges[current]:
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + dist, neighbor, path))
        return [], float('inf')


# Create the graph
def create_graph():
    graph = AirportGraph()
    # add airports
    airports = [
        ("ATL", "Atlanta", "GA", -84.3880, 33.7490),
        ("AUS", "Austin", "TX", -97.7431, 30.2672),
        ("BOS", "Boston", "MA", -71.0096, 42.3656),
        ("BWI", "Baltimore", "MD", -76.6413, 39.2904),
        ("DCA", "Washington D.C.", "VA", -77.0369, 38.9072),
        ("DEN", "Denver", "CO", -104.9903, 39.7392),
        ("DFW", "Dallas", "TX", -96.7967, 32.7767),
        ("DTW", "Detroit", "MI", -83.0458, 42.3314),
        ("EWR", "Newark", "NJ", -74.1745, 40.7357),
        ("IAD", "Washington D.C.", "VA", -77.4558, 38.8821),
        ("IAH", "Houston", "TX", -95.3698, 29.7604),
        ("JFK", "New York City", "NY", -73.7781, 40.6413),
        ("LAS", "Las Vegas", "NV", -115.1398, 36.1699),
        ("LAX", "Los Angeles", "CA", -118.2437, 34.0522),
        ("MDW", "Chicago", "IL", -87.6298, 41.8781),
        ("MIA", "Miami", "FL", -80.1918, 25.7617),
        ("MSP", "Minneapolis", "MN", -93.2650, 44.9778),
        ("PDX", "Portland", "OR", -122.6762, 45.5051),
        ("PHL", "Philadelphia", "PA", -75.1652, 39.9526),
        ("RDU", "Raleigh", "NC", -78.7870, 35.7796),
        ("SAN", "San Diego", "CA", -117.1611, 32.7157),
        ("SEA", "Seattle", "WA", -122.3321, 47.6062),
        ("SFO", "San Francisco", "CA", -122.4194, 37.7749),
        ("SLC", "Salt Lake City", "UT", -111.8910, 40.7608)
    ]
    # add neighbours
    for code, city, state, lon, lat in airports:
        graph.add_airport(code, city, state, lon, lat)
    neighbours = {
        "ATL": ["AUS", "BOS", "BWI", "DCA", "DEN", "DFW", "DTW", "EWR", "IAD", "IAH", "JFK", "LAS", "LAX", "MDW", "MIA",
                "MSP", "PDX", "PHL", "RDU"],
        "AUS": ["ATL", "BOS", "DTW", "JFK", "RDU", "LAS", "LAX", "MSP", "SEA", "SLC"],
        "BOS": ["SLC", "RDU", "AUS", "ATL", "DTW", "MSP", "SEA", "LAX", "DEN", "JFK", "IAD", "MIA", "PHL", "IAH",
                "LAS"],
        "BWI": ["ATL", "DTW", "MSP", "JFK", "SLC", "BOS"],
        "DCA": ["ATL", "JFK", "BOS", "DTW", "MSP", "SLC"],
        "DEN": ["ATL", "MSP", "SLC", "DTW"],
        "DFW": ["ATL", "MSP", "DTW", "SLC"],
        "DTW": ["ATL", "MSP", "DTW", "SLC", "LAX"],
        "EWR": ["BOS", "JFK", "ATL", "RDU", "MIA", "LAX", "SFO", "SEA"],
        "IAD": ["ATL", "BOS", "DTW", "MSP", "RDU", "SLC"],
        "IAH": ["ATL", "DTW", "SLC"],
        "JFK": ["ATL", "DTW", "MSP", "SLC"],
        "LAS": ["LAX", "ATL", "MIA", "DFW", "BOS", "SFO", "DTW", "SEA", "MSP"],
        "LAX": ["ATL", "MSP", "DTW", "SLC", "LAX", "SEA", "SFO", "DFW"],
        "MDW": ["JFK", "SFO", "SLC", "ATL", "LAS", "MSP", "BOS", "DTW", "SEA", "PDX"],
        "MIA": ["ATL", "DTW", "MSP"],
        "MSP": ["ATL", "JFK", "LAX", "BOS", "DFW", "DCA"],
        "PDX": ["ATL", "DEN", "DFW", "SEA", "LAS", "LAX"],
        "PHL": ["SEA", "LAX", "SFO", "SLC", "MSP", "ATL", "DTW"],
        "RDU": ["ATL", "BOS", "JFK", "DTW", "MSP", "SLC"],
        "SAN": ["ATL", "BOS", "DTW", "MSP", "LAX", "SLC"],
        "SEA": ["MSP", "SEA", "SLC", "ATL", "DTW", "JFK"],
        "SFO": ["LAX", "SLC", "ATL", "MSP", "SFO", "DFW", "DEN", "LAS"],
        "SLC": ["LAX", "JFK", "SAN", "SEA", "DEN", "SLC", "DFW", "PDX"]
    }
    for code, neighbors in neighbours.items():
        for neighbor in neighbors:
            graph.add_edge(code, neighbor)
    return graph

# Initialize the graph
graph = create_graph()

# GUI Class
class AirportGraphAlgoMenu(tk.Frame):
    def __init__(self, master=None, graph=None):
        super().__init__(master)
        self.master = master
        self.graph = graph  # Store the graph instance
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.from_label = tk.Label(self, text="From:")
        self.from_label.grid(row=0, column=0)
        self.from_view = ttk.Combobox(self, values=list(self.graph.airports.keys()))
        self.from_view.grid(row=0, column=1)

        self.to_label = tk.Label(self, text="To:")
        self.to_label.grid(row=1, column=0)
        self.to_view = ttk.Combobox(self, values=list(self.graph.airports.keys()))
        self.to_view.grid(row=1, column=1)

        self.algo_label = tk.Label(self, text="Algorithm:")
        self.algo_label.grid(row=2, column=0)
        self.algo_choice_view = ttk.Combobox(self, values=["BFS", "DFS", "Dijkstra"])
        self.algo_choice_view.grid(row=2, column=1)

        self.run_button = tk.Button(self, text="Run", command=self.run_algorithm)
        self.run_button.grid(row=3, column=0, columnspan=2)

    def run_algorithm(self):
        from_airport = self.from_view.get()
        to_airport = self.to_view.get()
        algorithm = self.algo_choice_view.get()

        if algorithm == "BFS":
            print(f"BFS selected: from {from_airport} to {to_airport}")
            path = self.graph.bfs(from_airport, to_airport)
        elif algorithm == "DFS":
            print(f"DFS selected: from {from_airport} to {to_airport}")
            path = self.graph.dfs(from_airport, to_airport)
        elif algorithm == "Dijkstra":
            print(f"DFS selected: from {from_airport} to {to_airport}")
            path, cost = self.graph.dijkstra(from_airport, to_airport)

            print(f"Path: {path}, Cost: {cost:.2f}")
            return
        print(f"Path: {path}")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Airport Graph Algorithms")
    app = AirportGraphAlgoMenu(master=root, graph=graph)
    app.mainloop()
