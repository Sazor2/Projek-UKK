document.addEventListener('DOMContentLoaded', function() {
    // Handle form submission
    const admissionForm = document.querySelector('#admission-form');
    if (admissionForm) {
        admissionForm.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Submitting...';
        });
    }
    
    // Handle status update buttons
    const statusForms = document.querySelectorAll('.status-update-form');
    statusForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const button = this.querySelector('button');
            button.disabled = true;
        });
    });
    
    // Handle flash messages and temporary notices auto-hide
    const tempElements = document.querySelectorAll('.temp-notice');
    tempElements.forEach(element => {
        setTimeout(() => {
            element.style.opacity = '0';
            setTimeout(() => {
                if (element.parentNode) {
                    element.parentNode.removeChild(element);
                }
            }, 300);
        }, 6000); // Changed to 6 seconds
    });
    
    // Theme switcher functionality
    const themeToggle = document.getElementById('theme-toggle');
    
    if (themeToggle) {
        // Function to set theme
        function setTheme(isDark) {
            const theme = isDark ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            themeToggle.checked = isDark;
            
            // Dispatch event untuk komponen yang perlu update
            document.dispatchEvent(new CustomEvent('themeChanged', {
                detail: { theme: theme }
            }));
        }

        // Initialize theme from localStorage
        const savedTheme = localStorage.getItem('theme') || 'light';
        setTheme(savedTheme === 'dark');

        // Listen for theme toggle changes
        themeToggle.addEventListener('change', (e) => {
            setTheme(e.target.checked);
        });
    }

    // Initialize datepicker
    if ($.fn.datepicker) {
        $('.datepicker').datepicker({
            format: 'yyyy-mm-dd',
            language: 'id',
            autoclose: true,
            todayHighlight: true,
            endDate: new Date(),
            startView: 2,
            templates: {
                leftArrow: '<i class="fas fa-chevron-left"></i>',
                rightArrow: '<i class="fas fa-chevron-right"></i>'
            },
            orientation: "bottom auto",
            clearBtn: false,
            assumeNearbyYear: true,
            maxViewMode: 2,
            startDate: "-25y",
            endDate: "-10y"
        }).on('keydown', function(e) {
            e.preventDefault();
            return false;
        });

        // Make the calendar icon clickable
        $('.input-group-text').on('click', function() {
            $(this).prev('.datepicker').datepicker('show');
        });
    }

    // Filter functionality for admin table
    const filterButtons = document.querySelectorAll('.filter-options .btn');
    const applicationRows = document.querySelectorAll('.application-row');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.getAttribute('data-filter');
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Filter rows
            applicationRows.forEach(row => {
                const status = row.getAttribute('data-status');
                if (filter === 'all' || status === filter) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });
});