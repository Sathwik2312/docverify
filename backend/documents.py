from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from backend.db import db_connection


class UploadDoc(Resource):
    @jwt_required()
    def post(self):
        conn = db_connection()
        cur = conn.cursor()
        try:
            userid = int(get_jwt_identity())

            file = request.files.get("file")
            doc_type = request.form.get("doc_type")

            if not file:
                return {
                    "message": "File missing"
                }

            filename = file.filename

            path = os.path.join("uploads", filename)

            file.save(path)

            cur.execute(
                "INSERT INTO documents(user_id, doc_type, file_path) VALUES(%s,%s,%s)",
                (
                    userid,
                    doc_type,
                    path
                )
            )

            conn.commit()

            return {"message": "Upload successful"}

        except Exception as e:
            print("UPLOAD ERROR:", e)

            return {
                "message": "Upload failed"
            }

        finally:
            cur.close()
            return_db_connection(conn)


class GetUserDocs(Resource):
    @jwt_required()
    def post(self):
        conn = db_connection()
        cur = conn.cursor()
        try:
            userid = int(get_jwt_identity())

            cur.execute(
                "SELECT docid, doc_type, status FROM documents WHERE user_id=%s",
                (userid,)
            )

            rows = cur.fetchall()

            cols = [c[0] for c in cur.description]

            result = [dict(zip(cols, r)) for r in rows]

            return {
                "data": result
            }

        except Exception as e:
            print("DOCUMENT ERROR:", e)

            return {
                "data": []
            }

        finally:
            cur.close()
            return_db_connection(conn)