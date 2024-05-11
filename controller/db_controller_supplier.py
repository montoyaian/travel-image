import mysql.connector
from Classes.supplier import Supplier
import pyodbc

DELETE_SUCCESS = {"message": "eliminacion completa"}

class DatabaseControllerSupplier():
    """
    This class is used to connect to the database and execute queries
    """

    def insert_supplier(self, supplier:Supplier ):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO  dbo.supplier(
        Name,
        Contact,
        Description
        ) VALUES (?,?, ?)""",
        (
        supplier.name,
        supplier.contact,
        supplier.description,
        ))
        connection.commit()
        supplierj = {
        "name": supplier.name,
        "contact": supplier.contact,
        "Description": supplier.description,
        }

        return supplierj      


     
    def edit_supplier(self,supplier:Supplier ):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM dbo.supplier WHERE ID = ?""", (supplier.id,))
        result = cursor.fetchone()

        if not result :
            return {"error":"proveedor no encontrado"}

        cursor.execute("""UPDATE dbo.supplier SET 
        Name = ?,
        Contact = ?,
        Description = ?
        WHERE ID = ?""",
        (
        supplier.name,
        supplier.contact,
        supplier.description,
        supplier.id,
        ))
        connection.commit()
        supplierj = {
        "id": supplier.id,
        "name": supplier.name,
        "contact": supplier.contact,
        "Description": supplier.description,
        }
        return supplierj

    def delete_supplier(self, id:int):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        """
        Delete a supplier from database
        """
        cursor = connection.cursor()
        
        cursor.execute(
        """SELECT * FROM dbo.supplier WHERE id = ?""",
        (id,),
        )
        result = cursor.fetchone()
        if result:
            cursor.execute("""DELETE FROM dbo.supplier  WHERE id = ?""", (id,))      
            cursor.execute("""DELETE FROM dbo.first_class  WHERE ID_agency = ?""", (id,))
            cursor.execute("""DELETE FROM dbo.standard_class  WHERE ID_agency = ?""", (id,))
            connection.commit()
                      
            return DELETE_SUCCESS
        else:
            return {"error":"proveedor no encontrado"}        

    def show_supplier(self,id:str):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        cursor = connection.cursor()
        if id == "all":
            cursor.execute(
            '''SELECT * FROM dbo.supplier''')
            rows = cursor.fetchall()
            rowsj=[]
            for i in rows:
                rowj ={
                "id" : i[0],
                "name": i[1],
                "contact": i[2],
                "Description": i[3],
                }
                rowsj.append(rowj)
  
            return rowsj
        else:
            try:
                id = int(id)
                cursor.execute(
                '''SELECT * FROM dbo.supplier WHERE id = ?''',(id,))
                rows = cursor.fetchall()
                rowj = {
                    "id": rows[0][0],
                    "name": rows[0][1],
                    "contact": rows[0][2],
                    "Description": rows[0][3]
                }
                return rowj
            except:
                {"message" : "datos no validos"}   
    def show_supplier_name(self):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        cursor = connection.cursor()
        cursor.execute(
            '''SELECT * FROM dbo.supplier''')
        rows = cursor.fetchall()
        rowsj = []
        for i in rows:
            rowj ={
            "id" : i[0],
            "name": i[1]
            }
            rowsj.append(rowj)

        return rowsj
