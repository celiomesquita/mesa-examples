#!/usr/bin/env python3
"""
Simple visualization alternative using Mesa's built-in tools.
This runs without requiring Solara server.
"""

import matplotlib.pyplot as plt
import numpy as np
from warehouse.model import WarehouseModel
from warehouse.agents import RobotAgent, InventoryAgent

def visualize_warehouse(model, step=0):
    """Create a simple 2D visualization of the warehouse."""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Get warehouse dimensions
    max_x = max(agent.cell.coordinate[0] for agent in model.agents)
    max_y = max(agent.cell.coordinate[1] for agent in model.agents)

    # Create empty grid for visualization
    grid = np.zeros((max_x + 1, max_y + 1))

    # Plot inventory items (blue squares)
    inventory_x = []
    inventory_y = []
    for agent in model.agents_by_type[InventoryAgent]:
        x, y, z = agent.cell.coordinate
        inventory_x.append(x)
        inventory_y.append(y)
        grid[x, y] = 1

    # Plot robots (red circles)
    robot_x = []
    robot_y = []
    robot_status = []
    for agent in model.agents_by_type[RobotAgent]:
        x, y, z = agent.cell.coordinate
        robot_x.append(x)
        robot_y.append(y)
        robot_status.append(agent.status)
        grid[x, y] = 2

    # Plot loading docks (yellow diamonds)
    loading_docks = [(0, 0), (0, 2), (0, 4), (0, 6), (0, 8)]
    dock_x = [coord[0] for coord in loading_docks]
    dock_y = [coord[1] for coord in loading_docks]

    # Plot charging stations (green triangles)
    charging_stations = [(21, 19), (21, 17), (21, 15), (21, 13), (21, 11)]
    charge_x = [coord[0] for coord in charging_stations]
    charge_y = [coord[1] for coord in charging_stations]

    # Create the plot
    ax.scatter(inventory_x, inventory_y, c='blue', marker='s', s=30, label='Inventory', alpha=0.6)
    ax.scatter(robot_x, robot_y, c='red', marker='o', s=100, label='Robots')
    ax.scatter(dock_x, dock_y, c='yellow', marker='D', s=150, label='Loading Docks', edgecolors='black')
    ax.scatter(charge_x, charge_y, c='green', marker='^', s=150, label='Charging Stations', edgecolors='black')

    # Add robot status annotations
    for i, (x, y, status) in enumerate(zip(robot_x, robot_y, robot_status)):
        ax.annotate(f'R{i+1}\n{status}', (x, y), xytext=(5, 5),
                   textcoords='offset points', fontsize=8,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

    ax.set_xlim(-1, max_x + 1)
    ax.set_ylim(-1, max_y + 1)
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_title(f'Warehouse Simulation - Step {step}')
    ax.legend()
    ax.grid(True, alpha=0.3)

    return fig

def run_simulation_with_viz(steps=10):
    """Run the simulation and show visualization every few steps."""
    model = WarehouseModel()

    print(f"Starting simulation with {len(model.agents)} agents")
    print(f"- Robots: {len(model.agents_by_type[RobotAgent])}")
    print(f"- Inventory items: {len(model.agents_by_type[InventoryAgent])}")

    # Show initial state
    fig = visualize_warehouse(model, 0)
    plt.show()

    # Run simulation
    for step in range(1, steps + 1):
        model.step()
        print(f"Step {step} completed")

        # Show visualization every 5 steps
        if step % 5 == 0:
            fig = visualize_warehouse(model, step)
            plt.show()

    # Show final state
    print("\nFinal robot states:")
    for i, robot in enumerate(model.agents_by_type[RobotAgent]):
        print(f"  Robot {i+1}: {robot.status}, carrying: {robot.carrying}")

if __name__ == "__main__":
    print("Warehouse Simulation - Simple Visualization")
    print("=" * 50)

    try:
        run_simulation_with_viz(10)
    except KeyboardInterrupt:
        print("\nSimulation stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()