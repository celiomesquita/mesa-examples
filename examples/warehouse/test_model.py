#!/usr/bin/env python3
"""
Test script to verify the warehouse model works correctly.
"""

from warehouse.model import WarehouseModel
from warehouse.agents import RobotAgent, InventoryAgent

def test_model():
    print("Testing Warehouse Model...")

    # Create model
    model = WarehouseModel()
    print(f"✓ Model created with {len(model.agents)} agents")

    # Check agent types
    print("\nAgent breakdown:")
    for agent_type, agents in model.agents_by_type.items():
        print(f"  {agent_type.__name__}: {len(agents)}")

    # Run a few steps
    print("\nRunning simulation steps...")
    for i in range(5):
        try:
            model.step()
            print(f"✓ Step {i+1} completed")
        except Exception as e:
            print(f"✗ Step {i+1} failed: {e}")
            import traceback
            traceback.print_exc()
            break

    # Check robot states
    print("\nRobot states:")
    for robot in model.agents_by_type[RobotAgent]:
        print(f"  Robot at {robot.cell.coordinate}: status={robot.status}, carrying={robot.carrying}")

    print("\n✓ Model test completed successfully!")

if __name__ == "__main__":
    test_model()