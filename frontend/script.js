document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('resumeForm');
    const submitBtn = document.getElementById('submitBtn');
    const spinner = submitBtn.querySelector('.spinner-border');
    const results = document.getElementById('results');
    const error = document.getElementById('error');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset UI
        results.classList.add('d-none');
        error.classList.add('d-none');
        
        // Show loading state
        submitBtn.disabled = true;
        spinner.classList.remove('d-none');
        
        const formData = new FormData();
        const fileInput = document.getElementById('resume');
        
        if (!fileInput.files[0]) {
            showError('Please select a file to upload');
            return;
        }
        
        formData.append('resume', fileInput.files[0]);

        try {
            const response = await fetch('https://resumeranker-89kg.onrender.com/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'An error occurred while processing your resume');
            }

            // Update UI with results
            updateResults(result);
            results.classList.remove('d-none');
        } catch (err) {
            showError(err.message);
        } finally {
            // Reset loading state
            submitBtn.disabled = false;
            spinner.classList.add('d-none');
        }
    });

    function updateResults(result) {
        // Update total score
        document.getElementById('totalScore').textContent = result.total_score;
        
        // Update section scores
        const sections = {
            length: { element: 'lengthScore', max: 3 },
            skills: { element: 'skillsScore', max: 2 },
            experience: { element: 'experienceScore', max: 2 },
            education: { element: 'educationScore', max: 1.5 },
            achievements: { element: 'achievementsScore', max: 1.5 }
        };

        for (const [section, info] of Object.entries(sections)) {
            const score = result.section_scores[section];
            const element = document.getElementById(info.element);
            const percentage = (score / info.max) * 100;
            
            element.style.width = `${percentage}%`;
            element.textContent = `${section.charAt(0).toUpperCase() + section.slice(1)} (${score}/${info.max})`;
        }
    }

    function showError(message) {
        error.textContent = message;
        error.classList.remove('d-none');
    }
});
