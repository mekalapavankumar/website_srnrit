const testimonials = document.querySelectorAll('.testimonial');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');
let currentIndex = 0; // Start from the first testimonial (Isha, index 0)

// to show the current testimo and handle buttons visibility
function showTestimonial(index) {
    testimonials.forEach((testimonial, i) => {
        testimonial.classList.remove('active');
        if (i === index) {
            testimonial.classList.add('active');
        }
    });

    // Hide 'Previous' button on the first slide (Isha)
    if (currentIndex === 0) {
        prevBtn.style.display = 'none';
    } else {
        prevBtn.style.display = 'block';
    }

    // Hide 'Next' button on the last slide (Sam)
    if (currentIndex === testimonials.length - 1) {
        nextBtn.style.display = 'none';
    } else {
        nextBtn.style.display = 'block';
    }
}

// Show the next testimonial (moves forward)
nextBtn.addEventListener('click', () => {
    if (currentIndex < testimonials.length - 1) {
        currentIndex++;
        showTestimonial(currentIndex);
    }
});

// Show the previous testimonial (moves backward)
prevBtn.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
        showTestimonial(currentIndex);
    }
});

// Initialize by showing the first testimonial (Isha)
showTestimonial(currentIndex);
