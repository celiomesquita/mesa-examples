# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Running the Model

**Option 1: Standard Solara CLI**
```bash
solara run app.py
```

**Option 2: Alternative server (for WSL/networking issues)**
```bash
python run_server.py
```

**Option 3: Test model without visualization**
```bash
python test_model.py
```

**Troubleshooting WSL Connection Issues:**
If you get "connection refused" errors in WSL:
1. Try accessing via the WSL IP: `ip addr show eth0`
2. Use Windows localhost: Replace `localhost` with `127.0.0.1`
3. Check Windows Firewall settings
4. Use the alternative server script: `run_server.py`

### Testing
```bash
# From the mesa-examples root directory
pytest test_examples.py::test_model_steps[WarehouseModel]
```
Tests the warehouse model specifically. The project uses pytest with parametrized tests that automatically discover Mesa models.

### Linting
```bash
# From the mesa-examples root directory
ruff check examples/warehouse/
ruff format examples/warehouse/
```
Uses ruff for both linting and formatting. Configuration is in `pyproject.toml`.

## Architecture

### Meta-Agent System
This warehouse example demonstrates Mesa's meta-agent capabilities, where complex agents are composed of simpler sub-agents:

- **RobotAgent**: A meta-agent created from three constituting agents
  - **RouteAgent**: Handles pathfinding using A* algorithm
  - **SensorAgent**: Manages movement and obstacle detection
  - **WorkerAgent**: Handles task execution (pickup/delivery)

### Key Components

**Model Structure (`warehouse/model.py`)**:
- `WarehouseModel`: Main simulation controller
- Uses `OrthogonalMooreGrid` for 3D warehouse space
- Creates inventory items and robot meta-agents during initialization
- Central coordination through `central_move()` method

**Agent Hierarchy (`warehouse/agents.py`)**:
- `InventoryAgent`: Fixed inventory items with quantities
- Three constituting agents that form robot meta-agents:
  - Navigation, sensing, and work capabilities are separated
  - Meta-agent creation uses `create_meta_agent()` with attribute/method assumption

**Warehouse Generation (`warehouse/make_warehouse.py`)**:
- Procedural generation of 3D warehouse layout
- Predefined loading dock and charging station locations
- Random item code generation for inventory

### Meta-Agent Usage Patterns
- Access constituting agents: `robot.get_constituting_agent_instance(RouteAgent)`
- Reference meta-agent type: `type(model.RobotAgent)` (required pattern)
- Attribute sharing enabled through `assume_constituting_agent_attributes=True`
- Method sharing enabled through `assume_constituting_agent_methods=True`

### Visualization (`app.py`)
- Uses Solara for web-based 3D visualization
- Matplotlib 3D scatter plots showing robots, inventory, and loading docks
- Real-time updates during simulation steps