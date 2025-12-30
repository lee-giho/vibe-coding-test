// 설정
const CONFIG = {
    API_BASE_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:5001/api/v1'
        : '/api/v1',
    POLL_ID: 1,
    POLL_INTERVAL: 3000, // 3초
    TOAST_DURATION: 3000
};

// 옵션 ID 매핑 (서버에서 받아온 후 설정됨)
const optionMap = {
    jjajang: null,
    jjamppong: null
};

// 상태 관리
let state = {
    current: 'loading', // loading, empty, success, error
    isVoting: false,
    pollIntervalId: null,
    lastResults: null
};

// DOM 요소
const elements = {
    loadingState: document.getElementById('loadingState'),
    errorState: document.getElementById('errorState'),
    emptyState: document.getElementById('emptyState'),
    voteSection: document.getElementById('voteSection'),
    resultsSection: document.getElementById('resultsSection'),
    statusBadge: document.getElementById('statusBadge'),
    totalVotes: document.getElementById('totalVotes'),
    resultsList: document.getElementById('resultsList'),
    lastUpdated: document.getElementById('lastUpdated'),
    errorMessage: document.getElementById('errorMessage'),
    toast: document.getElementById('toast'),
    buttons: {
        jjajang: document.getElementById('btn-jjajang'),
        jjamppong: document.getElementById('btn-jjamppong')
    },
    cards: {
        jjajang: document.getElementById('card-jjajang'),
        jjamppong: document.getElementById('card-jjamppong')
    }
};

// 초기화
window.addEventListener('DOMContentLoaded', () => {
    init();
});

async function init() {
    console.log('앱 초기화 시작');
    setState('loading');
    await fetchResults();
    startPolling();
}

// 상태 변경
function setState(newState) {
    state.current = newState;
    
    // 모든 state 숨기기
    elements.loadingState.classList.add('hidden');
    elements.errorState.classList.add('hidden');
    elements.emptyState.classList.add('hidden');
    elements.voteSection.classList.add('hidden');
    elements.resultsSection.classList.add('hidden');
    
    // 상태 배지 업데이트
    elements.statusBadge.classList.remove('offline', 'updating');
    
    // 새 상태 표시
    switch(newState) {
        case 'loading':
            elements.loadingState.classList.remove('hidden');
            break;
        case 'error':
            elements.errorState.classList.remove('hidden');
            elements.statusBadge.classList.add('offline');
            elements.statusBadge.textContent = 'OFFLINE';
            break;
        case 'empty':
            elements.emptyState.classList.remove('hidden');
            elements.voteSection.classList.remove('hidden');
            elements.statusBadge.textContent = 'LIVE';
            break;
        case 'success':
            elements.voteSection.classList.remove('hidden');
            elements.resultsSection.classList.remove('hidden');
            elements.statusBadge.textContent = 'LIVE';
            break;
    }
}

// 결과 조회
async function fetchResults() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/results?pollId=${CONFIG.POLL_ID}`);
        const json = await response.json();
        
        if (!response.ok) {
            throw new Error(json.error?.message || 'Failed to fetch results');
        }
        
        if (json.success && json.data) {
            handleResultsSuccess(json.data);
        } else {
            throw new Error('Invalid response format');
        }
        
    } catch (error) {
        console.error('결과 조회 실패:', error);
        handleResultsError(error.message);
    }
}

// 결과 조회 성공
function handleResultsSuccess(data) {
    state.lastResults = data;
    
    // 옵션 ID 매핑 설정 (최초 1회)
    if (!optionMap.jjajang && data.options && data.options.length >= 2) {
        // 라벨 기반으로 매핑
        data.options.forEach(opt => {
            if (opt.label === '짜장면') {
                optionMap.jjajang = opt.optionId;
            } else if (opt.label === '짬뽕') {
                optionMap.jjamppong = opt.optionId;
            }
        });
        console.log('옵션 ID 매핑:', optionMap);
    }
    
    // 상태 결정
    if (data.totalVotes === 0) {
        setState('empty');
    } else {
        setState('success');
        renderResults(data);
    }
}

// 결과 조회 실패
function handleResultsError(message) {
    setState('error');
    elements.errorMessage.textContent = message || '서버 연결이 불안정합니다.';
}

// 결과 렌더링
function renderResults(data) {
    // 총 투표수
    elements.totalVotes.textContent = data.totalVotes;
    
    // 옵션별 결과
    elements.resultsList.innerHTML = '';
    data.options.forEach(option => {
        const resultItem = createResultItem(option);
        elements.resultsList.appendChild(resultItem);
    });
    
    // 마지막 업데이트 시간
    const updatedTime = new Date(data.updatedAt).toLocaleTimeString('ko-KR');
    elements.lastUpdated.textContent = updatedTime;
}

// 결과 아이템 생성
function createResultItem(option) {
    const div = document.createElement('div');
    div.className = 'result-item';
    div.innerHTML = `
        <div class="result-header">
            <span class="result-label">${option.label}</span>
            <div class="result-stats">
                <span>${option.count}표</span>
                <span>${option.percent}%</span>
            </div>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: ${option.percent}%">
                ${option.percent > 20 ? option.percent + '%' : ''}
            </div>
        </div>
    `;
    return div;
}

// 투표 제출
async function handleVote(optionKey) {
    if (state.isVoting) return;
    
    const optionId = optionMap[optionKey];
    if (!optionId) {
        showToast('옵션 정보를 불러오는 중입니다. 잠시 후 다시 시도해주세요.', 'error');
        return;
    }
    
    // 투표 중 상태
    state.isVoting = true;
    setButtonLoading(optionKey, true);
    elements.statusBadge.classList.add('updating');
    elements.statusBadge.textContent = 'UPDATING...';
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/votes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                pollId: CONFIG.POLL_ID,
                optionId: optionId
            })
        });
        
        const json = await response.json();
        
        if (!response.ok) {
            const errorMsg = json.error?.message || '투표에 실패했습니다.';
            throw new Error(errorMsg);
        }
        
        if (json.success && json.data && json.data.results) {
            // 성공 - 결과 즉시 반영
            handleResultsSuccess(json.data.results);
            showToast('투표가 반영되었습니다! 🎉', 'success');
            
            // 카드 애니메이션
            elements.cards[optionKey].classList.add('voted');
            setTimeout(() => {
                elements.cards[optionKey].classList.remove('voted');
            }, 500);
        } else {
            throw new Error('Invalid response format');
        }
        
    } catch (error) {
        console.error('투표 실패:', error);
        showToast(error.message, 'error');
    } finally {
        state.isVoting = false;
        setButtonLoading(optionKey, false);
        elements.statusBadge.classList.remove('updating');
        elements.statusBadge.textContent = 'LIVE';
    }
}

// 버튼 로딩 상태
function setButtonLoading(optionKey, isLoading) {
    const btn = elements.buttons[optionKey];
    const textSpan = btn.querySelector('.btn-text');
    const spinner = btn.querySelector('.btn-spinner');
    
    // 모든 버튼 비활성화/활성화
    Object.values(elements.buttons).forEach(b => {
        b.disabled = isLoading;
    });
    
    if (isLoading) {
        textSpan.classList.add('hidden');
        spinner.classList.remove('hidden');
    } else {
        textSpan.classList.remove('hidden');
        spinner.classList.add('hidden');
    }
}

// 토스트 메시지
function showToast(message, type = 'info') {
    elements.toast.textContent = message;
    elements.toast.className = `toast ${type}`;
    elements.toast.classList.remove('hidden');
    
    setTimeout(() => {
        elements.toast.classList.add('hidden');
    }, CONFIG.TOAST_DURATION);
}

// 폴링 시작
function startPolling() {
    // 기존 폴링 중지
    if (state.pollIntervalId) {
        clearInterval(state.pollIntervalId);
    }
    
    // 새 폴링 시작
    state.pollIntervalId = setInterval(() => {
        if (state.current !== 'error' && !state.isVoting) {
            fetchResults();
        }
    }, CONFIG.POLL_INTERVAL);
    
    console.log('폴링 시작:', CONFIG.POLL_INTERVAL + 'ms');
}

// 폴링 중지
function stopPolling() {
    if (state.pollIntervalId) {
        clearInterval(state.pollIntervalId);
        state.pollIntervalId = null;
        console.log('폴링 중지');
    }
}

// 재시도
function retryLoad() {
    console.log('재시도');
    setState('loading');
    fetchResults();
}

// 탭 비활성화 시 폴링 최적화 (선택)
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        stopPolling();
    } else {
        fetchResults();
        startPolling();
    }
});
