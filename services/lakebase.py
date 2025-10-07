import os
import uuid
import time
import psycopg2
from databricks.sdk import WorkspaceClient


class LakebaseService:
    """Singleton service for Lakebase database connections"""
    
    _instance = None
    _connection = None
    _connection_time = None
    _workspace_client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def _get_connection(self):
        """Get or refresh the database connection"""
        current_time = time.time()
        
        # Check if we need to create a new connection or refresh
        if self._connection is None or self._connection_time is None:
            # First time connection
            self._create_connection()
        elif (current_time - self._connection_time) > (59 * 60):
            # Connection is older than 59 minutes, refresh it
            self._close_connection()
            self._create_connection()
        
        return self._connection
    
    def _create_connection(self):
        """Create a new database connection with fresh token"""
        # Initialize workspace client if not already done
        if self._workspace_client is None:
            self._workspace_client = WorkspaceClient(
                host=os.getenv("DATABRICKS_HOST"),
                client_id=os.getenv("DATABRICKS_CLIENT_ID"),
                client_secret=os.getenv("DATABRICKS_CLIENT_SECRET")
            )
        
        # Get environment variables
        instance_name = os.getenv("LAKEBASE_INSTANCE_NAME")
        db_name = os.getenv("LAKEBASE_DB_NAME")
        db_user = "2025_vibe_coding"  # hardcoded group name
        
        # Generate database credential
        cred = self._workspace_client.database.generate_database_credential(
            request_id=str(uuid.uuid4()), 
            instance_names=[instance_name]
        )
        
        # Get database instance
        instance = self._workspace_client.database.get_database_instance(name=instance_name)
        
        # Create connection
        self._connection = psycopg2.connect(
            host=instance.read_write_dns,
            dbname=db_name,
            user=db_user,
            password=cred.token,
            sslmode="require",
        )
        
        self._connection_time = time.time()
    
    def _close_connection(self):
        """Close the current connection"""
        if self._connection:
            try:
                self._connection.close()
            except Exception:
                pass
            self._connection = None
            self._connection_time = None
    
    def query(self, sql: str):
        """
        Execute a SQL query and return rows
        
        Args:
            sql: SQL query string to execute
            
        Returns:
            List of rows returned by the query
            
        Raises:
            Exception: If query execution fails
        """
        conn = self._get_connection()
        
        with conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.commit()
            return rows


# Singleton instance
Lakebase = LakebaseService()

