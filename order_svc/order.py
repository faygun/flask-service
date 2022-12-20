import requests
from utility import config
from auth import token_util
from flask_sqlalchemy import SQLAlchemy

def getOrders(db:SQLAlchemy, filter):
    accessTokenEntity = token_util.getToken(db)
    query = ""

    if filter:
        if "orderNumber" in filter and filter["orderNumber"]:
            query += f"order_number={filter['orderNumber']}&"
        if "orderStatus" in filter and filter["orderStatus"]:
            query += f"order_status={filter['orderStatus']}&"
        if "orderFrom" in filter and filter["orderFrom"]:
            query += f"created_after={filter['orderFrom']}T00:00:00Z&"
        if "orderEnd" in filter and filter["orderEnd"]:
            query += f"created_before={filter['orderEnd']}T00:00:00Z&"
        if "brand" in filter and filter["brand"]:
            query += f"merchant_id={filter['brand']}&"
        if "pageNumber" in filter:
            query += f"page[number]={filter['pageNumber']}&"
        if "pageSize" in filter and filter["pageSize"]:
            query += f"page[size]={filter['pageSize']}&"

        
        query = query.rstrip("&")

    if accessTokenEntity:
        orderHeader = {
            "Authorization": f"Bearer {accessTokenEntity.accessToken}"
        }
    
    else:
        bearerToken = refreshToken(db)
        print("took refresh token...")
        if not bearerToken:
            return "missing credential", 401
        
        orderHeader = {
            "Authorization": f"Bearer {bearerToken}"
        }
        
    print(f"{config.BASE_URI}/merchants/{config.MERCHANT_ID}{config.ORDER_URI}{'?' + query if query != '' else ''}")

    response = requests.get(f"{config.BASE_URI}/merchants/{config.MERCHANT_ID}{config.ORDER_URI}{'?' + query if query != '' else ''}", headers=orderHeader)

    orderData = response.json()
    if "status" in orderData and orderData["status"] == 401:
        bearerToken = refreshToken(db, accessTokenEntity)

        if not bearerToken:
            return "missing credential", 401

        orderHeader = {
            "Authorization": f"Bearer {bearerToken}"
        }

        response = requests.get(f"{config.BASE_URI}/merchants/{config.MERCHANT_ID}{config.ORDER_URI}", headers=orderHeader)

        orderData = response.json()

    return orderData


def refreshToken(db, existsToken = None):
    accessTokenEntity = token_util.generateToken(db, existsToken)
    if accessTokenEntity:
        return accessTokenEntity.accessToken
    else:
        return ""



    

    
