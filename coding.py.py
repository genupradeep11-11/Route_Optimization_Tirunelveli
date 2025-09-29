import pandas as pd
from geopy.distance import geodesic
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import webbrowser


df = pd.read_excel("customers.xlsx")  


customer_names = df['Customer Name'].tolist()


locations = list(zip(df['Latitude'], df['Longitude']))
num_customers = len(locations)

distance_matrix = []
for i in range(num_customers):
    row = []
    for j in range(num_customers):
        dist = geodesic(locations[i], locations[j]).kilometers
        row.append(dist)
    distance_matrix.append(row)


manager = pywrapcp.RoutingIndexManager(num_customers, 1, 0)
routing = pywrapcp.RoutingModel(manager)

def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return int(distance_matrix[from_node][to_node] * 1000)  

transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

solution = routing.SolveWithParameters(search_parameters)


route = []
if solution:
    index = routing.Start(0)
    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        route.append(customer_names[node_index])   
        index = solution.Value(routing.NextVar(index))
    node_index = manager.IndexToNode(index)
    route.append(customer_names[node_index])   

 
print("Route found:")
print(" -> ".join(route))

 
def generate_google_maps_route(locations):
    base_url = "https://www.google.com/maps/dir/?api=1"
    waypoints = "|".join([f"{lat},{lon}" for lat, lon in locations])
    url = f"{base_url}&waypoints={waypoints}&travelmode=driving"
    return url

 
optimized_locations = [(df.loc[df['Customer Name'] == name, 'Latitude'].values[0],
                        df.loc[df['Customer Name'] == name, 'Longitude'].values[0])
                       for name in route]

url = generate_google_maps_route(optimized_locations)
webbrowser.open(url)
