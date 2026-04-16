import math
import random
import statistics
import streamlit as st
import pandas as pd

# Scenarios
scenarios = {
    "Scenario 1": {
        "Depot": (0, 0),
        "A": (1, 2),
        "B": (3, 5),
        "C": (6, 1),
        "D": (8, 4),
        "E": (5, 7)
    },
    "Scenario 2": {
        "Depot": (0, 0),
        "A": (2, 2),
        "B": (3, 2),
        "C": (2, 3),
        "D": (3, 3),
        "E": (4, 2)
    },
    "Scenario 3": {
        "Depot": (0, 0),
        "A": (1, 2),
        "B": (2, 1),
        "C": (2, 3),
        "D": (10, 10),
        "E": (11, 9),
        "F": (9, 11)
    }
}

def distance(p1, p2):
    return math.dist(p1, p2)

def nearest_neighbor_route(start_point, locations):
    unvisited = locations.copy()
    current_point = start_point
    route = [current_point]
    total_distance = 0

    while unvisited:
        next_point = min(unvisited, key=lambda p: distance(current_point, p))
        dist = distance(current_point, next_point)
        total_distance += dist
        route.append(next_point)
        unvisited.remove(next_point)
        current_point = next_point

    # Return to Depot
    dist_to_depot = distance(current_point, start_point)
    total_distance += dist_to_depot
    route.append(start_point)

    return route, total_distance

def random_route(start_point, locations):
    unvisited = locations.copy()
    random.shuffle(unvisited)
    current_point = start_point
    route = [current_point]
    total_distance = 0

    for next_point in unvisited:
        dist = distance(current_point, next_point)
        total_distance += dist
        route.append(next_point)
        current_point = next_point

    # Return to Depot
    dist_to_depot = distance(current_point, start_point)
    total_distance += dist_to_depot
    route.append(start_point)

    return route, total_distance

st.title("Amazon Delivery Route Efficiency Simulator")
st.write("""
This app assesses the efficiency of two different routes for an Amazon Delivery driver across three scenarios:
- **Scenario 1**: Uniformly spaced out points.
- **Scenario 2**: Clustered points.
- **Scenario 3**: Two clusters separated over a distance.

It compares the **Nearest Neighbor** (Greedy) method against a **Random Route** method. 
It assumes an average speed where 1 mile = 5 minutes.
""")

for name, points in scenarios.items():
    st.header(name)
    depot = points["Depot"]
    locations_to_visit = [v for k, v in points.items() if k != "Depot"]

    # Statistics Calculation
    # Nearest Neighbor (Deterministic)
    nn_route, nn_dist = nearest_neighbor_route(depot, locations_to_visit)
    nn_time = nn_dist * 5

    # Random Route (10 Trials)
    random_trials = [random_route(depot, locations_to_visit) for _ in range(10)]
    random_distances = [r[1] for r in random_trials]
    random_times = [d * 5 for d in random_distances]

    # Stats for Random
    stats_data = {
        "Metric": [
            "Average Distance (miles)", "Minimum Distance (miles)", "Maximum Distance (miles)", "Std Dev Distance (miles)",
            "Average Time (mins)", "Minimum Time (mins)", "Maximum Time (mins)", "Std Dev Time (mins)"
        ],
        "Nearest Neighbor": [
            f"{nn_dist:.2f}", f"{nn_dist:.2f}", f"{nn_dist:.2f}", "0.00",
            f"{nn_time:.2f}", f"{nn_time:.2f}", f"{nn_time:.2f}", "0.00"
        ],
        "Random (10 Trials)": [
            f"{statistics.mean(random_distances):.2f}",
            f"{min(random_distances):.2f}",
            f"{max(random_distances):.2f}",
            f"{statistics.stdev(random_distances):.2f}",
            f"{statistics.mean(random_times):.2f}",
            f"{min(random_times):.2f}",
            f"{max(random_times):.2f}",
            f"{statistics.stdev(random_times):.2f}"
        ]
    }

    df_stats = pd.DataFrame(stats_data)
    st.table(df_stats)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Nearest Neighbor Route")
        st.metric("Distance", f"{nn_dist:.2f} miles")
        st.metric("Time", f"{nn_time:.2f} mins")
        with st.expander("Show Route Details"):
            st.write(nn_route)

    with col2:
        st.subheader("Example Random Route")
        # Show the first random trial as an example
        r_route, r_dist = random_trials[0]
        r_time = r_dist * 5
        st.metric("Distance", f"{r_dist:.2f} miles")
        st.metric("Time", f"{r_time:.2f} mins")
        with st.expander("Show Example Route Details"):
            st.write(r_route)

if st.button("Re-run Simulation"):
    st.rerun()







