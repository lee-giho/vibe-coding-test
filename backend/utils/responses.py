from flask import jsonify

def make_response(success=True, data=None, error=None, status=200):
    """
    표준 API 응답 생성
    
    Args:
        success (bool): 성공 여부
        data: 응답 데이터
        error (dict): 에러 정보 {'code': str, 'message': str, 'details': any}
        status (int): HTTP 상태 코드
    """
    return jsonify({
        'success': success,
        'data': data,
        'error': error
    }), status

def make_error(status, code, message, details=None):
    """
    에러 응답 생성
    
    Args:
        status (int): HTTP 상태 코드
        code (str): 에러 코드
        message (str): 에러 메시지
        details: 추가 상세 정보
    """
    return make_response(
        success=False,
        data=None,
        error={
            'code': code,
            'message': message,
            'details': details
        },
        status=status
    )
