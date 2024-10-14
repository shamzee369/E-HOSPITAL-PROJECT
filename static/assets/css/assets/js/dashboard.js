// Ensure the DOM is fully loaded before running scripts
document.addEventListener("DOMContentLoaded", function () {
    // Smooth scrolling for internal links
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    scrollLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            target.scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Dropdown menu toggle
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', function () {
            this.classList.toggle('active');
            const dropdownMenu = this.nextElementSibling;
            dropdownMenu.classList.toggle('show');
        });
    });

    // Close dropdowns when clicking outside
    window.addEventListener('click', function (e) {
        if (!e.target.matches('.dropdown-toggle')) {
            dropdowns.forEach(dropdown => {
                const dropdownMenu = dropdown.nextElementSibling;
                dropdown.classList.remove('active');
                dropdownMenu.classList.remove('show');
            });
        }
    });

    // Initialize charts using Chart.js
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            datasets: [{
                label: 'Sales',
                data: [12, 19, 3, 5, 2, 3, 7],
                backgroundColor: 'rgba(74, 144, 226, 0.5)',
                borderColor: 'rgba(74, 144, 226, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeOutBounce'
            }
        }
    });

    // Example of showing a toast notification
    function showToast(message) {
        const toastContainer = document.createElement('div');
        toastContainer.className = 'toast';
        toastContainer.innerText = message;
        document.body.appendChild(toastContainer);

        // Remove the toast after 3 seconds
        setTimeout(() => {
            toastContainer.classList.add('fade');
            setTimeout(() => {
                document.body.removeChild(toastContainer);
            }, 300);
        }, 3000);
    }

    // Call showToast as an example
    showToast('Welcome to the Dashboard!');

    // Example of modal functionality
    const modal = document.getElementById('myModal');
    const openModalBtn = document.getElementById('openModal');
    const closeModalBtn = document.getElementsByClassName('close')[0];

    openModalBtn.onclick = function () {
        modal.style.display = 'block';
    }

    closeModalBtn.onclick = function () {
        modal.style.display = 'none';
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});
