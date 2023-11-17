import os
import subprocess

def execute_sql_scripts():
    # Define the directory containing your SQL scripts
    sql_script_dir = './steps/'

    # List all SQL script files in the directory
    sql_files = [f for f in os.listdir(sql_script_dir) if f.endswith('.sql')]

    # SnowSQL connection string
    snowsql_connection = 'dev'

    for sql_file in sql_files:
        # Construct the SnowSQL command
        snowsql_cmd = f"snowsql -c {snowsql_connection} -f {os.path.join(sql_script_dir, sql_file)}"
        
        # Execute the SQL script using subprocess
        try:
            subprocess.run(snowsql_cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing {sql_file}: {e}")
            # You can choose to handle errors or continue with the next script


# This will Deploy the SQL scripts in the steps folder
if __name__ == "__main__":
    execute_sql_scripts()
