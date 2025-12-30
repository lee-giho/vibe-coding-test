-- 짜장면 vs 짬뽕 투표 서비스 초기 데이터
-- 실행 순서: schema.sql 이후 실행됨 (파일명 순서로 실행)

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 초기 투표 주제 생성
INSERT INTO polls (id, title, is_active) VALUES
(1, '짜장면 vs 짬뽕', 1);

-- 투표 선택지 생성
INSERT INTO options (poll_id, label, vote_count) VALUES
(1, '짜장면', 0),
(1, '짬뽕', 0);
