from datetime import datetime
from .database import get_connection
import sqlite3

class SolutionHandler:
    def __init__(self, conn):
        self.conn=conn

    def create_solution(self, name, description):
        try:
            query='''INSERT INTO solutions (name, description, created_at)
                    VALUES (?, ?, ?)'''
            self.conn.execute(query, (name, description, datetime.now().isoformat()))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error creating solution: {e}")
            return False

    def get_solution(self):
        try:
            query="SELECT * FROM solutions"
            cursor=self.conn.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving solutions: {e}")
            return None
        
    def update_solution(self, solution_id, name, description):
        try:
            query='''Update solutions
                    SET name = ?, description = ? WHERE ID =?'''
            self.conn.execute(query, (name, description, solution_id))
            self.conn.commit()    
            return True
        except sqlite3.Error as e:
            print(f"Error updating solution: {e}")
            return False

    def show_available_solutions(self):
        try:
            query="SELECT id, name FROM solutions"
            cursor = self.conn.execute(query)
            solutions = cursor.fetchall()
            return solutions if solutions else None
        except sqlite3.Error as e:
            print(f"Error retrieving solutions: {e}")
            return None
    
    def validate_solution_choice(self, choice, solutions):
        try:
            choice = int(choice)
            if any(solution[0] == choice for solution in solutions):
                return choice
            print("Invalid solution ID")
            return None
        except ValueError:
            print("Please enter a valid number")
            return None
        
    def delete_solution(self, solution_id):
        """Delete a solution and all of its associated flows."""
        try:
            # first delete all flows associated with the solution
            flows_query="SELECT id FROM flows WHERE solution_id=?"
            flows=self.conn.execute(flows_query, (solution_id,)).fetchall()

            for flow in flows:
                flow_id=flow[0]
                 # Delete flow logs for this flow
                self.conn.execute("DELETE FROM flow_logs WHERE flow_id = ?", (flow_id,))
                # Delete the flow
                self.conn.execute("DELETE FROM flows WHERE id = ?", (flow_id,))

            # Now delete the solution
            self.conn.execute("DELETE FROM solutions WHERE id = ?", (solution_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"An error occurred while deleting the solution: {e}")
            return False
        
    def bubble_sort_solutions(self,key_index=1):
        """
        Sort solutions using bubble sort by the given column index.
        key_index: 0 = id, 1 = name, 2 = description
        """
        try:
            solutions = self.get_solution()
            arr = list(solutions)
            n = len(arr)
            for i in range(n):
                for j in range(0, n-i-1):
                    if arr[j][key_index] > arr[j+1][key_index]:
                        arr[j], arr[j+1] = arr[j+1], arr[j]
            return arr
        except sqlite3.Error as e:
            print(f"Error sorting solutions: {e}")
            return None
    
    def linear_search_solution(self, solution_id, key_index = 1):
        """
        Search for a solution by name or ID using linear search.
        key_index: 0 = id, 1 = name, 2 = description
        """
        try:
            solutions = self.get_solution()
            for item in solutions:
                if item[key_index].lower() == solution_id.lower():
                    return item
            return None
        except sqlite3.Error as e:
            print(f"Error searching for solution: {e}")
            return None