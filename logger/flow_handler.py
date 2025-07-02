import sqlite3
from datetime import datetime
from .database import get_connection
from .flow_logger import FlowLogger

class FlowHandler:
    def __init__(self, conn):
        self.conn = conn
        self.logger = FlowLogger(conn) # Initialize the FlowLogger with the database connection

    def create_flow(self, title, description, solution_id, priority, creator_id):
        query='''INSERT INTO flows
                (title, description, solution_id, status, priority, creator_id, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?)'''
        try:
            now=datetime.now().isoformat()
            cursor=self.conn.execute(query, (title, description, solution_id, 'New', priority, creator_id, now, now))
            self.conn.commit()

            # Get creator name from developers table
            name_query = "SELECT name FROM developers WHERE id = ?"
            cursor_name = self.conn.execute(name_query, (creator_id,))
            name_result = cursor_name.fetchone()
            creator_name = name_result[0] if name_result else f"User {creator_id}"
            
            # Add logging
            self.logger.log_flow(
                flow_id=cursor.lastrowid,
                flow_name=title,
                status='New',
                details=f'Flow created by {creator_name}'
            )
            return True
        except sqlite3.Error as e:
            print(f"Error creating flow: {e}")
            return False

    def update_flow_status(self, flow_id, status):
        try:
            # Get the flow name before updating status
            cursor = self.conn.execute("SELECT title FROM flows WHERE id = ?", (flow_id,))
            row = cursor.fetchone()
            flow_name = row[0] if row else "Unknown Flow"

            # Update the flow status
            query='''UPDATE flows
                    SET status = ?, updated_at = ? WHERE ID = ?'''
            self.conn.execute(query, (status, datetime.now().isoformat(), flow_id))
            self.conn.commit()

            # Add logging
            self.logger.log_flow(
                flow_id=flow_id,
                flow_name=flow_name,
                status=status,
                details=f'Flow status updated to {status}'
            )
            return True
        except sqlite3.Error as e:
            print(f"Error updating flow status: {e}")
            return False

    def assigned(self, flow_id, assigned, status):
        try:
            # Get the flow name before assigning flow
            cursor = self.conn.execute("SELECT title FROM flows WHERE id = ?", (flow_id,))
            row = cursor.fetchone()
            flow_name = row[0] if row else "Unknown Flow"

            # Update the flow assignee and status
            query='''UPDATE flows
                    SET status = ?, assigned_id = ?, updated_at = ?
                    WHERE id=?'''
            self.conn.execute(query, (status, assigned, datetime.now().isoformat(), flow_id))
            self.conn.commit()

            # Get the developer name from developers table
            name_query = "SELECT name FROM developers WHERE id = ?"
            cursor_name = self.conn.execute(name_query, (assigned,))
            name_result = cursor_name.fetchone()
            assigned_name = name_result[0] if name_result else f"User {assigned}"

            # Add logging
            self.logger.log_flow(
                flow_id=flow_id,
                flow_name=flow_name,  
                status=status,
                details=f'Flow assigned to {assigned_name}'
            )
            return True
        except sqlite3.Error as e:
            print(f"Error assigning developer ID to flow: {e}")
            return False

    def get_flows(self, solution_id=None):
        try:
            if solution_id:
                solution_id=int(solution_id)
                # Check if solution exists
                check_query="SELECT id FROM solutions WHERE id=?"
                cursor=self.conn.execute(check_query, (solution_id,))
                if not cursor.fetchone():
                    return None
                
                # Fetch flows for the given solution_id
                query = '''
                SELECT id, title, description, solution_id, status, priority, assigned_id, creator_id, created_at, updated_at
                FROM flows
                WHERE solution_id = ?
                '''
                cursor = self.conn.execute(query, (solution_id,))
            else:
                # Fetch all flows
                query = '''
                SELECT id, title, description, solution_id, status, priority, assigned_id, creator_id, created_at, updated_at
                FROM flows
                '''
                cursor =self.conn.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving flows: {e}")
            return None
    
    def delete_flow(self, flow_id):
        try:
            """Delete a flow but keep its associated logs."""
            # Get the flow name before deleting
            cursor = self.conn.execute("SELECT title FROM flows WHERE id = ?", (flow_id,))
            row = cursor.fetchone()
            flow_name = row[0] if row else "Unknown Flow"

            # Log the deletion before removing the flow
            self.logger.log_flow(
                flow_id=flow_id,
                flow_name=flow_name,  
                status='Deleted',
                details=f'Flow with ID {flow_id} deleted'
            )
            # Delete flow 
            self.conn.execute("DELETE FROM flows WHERE id = ?", (flow_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting flow: {e}")
            return False
    
    