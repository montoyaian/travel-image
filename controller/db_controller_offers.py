from Classes.offers import Offer
import mysql.connector
import pyodbc

DELETE_SUCCESS = {"message": "eliminacion completa"}

class DatabaseControllerOffers():

    def insert_offer(self, offer:Offer):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        cursor = connection.cursor()
        if offer.flight_type == "standard class":
            cursor.execute(
            """SELECT * FROM dbo.standard_class WHERE id = ?""",
            (offer.id_flight,),
            )
            result = cursor.fetchone()
            if result:
                cursor.execute("""INSERT INTO dbo.Offers(
                Id_flight,
                Discount,
                Customer_type,
                Flight_type
                ) VALUES (?, ?, ?, ?)""",
                (
                offer.id_flight,
                offer.discount,
                offer.customer_type,
                offer.flight_type
                ))
                connection.commit()
                
                offerj = {
                    "Id_flight":offer.id_flight,
                    "Discount":offer.discount,
                    "Customer_type":offer.customer_type,
                    "Flight_type":offer.flight_type
                    }
                return offerj
            else:
                return{"error": "id de vuelo no encotrado"}
            
        elif offer.flight_type == "first class":
            cursor = connection.cursor()
            cursor.execute(
            """SELECT * FROM dbo.first_class WHERE id = ?""",
            (offer.id_flight,),
            )
            result = cursor.fetchone()
            if result:
                cursor.execute(      """INSERT INTO  dbo.Offers(
                Id_flight,
                Discount,
                Customer_type,
                Flight_type
                ) VALUES (?, ?, ?, ?)""",
                (
                offer.id_flight,
                offer.discount,
                offer.customer_type,
                offer.flight_type
                ))
                connection.commit()
                
                offerj = {
                    "Id_flight":offer.id_flight,
                    "Discount":offer.discount,
                    "Customer_type":offer.customer_type,
                    "Flight_type":offer.flight_type
                    }
                return offerj
            else:
                return{"error": "id de vuelo no encotrado"} 
        else:
            return{"error": "tipo de vuelo no encotrado"}   
        
    def edit_offer(self,offer:Offer):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        cursor = connection.cursor()
        cursor.execute(
        """SELECT * FROM dbo.Offers WHERE id = ?""",
        (offer.id,),
        )
        result = cursor.fetchone()
        if result:
            if offer.flight_type == "standard class":
                cursor.execute(
                """SELECT * FROM dbo.standard_class WHERE id = ?""",
                (offer.id_flight,),
                )
                result = cursor.fetchone()
                if result:
                    cursor.execute("""UPDATE dbo.Offers SET
                    Id_flight = ?,
                    Discount = ?,
                    Customer_type = ?,
                    Flight_type = ?
                    WHERE id = ?""",
                    (
                    offer.id_flight,
                    offer.discount,
                    offer.customer_type,
                    offer.flight_type,
                    offer.id
                    ))
                    connection.commit()
                    
                    offerj = {
                        "ID":offer.id,
                        "Id_flight":offer.id_flight,
                        "Discount":offer.discount,
                        "Customer_type":offer.customer_type,
                        "Flight_type":offer.flight_type
                        }
                    return offerj
                else:
                    return{"error": "id de vuelo no encotrado"}            
            elif offer.flight_type == "first class":
                cursor.execute(
                """SELECT * FROM dbo.first_class WHERE id = ?""",
                (offer.id_flight,),
                )
                result = cursor.fetchone()
                if result:
                    cursor.execute(      """UPDATE dbo.Offers SET
                    Id_flight = ?,
                    Discount = ?,
                    Customer_type = ?,
                    Flight_type = ?
                    WHERE id = ?""",
                    (
                    offer.id_flight,
                    offer.discount,
                    offer.customer_type,
                    offer.flight_type,
                    offer.id
                    ))
                    connection.commit()
                    
                    offerj = {
                        "ID":offer.id,
                        "Id_flight":offer.id_flight,
                        "Discount":offer.discount,
                        "Customer_type":offer.customer_type,
                        "Flight_type":offer.flight_type
                        }
                    return offerj
                else:
                    return{"error": "id de vuelo no encotrado"} 
            else:
                return{"error": "tipo de vuelo no encotrado"}            
        else:
            return{"error": "reserva no encontrada"}     
    
    def delete_offer(self, id:int):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        cursor = connection.cursor()
        """
        Delete a offer from database
        """
        cursor.execute(
        """SELECT * FROM dbo.Offers WHERE id = ?""",
        (id,),
        )
        result = cursor.fetchone()
        if result:
            cursor.execute("""DELETE FROM dbo.Offers  WHERE id = ?""", (id,))
            connection.commit()
            
            return DELETE_SUCCESS   
        else:
            return {"error":"oferta no encontrada"} 
    
    def show_offer(self, id:str):
        conn_str = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=appservermontoya.database.windows.net;DATABASE=appdb;UID=sqladmin;PWD=Azure@123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connection = pyodbc.connect(conn_str)      
        cursor = connection.cursor()
        if id == "all":
            cursor.execute(
                '''SELECT * FROM dbo.Offers''')
            rows = cursor.fetchall()
            rowsj=[]
            for i in rows:
                rowj ={
                "id":i[0],
                "Id_flight":i[1],
                "Discount":i[2],
                "Customer_type":i[3],
                "Flight_type":i[4]
                }
                rowsj.append(rowj)
    
            return rowsj
        else:
            try:
                cursor.execute(
                '''SELECT * FROM dbo.Offers WHERE ID = ?''',(id,))
                rows = cursor.fetchone()
                rowj = {
                "id":rows[0],
                "Id_flight":rows[1],
                "Discount":rows[2],
                "Customer_type":rows[3],
                "Flight_type":rows[4]
                }
 
                return rowj
            except:
                {"message" : "datos no validos"}