from Classes.first_class import Firstclass
from Classes.standard_class import Standardclass
from datetime import date
import mysql.connector
import pyodbc

DELETE_SUCCESS = {"message": "eliminacion completa"}




class DatabaseControllerFlight():
    """
    This class is used to connect to the database and execute queries
    """

    def insert_flight(self, flight: Firstclass or Standardclass):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        cursor = connection.cursor()
        cursor.execute(
        """SELECT * FROM dbo.supplier WHERE id = ?""",
        (flight.id_agency,),
        )
        result = cursor.fetchone()
        if result:
            if flight.positions > 0:
                if flight.date >= date.today():
                    if isinstance(flight, Firstclass):
                        cursor.execute(      """INSERT INTO  dbo.first_class(
                        Origin,
                        Destination,
                        Date,
                        Positions,
                        Hour,
                        Id_agency,
                        Premium_cost
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (
                        flight.origin,
                        flight.destination,
                        flight.date,
                        flight.positions,
                        flight.hour,
                        flight.id_agency,
                        flight.premium_cost,
                        ))
                        connection.commit()
                        
                        flightj = {
                        "origin": flight.origin,
                        "destination": flight.destination,
                        "date": flight.date,
                        "positions": flight.positions,
                        "hour": flight.hour,
                        "id_agency": flight.id_agency,
                        "premium_cost": flight.premium_cost
                        }
                        return flightj

            
                    elif isinstance(flight, Standardclass):
                        cursor.execute(      """INSERT INTO  dbo.standard_class(
                        Origin,
                        Destination,
                        Date,
                        Positions,
                        Hour,
                        Id_agency,
                        standard_cost
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (
                        flight.origin,
                        flight.destination,
                        flight.date,
                        flight.positions,
                        flight.hour,
                        flight.id_agency,
                        flight.standard_cost,
                        ))
                        connection.commit()
                        
                        flightj = {
                        "origin": flight.origin,
                        "destination": flight.destination,
                        "date": flight.date,
                        "positions": flight.positions,
                        "hour": flight.hour,
                        "id_agency": flight.id_agency,
                        "standard_cost": flight.standard_cost
                        }
                        return flightj    
                else:
                    return{"error": "fecha no valida"}
            else:
                return{"error": "cantidad de puestos no aceptada"}
        else:
            return{"error":"proveedor no encontrado"}

    def edit_flight(self, flight:Standardclass or Firstclass):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        cursor = connection.cursor()
        cursor.execute(
        """SELECT * FROM dbo.supplier WHERE id = ?""",
        (flight.id_agency,),
        )
        result = cursor.fetchone()
        if result:
            if isinstance(flight, Standardclass):
                cursor.execute(
                """SELECT * FROM dbo.standard_class WHERE id = ?""",
                (flight.id,),
                 )
                result = cursor.fetchone()
                if result:
                    if flight.positions > 0:
                        if flight.date >= date.today():
                            cursor.execute(
                                """UPDATE dbo.standard_class SET
                                Origin=?,
                                Destination=?,
                                Date= ?,
                                Positions=?,
                                Hour=?,
                                Id_agency=?,
                                standard_cost=?
                                WHERE id = ?""",
                                (
                                    flight.origin,
                                    flight.destination,
                                    flight.date,
                                    flight.positions,
                                    flight.hour,
                                    flight.id_agency,
                                    flight.standard_cost,
                                    flight.id,
                                ),
                            )
                            connection.commit()
                            cursor.execute(
                            """SELECT * FROM dbo.standard_class WHERE id = ?""",
                            (flight.id,),
                            )
                            updated_flight = cursor.fetchone()

                            updated_flight_dict = {
                                "id": updated_flight[0], 
                                "origin": updated_flight[1],
                                "destination": updated_flight[2],
                                "date": updated_flight[3],
                                "positions": updated_flight[4],
                                "hour": updated_flight[5],
                                "id_agency": updated_flight[6],
                                "standard_cost": updated_flight[7]
                            }
                            
                            return updated_flight_dict
                        
                        else:
                            return{"error": "fecha no valida"}
                    else:
                        return{"error": "cantidad de puestos no aceptada"}
                else:
                    return{"error": "vuelo no encontrado"}
           
            elif isinstance(flight, Firstclass):
                cursor.execute(
                """SELECT * FROM dbo.first_class WHERE id = ?""",
                (flight.id,),
                )
                result = cursor.fetchone()
                if result:
                    if flight.positions > 0:
                        if flight.date >= date.today():
                            cursor.execute(
                                """UPDATE dbo.first_class SET
                                Origin=?,
                                Destination=?,
                                Date=?,
                                Positions=?,
                                Hour=?,
                                Id_agency=?,
                                premium_cost=?
                                WHERE id = ?""",
                                (
                                flight.origin,
                                flight.destination,
                                flight.date,
                                flight.positions,
                                flight.hour,
                                flight.id_agency,
                                flight.premium_cost,
                                flight.id,
                                ),
                            )
                            connection.commit()
                            cursor.execute(
                            """SELECT * FROM dbo.first_class WHERE id = ?""",
                            (flight.id,),
                            )
                            updated_flight = cursor.fetchone()

                            updated_flight_dict = {
                                "id": updated_flight[0],  
                                "origin": updated_flight[1],
                                "destination": updated_flight[2],
                                "date": updated_flight[3],
                                "positions": updated_flight[4],
                                "hour": updated_flight[5],
                                "id_agency": updated_flight[6],
                                "premium_cost": updated_flight[7]
                            }
                            
                            return updated_flight_dict
                        else:
                            return{"error": "fecha no valida"}
                    else:
                        return{"error": "cantidad de puestos no aceptada"}
                else:
                    return{"error": "vuelo no encontrado"}
        else:
            return{"error": "proveedor no encontrado"}
                        
    def delete_flight(self, id: int, class_type: str):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        """
        Delete a flight from database
        """
        cursor = connection.cursor()
        class_type.lower()
        if (class_type == "first class"):
            cursor.execute(
            """SELECT * FROM dbo.first_class WHERE id = ?""",
            (id,),
            )
            result = cursor.fetchone()
            if result:
                cursor.execute("""DELETE FROM dbo.first_class WHERE id = ?""", (id,))
                cursor.execute("""DELETE FROM dbo.bookings WHERE Id_flight= ? AND Type_flight = 'first class'""", (id,))
                cursor.execute("""DELETE FROM dbo.Offers WHERE Id_flight = ?""", (id,))
                connection.commit()
                return DELETE_SUCCESS
            else:
                return{"error": "vuelo no encontrado"}            
        elif (class_type == "standard class"):
            cursor.execute(
            """SELECT * FROM dbo.standard_class WHERE id = ?""",
            (id,),
            )
            result = cursor.fetchone()
            if result:
                cursor.execute("""DELETE FROM dbo.standard_class WHERE id = ?""", (id,))
                cursor.execute("""DELETE FROM dbo.bookings WHERE Id_flight= ? AND Type_flight = 'standard class'""", (id,))
                cursor.execute("""DELETE FROM dbo.Offers WHERE Id_flight = ?""", (id,))
                connection.commit()
                
                return DELETE_SUCCESS
            else:
                return{"error": "vuelo no encontrado"} 
        else:
            return {"error":"tipo de vuelo no encontrado"}      
            
    def show_flight(self, table_name:str,id:str ):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        cursor = connection.cursor()
        try:
            if table_name == "all":
                cursor.execute('SELECT * FROM dbo.first_class')
                rows = cursor.fetchall()
                cursor.execute('SELECT * FROM dbo.standard_class')
                rows += cursor.fetchall()
                rowsj=[]
                for i in rows:
                    print(i[5])
                    rowj ={
                    "id" : i[0],
                    "origin": i[1],
                    "destination": i[2],
                    "date": i[3],
                    "positions": i[4],
                    "hour": i[5],
                    "id_agency": i[6],
                    "cost": i[7]
                    }
                    rowsj.append(rowj)
    
                return rowsj
                
            else:
                if id == "all":
                    cursor.execute(
                        '''SELECT * FROM dbo.{}'''.format(table_name))
                    rows = cursor.fetchall()
                    rowsj=[]
                    for i in rows:
                        rowj ={
                        "id" : i[0],
                        "origin": i[1],
                        "destination": i[2],
                        "date": i[3],
                        "positions": i[4],
                        "hour": i[5],
                        "id_agency": i[6],
                        "cost": i[7]
                        }
                        rowsj.append(rowj)
    
                    return rowsj
                else:
                    cursor.execute(
                        '''SELECT * FROM dbo.{} WHERE id = {}'''.format(table_name, id))
                    rows = cursor.fetchall()
                    rowj ={
                    "id" :  rows[0][0],
                    "origin": rows[0][1],
                    "destination": rows[0][2],
                    "date":rows[0][3],
                    "positions": rows[0][4],
                    "hour": rows[0][5],
                    "id_agency": rows[0][6],
                    "cost": rows[0][7]
                    }
                    return rowj
        except:
            return{"message":"datos no encontrados"}
       
