name: SnowSQL
env:
  SNOWSQL_DEST: ~/snowflake
  SNOWSQL_ACCOUNT: HYUGZMI-NFB65118
  SNOWSQL_USER: SANJU1209
  SNOWSQL_PWD: ${{ secrets.SNOWFLAKE_PASSWORD }}
  
on: push                                                  
jobs:                         
  executequery:                           
    name: Install SnowSQL                          
    runs-on: ubuntu-latest                           
    steps:
    - name: Checkout
      uses: actions/checkout@master
    - name: Download SnowSQL
      run:  curl -O https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/snowsql-1.2.9-linux_x86_64.bash
    - name: Install SnowSQL
      run: SNOWSQL_DEST=~/snowflake SNOWSQL_LOGIN_SHELL=~/.profile bash snowsql-1.2.9-linux_x86_64.bash
    - name: Test installation
      run:  ~/snowflake/snowsql -v
    - name: Execute SQL against Snowflake
      run:  ~/snowflake/snowsql -f .steps/3.USE_CASE_01.sql;
