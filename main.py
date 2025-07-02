from logger.flow_logger import FlowLogger
from logger.solution_handler import SolutionHandler
from logger.flow_handler import FlowHandler
from logger.developers_handler import DevelopersHandler
from logger.database import get_connection, initialize_all

def print_main_menu():
    print("\n1. Solution Management")
    print("2. Flow Management")
    print("3. Developer Management")
    print("4. View Flow Logs")

def main():
    conn=get_connection()
    initialize_all(conn)  

    logger = FlowLogger(conn)
    flow_handler= FlowHandler(conn)
    solution_handler = SolutionHandler(conn)
    developers_handler = DevelopersHandler(conn)

    while True:
        print_main_menu()
        main_choices = input("Select an option: ")

        if main_choices == '1':
            while True:
                print("\n1. Create Solution")
                print("2. View Solutions")
                print("3. Edit solution")
                print("4. Delete Solution")
                print("5. Return to Main Menu")
                solution_choice=input("Select an option: ")

                if solution_choice =='1':
                    name=input("Enter solution name: ")
                    description=input("Enter solution description: ")
                    success = solution_handler.create_solution(name, description)
                    if success:
                        print("Solution created successfully")
                    else:
                        print("Failed to create solution. Please try again.")

                elif solution_choice=='2':
                    print("\n View Solutions Options:")
                    print("1. View all (unsorted)")
                    print("2. Sort by name")
                    print("3. Search by name")
                    sub_choice = input("Select an option: ")

                    if sub_choice == '1':
                        solutions = solution_handler.get_solution()
                        for s in solutions:
                            print(f"\nID: {s[0]}")
                            print(f"Name: {s[1]}")
                            print(f"Description: {s[2]}")
                            print(f"Created At: {s[3]}")
                    
                    elif sub_choice == '2':
                        sorted_list = solution_handler.bubble_sort_solutions(key_index=1)
                        print("\nSorted Solutions by Name:")
                        for s in sorted_list:
                            print(f"\nID: {s[0]}")
                            print(f"Name: {s[1]}")
                            print(f"Description: {s[2]}")
                            print(f"Created At: {s[3]}")

                    elif sub_choice == '3':
                        name = input("Enter solution name to search: ")
                        found = solution_handler.linear_search_solution(name, key_index=1)
                        if found:
                            print(f"\nID: {found[0]}")
                            print(f"Name: {found[1]}")
                            print(f"Description: {found[2]}")
                            print(f"Created At: {found[3]}")
                        else:
                            print("No solution found with that name")

                elif solution_choice == '3':
                    solutions = solution_handler.get_solution()
                    if solutions:
                        print("\nAvailable Solutions:")
                        for sol in solutions:
                            print(f"ID: {sol[0]}, Name: {sol[1]}")
                        while True:
                            try:
                                sol_id = int(input("Enter solution ID to edit: "))
                                confirm = input("Are you sure you want to edit this solution? (yes/no): ")
                                if confirm.lower() == 'yes':
                                    name = input("Enter new solution name: ")
                                    description = input("Enter new solution description: ")
                                    solution_handler.update_solution(sol_id, name, description)
                                    print("Solution updated successfully")
                                break
                            except ValueError:
                                print("Please enter a valid numeric ID")
                    else:
                        print("No solutions found")
                        continue    

                elif solution_choice == '4':
                    solutions=solution_handler.get_solution()
                    if solutions:
                        print("\nAvailable Solutions:")
                        for sol in solutions:
                            print(f"ID: {sol[0]}, Name: {sol[1]}")
                        while True:
                            try:
                                sol_id=int(input("Enter solution ID to delete: "))
                                confirm=input("Are you sure you want to delete this solution? Please note that this will also delete all associated flows. (yes/no): ")
                                if confirm.lower() == 'yes':
                                    if solution_handler.delete_solution(sol_id):
                                        print("Solution deleted successfully")
                                    else:
                                        print("Failed to delete solution")
                                break
                            except ValueError:
                                print("Please enter a valid numeric ID")
                    else:
                        print("No solutions found")
                        continue

                elif solution_choice=='5':
                    break

        elif main_choices == '2':
            while True:
                print("\n1. Create Flow")
                print("2. View Flows")
                print("3. Update Flow Status")
                print("4. Assign Developer to Flow")
                print("5. Delete Flow") 
                print("6. Return to Main Menu")
                flow_choice = input("Select an option: ")

                if flow_choice == '1':
                    solutions = solution_handler.show_available_solutions()
                    if solutions:
                        print("\nAvailable Solutions:")
                        for sol in solutions:
                            print(f"ID: {sol[0]}, Name: {sol[1]}")

                        while True:
                            try:
                                solution_id = int(input("Enter the Solution ID to create a flow: "))
                                # Check if the solution exists
                                cursor = solution_handler.conn.execute("SELECT id FROM solutions WHERE id = ?", (solution_id,))
                                if cursor.fetchone():
                                    title = input("Enter flow title: ")
                                    description = input("Enter flow description: ")
                                    priority = input("Enter flow priority (Low, Medium, High, Critical): ")

                                    # Get a list of developers to assign as creator
                                    developers = developers_handler.get_developers()
                                    if developers:
                                        print("\nAvailable Developers:")
                                        for dev in developers:
                                            print(f"ID: {dev[0]}, Name: {dev[1]}")
                                        
                                        creator_id = int(input("Enter your developer ID (creator): "))

                                        # Validate Creator ID
                                        cursor = developers_handler.conn.execute("SELECT id FROM developers WHERE id = ?", (creator_id,))
                                        if cursor.fetchone():
                                            status = 'New'  # Default status for new flows
                                            success = flow_handler.create_flow(title, description, solution_id, priority, creator_id)
                                            if success:    
                                                print("Flow created successfully")
                                            else: 
                                                print("Failed to create flow")
                                            break
                                        else:
                                            print("Invalid developer ID.")
                                    else:
                                        print("No developers available to assign as creator")
                                        break
                                else:
                                    print("Invalid Solution ID")
                            except ValueError:
                                    print("Please enter a valid numeric ID")
                    else:
                        print("No solutions available to create a flow. Please create a solution first.")
                        continue

                elif flow_choice == '2':
                    solution_id=input("View all flows or flows for a specific solution? (a or s): ")
                    flows=None

                    if solution_id.lower() == 's':
                        # Display available solutions
                        solutions = solution_handler.get_solution()
                        if solutions:
                            print("\nAvailable Solutions:")
                            for sol in solutions:
                                print(f"ID: {sol[0]}, Name: {sol[1]}")
                            while True:
                                try:
                                    sol_id = int(input("Enter the Solution ID to view its flows: "))
                                    flows = flow_handler.get_flows(sol_id)
                                    if flows is None:
                                        print("Invalid Solution ID")
                                    break
                                except ValueError:
                                    print("Please enter a valid numeric ID")    
                    else:
                        flows=flow_handler.get_flows()
                    
                    if flows:
                        for flow in flows:
                            # Get assignee from developers table
                            cursor = developers_handler.conn.execute("SELECT name FROM developers WHERE id = ?", (flow[6],))
                            owner = cursor.fetchone()
                            assigned_name = owner[0] if owner else "Unassigned"

                            # Get creator from developers table
                            cursor = developers_handler.conn.execute("SELECT name FROM developers WHERE id = ?", (flow[7],))
                            creator = cursor.fetchone()
                            creator_name = creator[0] if creator else "Unknown Creator"

                            print("\n" + "="*30)
                            print(f"ID: {flow[0]}")
                            print(f"Title: {flow[1]}")
                            print(f"Description: {flow[2]}")
                            print(f"Solution ID: {flow[3]}")
                            print(f"Status: {flow[4]}")
                            print(f"Priority: {flow[5]}")
                            print(f"Assignee: {assigned_name}")
                            print(f"Creator: {creator_name}")
                            print(f"Created: {flow[8]}")
                            print(f"Updated: {flow[9]}")
                    else:
                        print("\nNo flows found")

                elif flow_choice == '3':
                    flows = flow_handler.get_flows()
                    if flows:
                        print("\nAvailable Flows:")
                        for flow in flows:
                            print(f"ID: {flow[0]}, Title: {flow[1]}")
                        while True:
                            try:
                                flow_id = input("Enter flow ID to update status: ")
                                status = input("Enter new status (New, In Progress, Blocked, Completed): ")
                                flow_handler.update_flow_status(flow_id, status)
                                print("Flow status updated successfully")
                                break
                            except ValueError:
                                print("Please enter a valid numeric ID")
                    else:
                        print("No flows available to update")
                        continue                           

                elif flow_choice == '4':
                    flows = flow_handler.get_flows()
                    if flows:
                            print("\nAvailable Flows:")
                            for flow in flows:
                                print(f"ID: {flow[0]}, Title: {flow[1]}")

                            # Get list of developers
                            developers = developers_handler.get_developers()
                            if developers:
                                print("\nAvailable Developers:")
                                for dev in developers:
                                    print(f"ID: {dev[0]}, Name: {dev[1]}")
                            else:
                                print("No developers available to assign to flow")
                                continue

                            while True:
                                try:
                                    flow_id=int(input("Enter flow ID to assign developer: "))
                                    owner = int(input("Enter developer ID to assign to this flow: "))

                                    # Check if the developer exists
                                    cursor = developers_handler.conn.execute("SELECT id FROM developers WHERE id = ?", (owner,))
                                    dev_result = cursor.fetchone()
                                    if dev_result:
                                        # proceed with assignment
                                        cursor = flow_handler.conn.execute("SELECT status FROM flows WHERE id = ?", (flow_id,))
                                        status_result = cursor.fetchone()
                                        if status_result:
                                            status = status_result[0]
                                            success = flow_handler.assigned(flow_id, owner, status)
                                            if success:   
                                                print("Developer assigned successfully")
                                            else:
                                                print("Error in assigning developer ID to flow")
                                            break
                                        else:
                                            print("Invalid flow ID")
                                    else:
                                        print("Developer not found")
                                        continue
                                except ValueError:
                                    print("Please enter a valid numeric ID")

                elif flow_choice == '5':
                    flows=flow_handler.get_flows()
                    if flows:
                        print("\nAvailable Flows:")
                        for flow in flows:
                            print(f"ID: {flow[0]}, Title: {flow[1]}")
                        while True:
                            try:
                                flow_id = int(input("Enter flow ID to delete: "))
                                confirm = input("Are you sure you want to delete this flow? (yes/no): ")
                                if confirm.lower() == 'yes':
                                    if flow_handler.delete_flow(flow_id):
                                        print("Flow deleted successfully")
                                    else:
                                        print("Failed to delete flow")
                                break
                            except ValueError:
                                print("Please enter a valid numeric ID")
                    else:
                        print("No flows found")
                        continue

                elif flow_choice == '6':
                    break

        elif main_choices == '3':
            while True:
                print("\n1. Add Developer")
                print("2. View Developers")
                print("3. Update Developer's details")
                print("4. Delete Developer")
                print("5. Return to Main Menu")
                dev_choice = input("Select an option: ")

                if dev_choice == '1':
                    name = input("Enter developer's name: ")
                    email = input("Enter developer's email: ")
                    success = developers_handler.add_developers(name, email)
                    if success:
                        print("Developer added successfully")
                    else:
                        print("Failed to add developer.")

                elif dev_choice == '2':
                    developers = developers_handler.get_developers()
                    if developers:
                        for dev in developers:
                            print(f"\nID: {dev[0]}")
                            print(f"Name: {dev[1]}")
                            print(f"Email: {dev[2]}")
                    else:
                        print("No developers found")

                elif dev_choice == '3':
                    # Display all developers
                    developers = developers_handler.get_developers()
                    if developers:
                        print("\n Current Developers:")
                        for dev in developers:
                            print(f"ID: {dev[0]}, Name: {dev[1]}, Email: {dev[2]}")
                        dev_id= input("Enter developer ID to update: ")
                        new_name = input("Enter new name: ")
                        new_email = input("Enter new email: ")
                        success = developers_handler.update_developers(dev_id, new_name, new_email)
                        if success:
                            print("Developer updated successfully")
                        else:
                            print("No developers found to update")

                elif dev_choice == '4':
                    # Display all developers
                    developers = developers_handler.get_developers()
                    if developers:
                        print("\n Current Developers:")
                        for dev in developers:
                            print(f"ID: {dev[0]}, Name: {dev[1]}, Email: {dev[2]}")
                        dev_id = input("Enter developer ID to delete: ")
                        confirm = input("Are you sure you want to delete this developer? (yes/no): ")
                        if confirm.lower() == 'yes':
                            success = developers_handler.delete_developers(dev_id)
                            if success:
                                print("Developer deleted successfully")
                            else:
                                print("Failed to delete developer")

                elif dev_choice == '5':
                    break

        elif main_choices == '4':
            logs=logger.read_logs()
            for log in logs:
                print(f"\nID: {log[0]}")
                print(f"Flow Name: {log[1]}")
                print(f"Status: {log[2]}")
                print(f"Timestamp: {log[3]}")
                print(f"Details: {log[4]}")
                if log[5]:
                    print(f"Flow ID: {log[5]}")

if __name__ == "__main__":
    main()