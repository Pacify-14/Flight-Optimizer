from heapq import heappush, heappop
from collections import deque

from flight import Flight

class Planner:
    def __init__(self, flights):
        # Initialize an empty dictionary for the graph
        self.graph = {}
        
        # Populate the graph with the given flights
        for flight in flights:
            if flight.start_city not in self.graph:
                self.graph[flight.start_city] = []
            self.graph[flight.start_city].append(flight)

        print(self.graph)
    
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        queue = deque([(start_city, [], 0)])  # (current_city, path_so_far, arrival_time)
        best_arrival = float('inf')
        best_path = None
        
        # Perform BFS
        while queue:
            current_city, path, arrival_time = queue.popleft()
            
            # If we reach the end city within time limits and fewer flights
            if current_city == end_city and t1 <= arrival_time <= t2:
                if best_path is None or len(path) < len(best_path) or (len(path) == len(best_path) and arrival_time < best_arrival):
                    best_path = path
                    best_arrival = arrival_time
            
            # Explore next flights from the current city if it has outgoing flights
            if current_city in self.graph:
                for flight in self.graph[current_city]:
                    if flight.departure_time >= t1 and arrival_time <= flight.departure_time:
                        # Ensure at least 20 minutes gap for connecting flights
                        if not path or flight.departure_time >= path[-1].arrival_time + 20:
                            queue.append((flight.end_city, path + [flight], flight.arrival_time))
        
        return best_path

    def cheapest_route(self, start_city, end_city, t1, t2):
        min_heap = [(0, start_city, [], 0)]  # (total_fare, city, path, arrival_time)
        best_cost = float('inf')
        best_path = None
        
        # Dijkstra’s algorithm with priority queue
        while min_heap:
            total_fare, current_city, path, arrival_time = heappop(min_heap)
            
            # If we reach the destination city within time limits with a cheaper cost
            if current_city == end_city and t1 <= arrival_time <= t2:
                if total_fare < best_cost:
                    best_cost = total_fare
                    best_path = path
            
            # Explore next flights from current city if it has outgoing flights
            if current_city in self.graph:
                for flight in self.graph[current_city]:
                    if flight.departure_time >= t1 and arrival_time <= flight.departure_time:
                        # Ensure at least 20 minutes gap for connecting flights
                        if not path or flight.departure_time >= path[-1].arrival_time + 20:
                            heappush(min_heap, (total_fare + flight.fare, flight.end_city, path + [flight], flight.arrival_time))
        
        return best_path

    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        min_heap = [(0, 0, start_city, [], 0)]  # (flight_count, total_fare, city, path, arrival_time)
        best_path = None
        best_flights = float('inf')
        best_cost = float('inf')
        
        # BFS with priority queue
        while min_heap:
            flight_count, total_fare, current_city, path, arrival_time = heappop(min_heap)
            
            # If we reach the destination city within time limits
            if current_city == end_city and t1 <= arrival_time <= t2:
                # Check for fewer flights or cheaper cost among paths with the same flights
                if best_path is None or flight_count < best_flights or (flight_count == best_flights and total_fare < best_cost):
                    best_path = path
                    best_flights = flight_count
                    best_cost = total_fare
            
            # Explore next flights from current city if it has outgoing flights
            if current_city in self.graph:
                for flight in self.graph[current_city]:
                    if flight.departure_time >= t1 and arrival_time <= flight.departure_time:
                        # Ensure at least 20 minutes gap for connecting flights
                        if not path or flight.departure_time >= path[-1].arrival_time + 20:
                            heappush(min_heap, (flight_count + 1, total_fare + flight.fare, flight.end_city, path + [flight], flight.arrival_time))
        
        return best_path
