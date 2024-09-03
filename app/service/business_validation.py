import re
from typing import Dict

def validate_business_number(business_no: str) -> Dict:
    """
    Validate the business number format.
    
    Args:
        business_no (str): The business number to validate.
        
    Returns:
        Dict: A dictionary with validation result.
    """
    # 사업자 등록 번호 형식 검증 (10자리 숫자)
    pattern = re.compile(r'^\d{3}-\d{2}-\d{5}$')

    # 형식에 맞는지 확인
    if pattern.match(business_no):
        # 추가적인 검증 로직이 필요할 경우 여기에 추가
        # 예를 들어, 특정 패턴의 유효성을 추가적으로 검증할 수 있습니다.
        return {"valid": True}
    else:
        return {"valid": False}