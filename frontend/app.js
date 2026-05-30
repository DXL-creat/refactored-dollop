// API基础URL
const API_BASE_URL = 'http://localhost:5000/api';

// DOM元素缓存
const elements = {
    climateSelect: document.getElementById('climate'),
    skinTypeSelect: document.getElementById('skin_type'),
    questionInput: document.getElementById('question'),
    submitBtn: document.getElementById('submit-btn'),
    resetBtn: document.getElementById('reset-btn'),
    loading: document.getElementById('loading'),
    errorMessage: document.getElementById('error-message'),
    result: document.getElementById('result'),
    answerContent: document.getElementById('answer-content'),
    resultClimate: document.getElementById('result-climate'),
    resultSkin: document.getElementById('result-skin')
};

/**
 * 提交调研问卷
 */
async function submitResearch() {
    // 获取表单数据
    const climate = elements.climateSelect.value;
    const skinType = elements.skinTypeSelect.value;
    const question = elements.questionInput.value.trim();
    
    // 验证输入
    if (!climate) {
        showError('请选择气候条件');
        return;
    }
    
    if (!skinType) {
        showError('请选择肤质类型');
        return;
    }
    
    if (!question) {
        showError('请输入调研问题');
        return;
    }
    
    // 显示加载状态
    showLoading(true);
    hideError();
    hideResult();
    
    try {
        // 调用API
        const response = await fetch(`${API_BASE_URL}/research`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                climate: climate,
                skin_type: skinType
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '请求失败');
        }
        
        const data = await response.json();
        
        // 显示结果
        displayResult(data);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || '获取回答时出错，请确保后端服务已启动');
    } finally {
        showLoading(false);
    }
}

/**
 * 显示结果
 */
function displayResult(data) {
    elements.answerContent.textContent = data.answer;
    elements.resultClimate.textContent = `🌤️ 气候: ${data.climate}`;
    elements.resultSkin.textContent = `🧴 肤质: ${data.skin_type}`;
    
    showResult(true);
}

/**
 * 复制回答
 */
function copyAnswer() {
    const text = elements.answerContent.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        // 显示复制成功提示
        const copyBtn = document.querySelector('.copy-btn');
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✅ 已复制';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('复制失败:', err);
        showError('复制失败');
    });
}

/**
 * 重置表单
 */
function resetForm() {
    elements.climateSelect.value = '';
    elements.skinTypeSelect.value = '';
    elements.questionInput.value = '';
    hideResult();
    hideError();
    elements.questionInput.focus();
}

/**
 * 显示加载状态
 */
function showLoading(show) {
    if (show) {
        elements.loading.classList.remove('hidden');
        elements.submitBtn.disabled = true;
        elements.resetBtn.disabled = true;
    } else {
        elements.loading.classList.add('hidden');
        elements.submitBtn.disabled = false;
        elements.resetBtn.disabled = false;
    }
}

/**
 * 显示错误消息
 */
function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorMessage.classList.remove('hidden');
}

/**
 * 隐藏错误消息
 */
function hideError() {
    elements.errorMessage.classList.add('hidden');
}

/**
 * 显示结果
 */
function showResult(show) {
    if (show) {
        elements.result.classList.remove('hidden');
        // 滚动到结果位置
        setTimeout(() => {
            elements.result.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    }
}

/**
 * 隐藏结果
 */
function hideResult() {
    elements.result.classList.add('hidden');
}

/**
 * 初始化页面
 */
function initializePage() {
    // 设置回车键提交
    elements.questionInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            submitResearch();
        }
    });
    
    // 设置焦点
    elements.questionInput.focus();
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializePage);
} else {
    initializePage();
}
