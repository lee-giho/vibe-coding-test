-- 짜장면 vs 짬뽕 투표 서비스 데이터베이스 스키마
-- MySQL 8.0+

-- 문자셋 설정
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- polls 테이블: 투표 주제
CREATE TABLE IF NOT EXISTS polls (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL COMMENT '투표 주제',
    is_active TINYINT(1) NOT NULL DEFAULT 1 COMMENT '활성 여부 (0: 비활성, 1: 활성)',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시각',
    INDEX idx_polls_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='투표 주제 테이블';

-- options 테이블: 투표 선택지
CREATE TABLE IF NOT EXISTS options (
    id INT PRIMARY KEY AUTO_INCREMENT,
    poll_id INT NOT NULL COMMENT '투표 주제 ID',
    label VARCHAR(50) NOT NULL COMMENT '선택지 이름 (예: 짜장면, 짬뽕)',
    vote_count INT NOT NULL DEFAULT 0 COMMENT '득표수 캐시',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시각',
    FOREIGN KEY (poll_id) REFERENCES polls(id) ON DELETE CASCADE,
    UNIQUE KEY uk_poll_label (poll_id, label) COMMENT '동일 poll에 중복 라벨 방지',
    INDEX idx_options_poll (poll_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='투표 선택지 테이블';

-- votes 테이블: 투표 로그
CREATE TABLE IF NOT EXISTS votes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    poll_id INT NOT NULL COMMENT '투표 주제 ID',
    option_id INT NOT NULL COMMENT '선택한 옵션 ID',
    client_hash CHAR(64) NULL COMMENT '클라이언트 식별 해시 (악용 방지용)',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '투표 시각',
    FOREIGN KEY (poll_id) REFERENCES polls(id) ON DELETE CASCADE,
    FOREIGN KEY (option_id) REFERENCES options(id) ON DELETE CASCADE,
    INDEX idx_votes_poll_created (poll_id, created_at),
    INDEX idx_votes_option (option_id),
    INDEX idx_votes_client_hash (client_hash, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='투표 로그 테이블';
