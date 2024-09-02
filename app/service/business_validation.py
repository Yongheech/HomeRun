# app/services/business_validation.py

import httpx
from typing import Dict

SERVICE_KEY = '	9GRdBCxTZtysQpCaJ40ER4FDMLutMxguPCAESTkBW9JTp%2FG3z4Rqd192CzdAFeVauOSyKsBVxXb9PGFBDy5xbw%3D%3D'
API_URL = 'https://api.odcloud.kr/api/nts-businessman/v1/status'

async def validate_business_number(business_no: str) -> Dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}?serviceKey={SERVICE_KEY}",
            json={"b_no": [business_no]},
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )


        response.raise_for_status()
        result = response.json()
        return result
