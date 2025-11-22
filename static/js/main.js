// Уведомления
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg ${
        type === 'success' ? 'bg-green-500 text-black' : 
        type === 'error' ? 'bg-red-500 text-white' : 'bg-gray-800 text-white'
    }`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// API вызовы
async function apiCall(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showToast('Ошибка соединения', 'error');
    }
}

// Модерация
async function approveJob(jobId) {
    const result = await apiCall(`/api/jobs/${jobId}/approve`, {
        method: 'POST'
    });
    
    if (result.success) {
        showToast('Вакансия одобрена', 'success');
        document.getElementById(`job-${jobId}`).remove();
    }
}

async function rejectJob(jobId) {
    const result = await apiCall(`/api/jobs/${jobId}/reject`, {
        method: 'POST'
    });
    
    if (result.success) {
        showToast('Вакансия отклонена', 'success');
        document.getElementById(`job-${jobId}`).remove();
    }
}