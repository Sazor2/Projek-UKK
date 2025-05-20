document.addEventListener('DOMContentLoaded', function() {
    // Handle form submission
    const admissionForm = document.querySelector('#admission-form');
    if (admissionForm) {
        admissionForm.addEventListener('submit', function(e) {
            const phone = document.getElementById('phone');
            const school = document.getElementById('previous_school');
            let isValid = true;

            // Validate phone
            if (!phone.value.trim()) {
                e.preventDefault();
                phone.classList.add('is-invalid');
                phone.nextElementSibling.textContent = 'Nomor telepon wajib diisi';
                isValid = false;
            } else if (!/^[0-9]{10,13}$/.test(phone.value.trim())) {
                e.preventDefault();
                phone.classList.add('is-invalid');
                phone.nextElementSibling.textContent = 'Nomor telepon harus 10-13 digit angka';
                isValid = false;
            } else {
                phone.classList.remove('is-invalid');
                phone.classList.add('is-valid');
            }

            // Validate school
            if (!school.value.trim()) {
                e.preventDefault();
                school.classList.add('is-invalid');
                school.nextElementSibling.textContent = 'Asal sekolah wajib diisi';
                isValid = false;
            } else if (school.value.trim().length < 3) {
                e.preventDefault();
                school.classList.add('is-invalid');
                school.nextElementSibling.textContent = 'Nama sekolah minimal 3 karakter';
                isValid = false;
            } else {
                school.classList.remove('is-invalid');
                school.classList.add('is-valid');
            }

            // If form is valid, show loading state
            if (isValid) {
                const submitButton = this.querySelector('button[type="submit"]');
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Mengirim...';
            }
        });

        // Real-time validation as user types
        const validateInput = (input, validationFn) => {
            input.addEventListener('input', function() {
                const result = validationFn(this.value.trim());
                if (result.isValid) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                    this.nextElementSibling.textContent = result.message;
                }
            });
        };

        // Phone validation
        validateInput(document.getElementById('phone'), (value) => {
            if (!value) return { isValid: false, message: 'Nomor telepon wajib diisi' };
            if (!/^[0-9]{10,13}$/.test(value)) return { isValid: false, message: 'Nomor telepon harus 10-13 digit angka' };
            return { isValid: true };
        });

        // School validation
        validateInput(document.getElementById('previous_school'), (value) => {
            if (!value) return { isValid: false, message: 'Asal sekolah wajib diisi' };
            if (value.length < 3) return { isValid: false, message: 'Nama sekolah minimal 3 karakter' };
            return { isValid: true };
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

    // Initialize datepicker with theme support
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
        });

        // Update datepicker theme when theme changes
        document.addEventListener('themeChanged', function(e) {
            $('.datepicker-dropdown').remove(); // Remove any open datepickers
            $('.datepicker').datepicker('update'); // Refresh datepickers
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
    
    // Validasi ukuran dan tipe file
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            const maxSize = 2 * 1024 * 1024; // 2MB
            
            if (file) {
                if (file.size > maxSize) {
                    alert('Ukuran file terlalu besar. Maksimum 2MB');
                    this.value = '';
                    return;
                }
                
                // Check file type based on input name
                if (this.name === 'foto_siswa') {
                    // Only images for foto_siswa
                    if (!['image/jpeg', 'image/png'].includes(file.type)) {
                        alert('Foto siswa harus berformat JPG atau PNG');
                        this.value = '';
                        return;
                    }
                } else {
                    // Allow PDF and images for other documents
                    const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
                    if (!allowedTypes.includes(file.type)) {
                        alert('File harus berformat PDF, JPG, atau PNG');
                        this.value = '';
                        return;
                    }
                }
            }
        });
    });
    
    // DataTables initialization for applications table
    const applicationsTable = document.getElementById('applicationsTable');
    if (applicationsTable) {
        let table = $(applicationsTable).DataTable({
            responsive: true,
            language: {
                url: '//cdn.datatables.net/plug-ins/1.11.5/i18n/id.json'
            },
            order: [[4, 'desc']], // Sort by date desc
            columnDefs: [
                { orderable: false, targets: [7] }, // Disable sorting for action column
                { 
                    targets: [5, 6], // Status and Payment columns
                    orderable: true,
                    render: function(data, type, row) {
                        if (type === 'sort') {
                            return data.textContent;
                        }
                        return data;
                    }
                }
            ],
            dom: '<"d-flex justify-content-between align-items-center mb-3"<"d-flex align-items-center"l><"d-flex"f>>rtip',
            lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "Semua"]],
        });

        // Handle filter buttons
        $('.filter-options .btn').on('click', function() {
            const filter = $(this).data('filter');
            if (filter === 'all') {
                table.column(5).search('').draw();
            } else {
                table.column(5).search(filter).draw();
            }
            
            // Update active button state
            $('.filter-options .btn').removeClass('active');
            $(this).addClass('active');
        });
    }
});

// Form Steps Navigation
function nextStep() {
    document.getElementById('step1').classList.remove('active');
    document.getElementById('step2').classList.add('active');
    document.getElementById('section1').classList.add('d-none');
    document.getElementById('section2').classList.remove('d-none');
    
    // Smooth scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function prevStep() {
    document.getElementById('step2').classList.remove('active');
    document.getElementById('step1').classList.add('active');
    document.getElementById('section2').classList.add('d-none');
    document.getElementById('section1').classList.remove('d-none');
    
    // Smooth scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Form Validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('admission-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Mohon lengkapi semua field yang wajib diisi');
                return false;
            }

            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Mengirim...';
        });
    }
});

// Add to your existing script.js
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-item');
    const table = $('#applicationsTable').DataTable();

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.dataset.filter;
            
            // Update active state
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Apply filter
            if (filter === 'all') {
                table.column(5).search('').draw();
            } else {
                table.column(5).search(filter).draw();
            }
        });
    });
});