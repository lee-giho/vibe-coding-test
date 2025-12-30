from flask import Flask, request, send_from_directory
from flask_cors import CORS
from db import Database
from services.poll_service import PollService
from utils.responses import make_response, make_error
import logging
import os

# Flask 앱 생성
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 정적 파일 제공 (프론트엔드)
@app.route('/')
def serve_index():
    """메인 페이지 제공"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """정적 파일 제공"""
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# Health Check
@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """헬스체크 엔드포인트"""
    db_ok = Database.check_health()
    
    if db_ok:
        return make_response(
            success=True,
            data={
                'status': 'ok',
                'db': 'ok'
            },
            status=200
        )
    else:
        return make_error(
            status=503,
            code='DB_UNAVAILABLE',
            message='database unavailable'
        )

# 결과 조회
@app.route('/api/v1/results', methods=['GET'])
def get_results():
    """투표 결과 조회"""
    try:
        # Query Parameter에서 pollId 추출
        poll_id = request.args.get('pollId', type=int)
        
        if not poll_id:
            return make_error(
                status=400,
                code='VALIDATION_ERROR',
                message='pollId is required'
            )
        
        # 결과 조회
        results = PollService.get_results(poll_id)
        
        if results is None:
            return make_error(
                status=404,
                code='NOT_FOUND',
                message='poll not found'
            )
        
        return make_response(
            success=True,
            data=results,
            status=200
        )
        
    except Exception as e:
        logger.error(f"Error in get_results: {str(e)}", exc_info=True)
        return make_error(
            status=500,
            code='INTERNAL_ERROR',
            message='unexpected error'
        )

# 투표 제출
@app.route('/api/v1/votes', methods=['POST'])
def submit_vote():
    """투표 제출"""
    try:
        # JSON Body 파싱
        data = request.get_json()
        
        if not data:
            return make_error(
                status=400,
                code='VALIDATION_ERROR',
                message='request body is required'
            )
        
        poll_id = data.get('pollId')
        option_id = data.get('optionId')
        
        # 필수 필드 검증
        if not poll_id:
            return make_error(
                status=400,
                code='VALIDATION_ERROR',
                message='pollId is required',
                details={'field': 'pollId'}
            )
        
        if not option_id:
            return make_error(
                status=400,
                code='VALIDATION_ERROR',
                message='optionId is required',
                details={'field': 'optionId'}
            )
        
        # 타입 검증
        if not isinstance(poll_id, int) or not isinstance(option_id, int):
            return make_error(
                status=400,
                code='VALIDATION_ERROR',
                message='pollId and optionId must be integers'
            )
        
        # 투표 처리
        result = PollService.submit_vote(poll_id, option_id)
        
        # 에러 체크
        if 'error' in result:
            error_code = result['error']
            if error_code == 'NOT_FOUND':
                return make_error(
                    status=404,
                    code=error_code,
                    message=result['message']
                )
            elif error_code == 'POLL_INACTIVE':
                return make_error(
                    status=409,
                    code=error_code,
                    message=result['message']
                )
        
        return make_response(
            success=True,
            data=result,
            status=200
        )
        
    except Exception as e:
        logger.error(f"Error in submit_vote: {str(e)}", exc_info=True)
        return make_error(
            status=500,
            code='INTERNAL_ERROR',
            message='unexpected error'
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
