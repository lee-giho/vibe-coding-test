from datetime import datetime
from db import Database

class PollService:
    """투표 관련 비즈니스 로직"""
    
    @staticmethod
    def get_results(poll_id):
        """
        투표 결과 조회
        
        Args:
            poll_id (int): 투표 ID
            
        Returns:
            dict: 결과 데이터 또는 None
        """
        try:
            with Database.get_cursor() as cursor:
                # Poll 존재 확인
                cursor.execute(
                    "SELECT id, title, is_active FROM polls WHERE id = %s",
                    (poll_id,)
                )
                poll = cursor.fetchone()
                
                if not poll:
                    return None
                
                # 옵션별 결과 조회
                cursor.execute(
                    """
                    SELECT id as optionId, label, vote_count as count
                    FROM options
                    WHERE poll_id = %s
                    ORDER BY id
                    """,
                    (poll_id,)
                )
                options = cursor.fetchall()
                
                # 총 투표수 계산
                total_votes = sum(opt['count'] for opt in options)
                
                # 퍼센트 계산
                for opt in options:
                    if total_votes > 0:
                        opt['percent'] = round((opt['count'] / total_votes) * 100, 2)
                    else:
                        opt['percent'] = 0.0
                
                return {
                    'pollId': poll['id'],
                    'title': poll['title'],
                    'totalVotes': total_votes,
                    'options': options,
                    'updatedAt': datetime.now().astimezone().isoformat()
                }
                
        except Exception as e:
            raise e
    
    @staticmethod
    def submit_vote(poll_id, option_id, client_hash=None):
        """
        투표 제출 (트랜잭션)
        
        Args:
            poll_id (int): 투표 ID
            option_id (int): 선택한 옵션 ID
            client_hash (str): 클라이언트 식별 해시 (선택)
            
        Returns:
            dict: 투표 반영 후 최신 결과 또는 None
        """
        connection = None
        cursor = None
        
        try:
            connection = Database.get_connection()
            cursor = connection.cursor()
            
            # 1. Poll 검증
            cursor.execute(
                "SELECT id, is_active FROM polls WHERE id = %s",
                (poll_id,)
            )
            poll = cursor.fetchone()
            
            if not poll:
                return {'error': 'NOT_FOUND', 'message': 'poll not found'}
            
            if not poll['is_active']:
                return {'error': 'POLL_INACTIVE', 'message': 'poll is inactive'}
            
            # 2. Option 검증
            cursor.execute(
                "SELECT id, poll_id FROM options WHERE id = %s AND poll_id = %s",
                (option_id, poll_id)
            )
            option = cursor.fetchone()
            
            if not option:
                return {'error': 'NOT_FOUND', 'message': 'option not found or does not belong to poll'}
            
            # 3. 투표 로그 삽입
            cursor.execute(
                """
                INSERT INTO votes (poll_id, option_id, client_hash)
                VALUES (%s, %s, %s)
                """,
                (poll_id, option_id, client_hash)
            )
            
            # 4. 옵션 카운트 증가 (원자적)
            cursor.execute(
                """
                UPDATE options
                SET vote_count = vote_count + 1
                WHERE id = %s AND poll_id = %s
                """,
                (option_id, poll_id)
            )
            
            if cursor.rowcount == 0:
                raise Exception("Failed to update vote count")
            
            # 트랜잭션 커밋
            connection.commit()
            
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        
        # 5. 최신 결과 반환 (새 연결 사용)
        results = PollService.get_results(poll_id)
        return {
            'pollId': poll_id,
            'optionId': option_id,
            'results': results
        }
