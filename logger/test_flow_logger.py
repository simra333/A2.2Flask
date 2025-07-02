import unittest
import sqlite3
from .database import get_connection, initialize_all
from .flow_handler import FlowHandler
from .solution_handler import SolutionHandler

# Test Database Connection
class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = get_connection(':memory:')  # Use an in-memory database for testing
    
    def test_connection(self):
        self.assertIsInstance(self.conn, sqlite3.Connection)

    def test_initialize_all(self):
        initialize_all(self.conn)
        cursor = self.conn.cursor()
        # test for all required tables
        tables = ['solutions', 'developers', 'flows', 'flow_logs']
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            self.assertIsNotNone(cursor.fetchone(), f"{table} table should be created")

# Test Solution Operations
class TestSolutionOperations(unittest.TestCase):
    def setUp(self):
        self.conn = get_connection(':memory:')
        initialize_all(self.conn)
        self.solution_handler = SolutionHandler(self.conn)

    def test_create_solution(self):
        result = self.solution_handler.create_solution(
            name="Test Solution",
            description="This is a test solution"
        )
        self.assertTrue(result)  

# Test Flow Operations
class TestFlowOperations(unittest.TestCase):
    def setUp(self):
        self.conn = get_connection(':memory:')
        initialize_all(self.conn)
        self.flow_handler = FlowHandler(self.conn)
    
    def test_create_flow(self):
        result = self.flow_handler.create_flow(
            title="Test Flow",
            description="This is a test flow",
            solution_id=1,
            priority="High",
            creator_id="1"
        )
        self.assertTrue(result)

    def test_update_flow_status(self):
        self.flow_handler.create_flow("Test Flow", "This is a test flow", 1, "High", "1")
        result = self.flow_handler.update_flow_status(1, "In Progress")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
