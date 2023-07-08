# CSE16Attendance

To do a moderated scan (scanning all at once and comparing)
  Run AttedenceUsingRosterScannerComparison.py
        1) Scan barcodes into a .txt file
        2) Upload this file and the roster file to compare

To do a un-moderated scan (leaving it open for periodic scans): 
  Run database.py
  
  Install MySQL Workbench:
  
  Click '+' next to MySQL Connections to create a connection
  
    Can leave name as default name: 'root'
    
    Press 'Test Connection'
    
  Once you're in your connection go to the schema tab on the left
  
  Right click and click on 'Create Schema' and name it
  
  Your schema should show up in the left hand schema tab
  
  Click on your schema's name
  
  Right click on tables and go to 'Create Table'
  
  Title the column ID
  
  

  In database.py's connectToDatabase method:
  
  Change database parameter to be schema's name (in the schema's tab)

Password will be the password you set when you initialized your workbench



