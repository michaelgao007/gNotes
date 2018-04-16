# **Overview**

This project creates a GUI-based notes search tool with Python plus MySQL structure.

# **1. MySQL Setup**

**1. Create a MySQL database 'notesdb' and a table 'NotesSearch' within the database for this example**

mysql> USE notesdb
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> SHOW TABLES;
+-------------------+
| Tables_in_notesdb |
+-------------------+
| NotesSearch       |
+-------------------+
1 row in set (0.00 sec)

mysql> DESCRIBE NotesSearch;
+-------+---------------+------+-----+---------+-------+
| Field | Type          | Null | Key | Default | Extra |
+-------+---------------+------+-----+---------+-------+
| Title | varchar(2000) | NO   |     | NULL    |       |
| Text  | varchar(2000) | NO   |     | NULL    |       |
+-------+---------------+------+-----+---------+-------+

**2. To allow MySQL connections in iptables**

/etc/sysconfig/iptables

-A INPUT -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT

# **2. GUI Client**

**1. gNotes.py**

1) Python Version: Python 3.5.1 (lower version will not work)

2) Python Modules:

- pymysql
- tkinter
- notesConfig (customized config file notesConfig.py)

**2. Run 'gNotes.py' to search and add new notes to the database**
