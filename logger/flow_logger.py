from datetime import datetime
from .database import get_connection, initialize_all
import sqlite3

class FlowLogger:
    def __init__(self, conn):
        self.conn=conn
        initialize_all(self.conn)
                          
    def read_logs(self):
        """Retrieve all flow logs from the database."""
        try:
            query = "SELECT * FROM flow_logs ORDER BY timestamp ASC"
            cursor=self.conn.execute(query) 
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error reading logs: {e}")
            return []

    def log_flow(self, flow_id=None, flow_name=None, status=None, details=None):
        """
        Log a flow-related event to the database.
        
        Args:
            flow_id (int, optional): ID of the related flow
            flow_name (str): Name of the flow
            status (str): Current status of the flow
            details (str): Additional details about the event
        """
        try:
            query = '''INSERT INTO flow_logs 
                    (flow_id, flow_name, status, timestamp, details)
                    VALUES (?, ?, ?, ?, ?)'''
            timestamp = datetime.now().isoformat()
            self.conn.execute(query, (flow_id, flow_name, status, timestamp, details))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error logging flow: {e}")
            return False
