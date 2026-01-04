// Common Navigation
const BACKEND_BASE_URL = "http://localhost:8000";
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-menu a');
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || href === '#') {
            link.style.fontWeight = '700';
            link.style.opacity = '1';
        }
    });
}

// Mobile Menu Toggle
function toggleMobileMenu() {
    const menu = document.querySelector('.nav-menu');
    menu.style.display = menu.style.display === 'flex' ? 'none' : 'flex';
}

// Dashboard Stats Animation
function animateStats() {
    const stats = document.querySelectorAll('.stat-number');
    stats.forEach(stat => {
        const target = parseFloat(stat.getAttribute('data-target'));
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            stat.textContent = current.toFixed(current > 10 ? 0 : 1);
            if (current > 10) stat.textContent += '%';
        }, 20);
    });
}

// File Upload Handler
function initUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    const analyzeBtn = document.getElementById('analyzeBtn');

    if (!uploadArea || !fileInput) return;

    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    function handleFiles(files) {
        fileList.innerHTML = '';
        Array.from(files).forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <span><i class="fas fa-file"></i> ${file.name} (${(file.size/1024/1024).toFixed(2)} MB)</span>
                <button onclick="this.parentElement.remove(); updateAnalyzeBtn();" 
                        style="background: #ef4444; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; cursor: pointer;">
                    Remove
                </button>
            `;
            fileList.appendChild(fileItem);
        });
        updateAnalyzeBtn();
    }

    function updateAnalyzeBtn() {
        analyzeBtn.disabled = fileList.children.length === 0;
    }

    analyzeBtn.addEventListener('click', async () => {
    const files = fileInput.files;

    if (!files.length) {
        alert("Please upload a file first");
        return;
    }

    const file = files[0]; // backend expects ONE file
    const formData = new FormData();
    formData.append("file", file);

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";

    try {
        const response = await fetch(
            `${BACKEND_BASE_URL}/assignments/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error("Upload failed");
        }

        const result = await response.json();

        // ✅ Store result for results page
        sessionStorage.setItem(
            "analysisResult",
            JSON.stringify(result)
        );

        // Redirect after successful backend call
        window.location.href = "results.html";

    } catch (error) {
        console.error(error);
        alert("Error analyzing assignment");
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyze Assignment";
    }
});

}

// Form Handlers
function initForms() {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
        });
    }

    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            setTimeout(() => {
                alert('Account created successfully!');
                window.location.href = 'dashboard.html';
            }, 1000);
        });
    }
}

// Page-specific Initialization
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initForms();
    initUpload();
    
    // Initialize stats animation for dashboard
    if (window.location.pathname.includes('dashboard')) {
        setTimeout(animateStats, 500);
    }
    
    // Animate elements on scroll
    window.addEventListener('scroll', () => {
        document.querySelectorAll('.animate').forEach((el, index) => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                el.style.opacity = '1';
            }
        });
    });
});
