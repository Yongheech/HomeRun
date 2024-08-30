async function checkBusinessStatus(businessNo) {
    try {
        const response = await fetch('/user/check_business_no', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ business_no: businessNo })
        });

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('사업자 번호 조회 오류:', error);
        return null;
    }
}