const fileInput = document.getElementById('resumes');
const fileList = document.getElementById('file-list');
const form = document.getElementById('screening-form');
const submitBtn = document.getElementById('submit-btn');
const btnText = document.querySelector('.btn-text');
const loader = document.querySelector('.loader');
const resultsSection = document.getElementById('results-section');
const resultsBody = document.getElementById('results-body');

fileInput.addEventListener('change', (e) => {
    fileList.innerHTML = '';
    Array.from(e.target.files).forEach(file => {
        const span = document.createElement('span');
        span.className = 'file-tag';
        span.innerHTML = `
            <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            ${file.name}
        `;
        fileList.appendChild(span);
    });
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(form);
    
    if (!formData.get('job_description').trim() || formData.getAll('files').length === 0 || formData.get('files').size === 0) {
        alert("Please provide both a job description and at least one resume file.");
        return;
    }

    // UI Loading state
    submitBtn.disabled = true;
    btnText.textContent = 'Processing...';
    loader.classList.remove('hidden');
    submitBtn.querySelector('svg').classList.add('hidden');
    resultsSection.classList.add('hidden');

    try {
        const response = await fetch('http://localhost:8000/api/screen', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server responded with status ${response.status}`);
        }

        const data = await response.json();
        displayResults(data.results);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during screening. Please ensure the backend is running and try again.');
    } finally {
        // Reset UI
        submitBtn.disabled = false;
        btnText.textContent = 'Screen Resumes';
        loader.classList.add('hidden');
        submitBtn.querySelector('svg').classList.remove('hidden');
    }
});

function displayResults(results) {
    resultsBody.innerHTML = '';
    
    if (!results || results.length === 0) {
        resultsBody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 3rem; color: #64748b;">No results found</td></tr>';
    } else {
        results.forEach(result => {
            let rankClass = result.rank <= 3 ? `rank-${result.rank}` : '';
            let scoreClass = 'score-low';
            if (result.score >= 70) scoreClass = 'score-high';
            else if (result.score >= 40) scoreClass = 'score-medium';

            const row = document.createElement('tr');
            row.innerHTML = `
                <td><span class="rank-badge ${rankClass}">${result.rank}</span></td>
                <td class="candidate-name">${result.candidate_name}</td>
                <td><span class="score-badge ${scoreClass}">${result.score.toFixed(2)}%</span></td>
                <td style="color: #64748b; font-size: 0.9rem;">${result.filename}</td>
            `;
            resultsBody.appendChild(row);
        });
    }

    resultsSection.classList.remove('hidden');
    
    // Scroll to results smoothly
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}
