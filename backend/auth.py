from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from backend.db import db_connection


class Register(Resource):
    def post(self):
        conn=None
        try:
            conn=db_connection()
            cur=conn.cursor()
            data=request.get_json()

            if not data.get("name") or not data.get("email") or not data.get("password"):

                return {
                    "status":"failed",
                    "message":"Missing fields"
                }

            cur.execute(
                """
                INSERT INTO users(
                    name,
                    email,
                    password,
                    role
                )
                VALUES(%s,%s,%s,%s)
                RETURNING id
                """,
                (
                    data["name"],
                    data["email"],
                    data["password"],
                    "user"
                )
            )

            userid=cur.fetchone()[0]

            conn.commit()

            return {
                "status":"success",
                "userid":userid
            }

        except Exception as e:
            print("REGISTER ERROR:",e)

            return {
                "status":"failed",
                "error":str(e)
            }

        finally:
            return_db_connection(conn)



class Login(Resource):
    def post(self):
        conn=None
        try:
            conn=db_connection()
            cur=conn.cursor()
            data=request.get_json()

            cur.execute(
                """
                SELECT
                    id,
                    name,
                    password,
                    role
                FROM users
                WHERE email=%s
                """,
                (data["email"],)
            )

            res=cur.fetchone()

            if res and res[2]==data["password"]:

                token=create_access_token(
                    identity=str(res[0]),
                    additional_claims={
                        "role":res[3],
                        "name":res[1]
                    }
                )

                return {
                    "status":"success",
                    "access_token":token,
                    "userid":res[0],
                    "role":res[3]
                }

            return {
                "status":"failed",
                "message":"Invalid login"
            }

        except Exception as e:
            print("LOGIN ERROR:",e)
            return {"status":"failed","error":str(e)}

        finally:
            if conn:
                return_db_connection(conn)