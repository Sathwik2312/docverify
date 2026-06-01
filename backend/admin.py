from flask import request, send_file
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from backend.db import db_connection


class GetAllDocs(Resource):
    @jwt_required()
    def get(self):
        conn=None
        try:
            conn=db_connection()
            cur=conn.cursor()

            cur.execute("""

                SELECT
                    d.docid,
                    u.name,
                    d.doc_type,
                    COALESCE(d.status,'pending') as status

                FROM documents d

                INNER JOIN users u
                ON d.user_id=u.id

                ORDER BY d.docid DESC

            """)

            rows=cur.fetchall()

            cols=[c[0] for c in cur.description]

            data=[dict(zip(cols,row)) for row in rows]

            total=len(data)

            approved=len(
                [x for x in data if x["status"]=="approved"]
            )

            rejected=len(
                [x for x in data if x["status"]=="rejected"]
            )

            pending=len(
                [x for x in data if x["status"]=="pending"]
            )

            cur.close()

            return {
                "data":data,
                "total":total,
                "approved":approved,
                "pending":pending,
                "rejected":rejected
            }

        except Exception as e:
            print("ADMIN ERROR:",e)

            return {
                "data":[],
                "total":0,
                "approved":0,
                "pending":0,
                "rejected":0
            }

        finally:
            return_db_connection(conn)


class VerifyDoc(Resource):
    @jwt_required()
    def post(self):
        conn=None
        try:
            conn=db_connection()
            cur=conn.cursor()

            data=request.get_json()

            cur.execute(
                """

                UPDATE documents
                SET status=%s
                WHERE docid=%s

                """,
                (
                    data["status"],
                    data["docid"]
                )
            )

            conn.commit()

            cur.close()

            return {
                "status":"updated"
            }

        except Exception as e:
            print("VERIFY ERROR:",e)

            return {
                "status":"failed"
            }

        finally:
            return_db_connection(conn)


class DownloadDoc(Resource):
    @jwt_required()
    def get(self,docid):
        conn=None
        try:
            conn=db_connection()
            cur=conn.cursor()

            cur.execute(
                """

                SELECT file_path
                FROM documents
                WHERE docid=%s

                """,
                (docid,)
            )

            res=cur.fetchone()

            cur.close()

            if not res:

                return {
                    "status":"failed"
                }

            return send_file(
                res[0],
                as_attachment=True
            )

        except Exception as e:
            print("DOWNLOAD ERROR:",e)

            return {
                "status":"failed"
            }

        finally:
            return_db_connection(conn)