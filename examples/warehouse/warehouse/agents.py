from queue import PriorityQueue

import mesa
from mesa.experimental.cell_space import FixedAgent, CellAgent


class InventoryAgent(FixedAgent):
    """Represents an inventory item in the warehouse."""

    def __init__(self, model, cell, item: str):
        super().__init__(model)
        self.cell = cell
        self.item = item
        self.quantity = 1000  # Default quantity


class RobotAgent(CellAgent):
    """Represents a robot that can navigate the warehouse and perform tasks.

    Combines routing, sensing, and working capabilities in a single agent.
    """

    def __init__(self, model, cell, loading_dock, charging_station):
        super().__init__(model)
        self.cell = cell
        self.loading_dock = loading_dock
        self.charging_station = charging_station
        self.path = None
        self.carrying = None
        self.item = None
        self.status = "open"

    def find_path(self, start, goal) -> list[tuple[int, int, int]] | None:
        """Determines the path for a robot to take using the A* algorithm."""

        def heuristic(a, b) -> int:
            dx = abs(a[0] - b[0])
            dy = abs(a[1] - b[1])
            return dx + dy

        open_set = PriorityQueue()
        open_set.put((0, start.coordinate))
        came_from = {}
        g_score = {start.coordinate: 0}

        while not open_set.empty():
            _, current = open_set.get()

            if current[:2] == goal.coordinate[:2]:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                path.insert(0, start.coordinate)
                path.pop()  # Remove the last location (inventory)
                return path

            for n_cell in self.model.warehouse[current].neighborhood:
                coord = n_cell.coordinate

                # Only consider orthogonal neighbors
                if abs(coord[0] - current[0]) + abs(coord[1] - current[1]) != 1:
                    continue

                tentative_g_score = g_score[current] + 1
                if not n_cell.is_empty:
                    tentative_g_score += 50  # Penalty for non-empty cells

                if coord not in g_score or tentative_g_score < g_score[coord]:
                    g_score[coord] = tentative_g_score
                    f_score = tentative_g_score + heuristic(coord, goal.coordinate)
                    open_set.put((f_score, coord))
                    came_from[coord] = current

        return None

    def move(
        self, coord: tuple[int, int, int], path: list[tuple[int, int, int]]
    ) -> str:
        """Moves the agent along the given path."""
        if coord not in path:
            raise ValueError("Current coordinate not in path.")

        idx = path.index(coord)
        if idx + 1 >= len(path):
            return "movement complete"

        next_cell = self.model.warehouse[path[idx + 1]]
        if next_cell.is_empty:
            self.cell = next_cell
            return "moving"

        # Handle obstacle
        neighbors = self.model.warehouse[self.cell.coordinate].neighborhood
        empty_neighbors = [n for n in neighbors if n.is_empty]
        if empty_neighbors:
            self.cell = self.random.choice(empty_neighbors)

        # Recalculate path
        new_path = self.find_path(self.cell, self.item.cell)
        self.path = new_path
        return "recalculating"

    def initiate_task(self, item: InventoryAgent):
        """Initiates a task for the robot to perform."""
        self.item = item
        self.path = self.find_path(self.cell, item.cell)

    def continue_task(self):
        """Continues the task if the robot is able to perform it."""
        status = self.move(self.cell.coordinate, self.path)

        if status == "movement complete" and self.status == "inventory":
            # Pick up item and bring to loading dock
            x, y = self.cell.coordinate[:2]
            z = self.item.cell.coordinate[2]
            self.cell = self.model.warehouse[x, y, z]
            self.status = "loading"
            self.carrying = self.item.item
            self.item.quantity -= 1
            self.cell = self.model.warehouse[x, y, 0]
            self.path = self.find_path(self.cell, self.loading_dock)

        if status == "movement complete" and self.status == "loading":
            # Load item onto truck and return to charging station
            self.carrying = None
            self.status = "open"


# Keep old class names for backwards compatibility
RouteAgent = RobotAgent
SensorAgent = RobotAgent
WorkerAgent = RobotAgent