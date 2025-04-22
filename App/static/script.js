// Common JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add active class to current nav item
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });

    // Confirm delete actions
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // Add image preview functionality if the image input exists
    const imageInput = document.getElementById('image_url');
    if (imageInput) {
        imageInput.addEventListener('change', previewImage);
    }
});

// Function to add new ingredient fields
function addIngredient() {
    const container = document.getElementById('ingredients-container');
    const newIngredient = document.createElement('div');
    newIngredient.className = 'ingredient-item mb-3';
    newIngredient.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <input type="text" class="form-control" name="ingredient_names[]" 
                       placeholder="Ingredient name" required>
            </div>
            <div class="col-md-4">
                <input type="text" class="form-control" name="ingredient_quantities[]" 
                       placeholder="Quantity" required>
            </div>
            <div class="col-md-2">
                <input type="text" class="form-control" name="ingredient_units[]" 
                       placeholder="Unit" required>
            </div>
        </div>
    `;
    container.appendChild(newIngredient);
}

// Function to preview image before upload
function previewImage(event) {
    const preview = document.getElementById('image-preview');
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function() {
        preview.src = reader.result;
        preview.style.display = 'block';
    }

    if (file) {
        reader.readAsDataURL(file);
    }
} 