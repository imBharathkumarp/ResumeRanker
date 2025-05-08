describe('ResumeRanker Frontend Tests', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <form id="resumeForm">
                <input type="file" id="resume">
                <button id="submitBtn">
                    <span class="spinner-border spinner-border-sm d-none"></span>
                    Analyze Resume
                </button>
            </form>
            <div id="results" class="d-none"></div>
            <div id="error" class="d-none"></div>
        `;
    });

    test('should show error when no file is selected', () => {
        const form = document.getElementById('resumeForm');
        const error = document.getElementById('error');
        
        form.dispatchEvent(new Event('submit'));
        
        expect(error.classList.contains('d-none')).toBe(false);
        expect(error.textContent).toBe('Please select a file to upload');
    });

    test('should handle API error response', async () => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: false,
                json: () => Promise.resolve({ error: 'Test error' })
            })
        );

        const form = document.getElementById('resumeForm');
        const fileInput = document.getElementById('resume');
        const error = document.getElementById('error');
        
        // Create a mock file
        const file = new File(['test'], 'test.pdf', { type: 'application/pdf' });
        Object.defineProperty(fileInput, 'files', {
            value: [file]
        });

        await form.dispatchEvent(new Event('submit'));
        
        expect(error.classList.contains('d-none')).toBe(false);
        expect(error.textContent).toBe('Test error');
    });

    test('should update UI with successful response', async () => {
        const mockResponse = {
            total_score: 7.5,
            section_scores: {
                length: 2.5,
                skills: 2.0,
                experience: 1.5,
                education: 1.0,
                achievements: 0.5
            }
        };

        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve(mockResponse)
            })
        );

        const form = document.getElementById('resumeForm');
        const fileInput = document.getElementById('resume');
        const results = document.getElementById('results');
        
        // Create a mock file
        const file = new File(['test'], 'test.pdf', { type: 'application/pdf' });
        Object.defineProperty(fileInput, 'files', {
            value: [file]
        });

        await form.dispatchEvent(new Event('submit'));
        
        expect(results.classList.contains('d-none')).toBe(false);
    });
}); 