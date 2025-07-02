import sqlite3

def get_connection(db_name='flow_logs.db'):
    """Create a database connection to the SQLite database specified by db_name."""
    conn=sqlite3.connect(db_name)
    return conn

def initialize_solution_db(conn):
    """Create solution table"""
    query='''CREATE TABLE IF NOT EXISTS solutions
                (id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP)'''
    conn.execute(query)
    conn.commit()

def initialize_developers_db(conn):
    """Create developers table"""
    query='''CREATE TABLE IF NOT EXISTS developers
                (id INTEGER PRIMARY KEY, 
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE)'''
    conn.execute(query)
    conn.commit()

def initialize_flows_db(conn):
    """Create the flows table with foreign keys to solutions and developers."""
    query = '''
    CREATE TABLE IF NOT EXISTS flows (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT,
        priority TEXT,
        solution_id INTEGER,
        assigned_id INTEGER,
        creator_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (solution_id) REFERENCES solutions(id),
        FOREIGN KEY (assigned_id) REFERENCES developers(id),
        FOREIGN KEY (creator_id) REFERENCES developers(id)
    )'''
    conn.execute(query)
    conn.commit()

def initialize_logs_db(conn):
    """Create the flow_logs table with a foreign key to flows."""
    query = '''
    CREATE TABLE IF NOT EXISTS flow_logs (
        id INTEGER PRIMARY KEY,
        flow_name TEXT,
        status TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        details TEXT,
        flow_id INTEGER,
        FOREIGN KEY (flow_id) REFERENCES flows(id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )'''
    conn.execute(query)
    conn.commit()      

def initialize_all(conn):
    """Initialize all tables in the correct order."""
    initialize_solution_db(conn)
    initialize_developers_db(conn)
    initialize_flows_db(conn)
    initialize_logs_db(conn)

