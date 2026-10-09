
from database.DB_connect import DBConnect
from model.registi import Regista


class DAO:
    @staticmethod
    def getAllMovies():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select * from movie m """

        cursor.execute(query)

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes( data1, data2):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct  n.*
                    from  names n, director_mapping dm  , movie m 
                    where n.id =dm.name_id and 
                    dm.movie_id =m.id 
                    and m.date_published between %s and %s
                                        """

        cursor.execute(query, (data1, data2))

        for row in cursor:
            results.append(Regista(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getFilmPerRegista(id, data1, data2):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """  select distinct m.id as movie_id , g.genre  as genere, m.worlwide_gross_income as incasso
                from movie m, director_mapping dm , genre g 
                where dm.movie_id =m.id  
                and g.movie_id =m.id 
                and dm.name_id =%s 
                AND m.date_published BETWEEN %s AND %s"""

        cursor.execute(query, (id,data1, data2))

        for row in cursor:
            results.append((row["movie_id"], row["genere"], row["incasso"]))

        cursor.close()
        conn.close()
        return results



