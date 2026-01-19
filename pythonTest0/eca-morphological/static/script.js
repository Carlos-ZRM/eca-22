console.log('🔍 script.js loaded');

// Check if backendData is available
console.log('Checking backendData:', typeof backendData);
if (typeof backendData !== 'undefined') {
    console.log('✓ backendData found:', backendData);
} else {
    console.error('❌ backendData not found - Jinja2 template not rendered?');
}

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🟢 DOMContentLoaded event fired');
    
    // Safely get all elements with null checks
    const simForm = document.getElementById('param-form');
    const initMethodSelect = document.getElementById('init-method-select');
    const densityContainer = document.getElementById('density-container');
    const densityInput = document.getElementById('density-input');
    const canvas = document.getElementById('image-canvas');
    const saveBtn = document.getElementById('save-image-btn');
    const infoPopup = document.getElementById('info-popup');
    const themeToggle = document.getElementById('theme-toggle');
    
    console.log('Elements found:');
    console.log('  param-form:', simForm ? '✓' : '❌ NOT FOUND');
    console.log('  init-method-select:', initMethodSelect ? '✓' : '❌ NOT FOUND');
    console.log('  image-canvas:', canvas ? '✓' : '❌ NOT FOUND');
    console.log('  save-image-btn:', saveBtn ? '✓' : '❌ NOT FOUND');
    
    // Get canvas context only if canvas exists
    let ctx = null;
    if (canvas) {
        ctx = canvas.getContext('2d');
        console.log('✓ Canvas context obtained');
    } else {
        console.error('❌ Canvas element not found! Cannot get 2D context');
    }
    
    // === POPULATE DROPDOWNS ===
    function populateSelect(selectId, options) {
        const select = document.getElementById(selectId);
        if (!select) {
            console.error(`Element not found: ${selectId}`);
            return;
        }
        if (!options || !Array.isArray(options)) {
            console.warn(`No valid options for ${selectId}`);
            return;
        }
        
        options.forEach(optionValue => {
            const option = document.createElement('option');
            option.value = optionValue;
            option.textContent = optionValue;
            if (selectId === 'init-method-select' && optionValue === 'random') {
                option.selected = true;
            }
            select.appendChild(option);
        });
        console.log(`✓ Populated ${selectId} with ${options.length} options`);
    }
    
    // Populate dropdowns if backendData exists
    if (typeof backendData !== 'undefined') {
        console.log('Populating dropdowns from backendData...');
        populateSelect('rule-select', backendData.rules);
        populateSelect('init-method-select', backendData.init_methods);
        populateSelect('print-method-select', backendData.print_methods);
    } else {
        console.error('Cannot populate dropdowns - backendData not defined');
    }
    
    // === DENSITY FIELD TOGGLE ===
    function toggleDensity() {
        if (initMethodSelect && densityContainer) {
            if (initMethodSelect.value === 'random') {
                densityContainer.style.display = 'block';
            } else {
                densityContainer.style.display = 'none';
            }
        }
    }
    
    if (initMethodSelect) {
        initMethodSelect.addEventListener('change', toggleDensity);
        toggleDensity();
    }
    
    if (densityInput) {
        densityInput.addEventListener('change', function() {
            let value = this.value.trim();
            let numValue = parseFloat(value);
            if (value === '' || isNaN(numValue)) {
                this.value = '0.5';
            } else {
                numValue = Math.max(0, Math.min(1, numValue));
                this.value = numValue;
            }
        });
        
        densityInput.addEventListener('blur', function() {
            let value = this.value.trim();
            let numValue = parseFloat(value);
            if (value === '' || isNaN(numValue)) {
                this.value = '0.5';
            } else {
                numValue = Math.max(0, Math.min(1, numValue));
                this.value = numValue;
            }
        });
    }
    
    // === SAVE IMAGE BUTTON ===
    if (saveBtn && canvas) {
        saveBtn.addEventListener('click', function() {
            const filename = 'simulacion.png';
            const link = document.createElement('a');
            link.download = filename;
            link.href = canvas.toDataURL('image/png');
            link.click();
            alert(`Imagen guardada como: ${filename}\nRuta: Descargas o carpeta configurada en tu navegador.`);
        });
    }
    
    // === FORM SUBMISSION ===
    if (simForm && canvas && ctx) {
        simForm.addEventListener('submit', (event) => {
            event.preventDefault();
            console.log('📤 Form submitted');
            
            const formData = new FormData(simForm);
            const payload = Object.fromEntries(formData.entries());
            console.log('Sending payload:', payload);
            
            fetch('/generate_image', {
                method: 'POST',
                body: JSON.stringify(payload),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('✓ Image data received from backend');
                if (saveBtn) saveBtn.style.display = 'inline-block';
                
                const img = new window.Image();
                img.onload = function() {
                    console.log('✓ Image loaded, drawing to canvas');
                    canvas.width = img.width;
                    canvas.height = img.height;
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(img, 0, 0);
                };
                img.onerror = function() {
                    console.error('Failed to load image data');
                };
                img.src = data.image_data;
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error generando imagen: ' + error);
            });
        });
    } else {
        console.error('Cannot attach form submission listener - missing elements');
        if (!simForm) console.error('  Missing: param-form');
        if (!canvas) console.error('  Missing: image-canvas');
        if (!ctx) console.error('  Missing: canvas 2D context');
    }
    
    // === DARK MODE ===
    if (themeToggle) {
        themeToggle.addEventListener('change', () => {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
        
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark-mode');
            themeToggle.checked = true;
        }
    }
    
    // === INFO POPUPS ===
    if (infoPopup) {
        document.addEventListener('mouseover', (event) => {
            if (event.target.classList.contains('info-icon')) {
                const infoText = event.target.dataset.info;
                const iconRect = event.target.getBoundingClientRect();
                
                infoPopup.textContent = infoText;
                infoPopup.style.display = 'block';
                
                let top = iconRect.top - infoPopup.offsetHeight - 5;
                let left = iconRect.left + (iconRect.width / 2) - (infoPopup.offsetWidth / 2);
                
                if (top < 0) { top = iconRect.bottom + 5; }
                if (left < 0) { left = 5; }
                
                infoPopup.style.top = `${top}px`;
                infoPopup.style.left = `${left}px`;
            }
        });
        
        document.addEventListener('mouseout', (event) => {
            if (event.target.classList.contains('info-icon')) {
                infoPopup.style.display = 'none';
            }
        });
    }
    
    console.log('✅ App initialization complete');
});

// === TAB MANAGEMENT ===
function openTab(evt, tabName) {
    console.log('Opening tab:', tabName);
    const tabcontents = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabcontents.length; i++) {
        tabcontents[i].style.display = "none";
    }
    const tablinks = document.getElementsByClassName("tab-link");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    const tabElement = document.getElementById(tabName);
    if (tabElement) {
        tabElement.style.display = "flex";
    }
    evt.currentTarget.className += " active";
}

console.log('✅ script.js fully loaded');
