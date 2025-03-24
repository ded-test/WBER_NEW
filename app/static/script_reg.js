window.onload = function () {
    const savedCity = localStorage.getItem('city');
    const cityInput = document.getElementById('city-input');
    if (savedCity && cityInput) {
        cityInput.value = savedCity;
    }
};

const form = document.querySelector('.registrationForm');
if (form) {
    form.addEventListener('submit', (e) => {
        const city = document.getElementById('city-input')?.value;
        if (city) {
            localStorage.setItem('city', city);
        }
    });
}

const input = document.getElementById('city-input');
const suggestionsBox = document.getElementById('suggestions');

if (input && suggestionsBox) {
    input.addEventListener('input', async () => {
        const query = input.value.trim();
        if (query.length > 0) {
            try {
                const response = await fetch(`/cities?prefix=${query}`);
                if (!response.ok) {
                    throw new Error(`Server error: ${response.status}`);
                }
                const data = await response.json();
                const cities = data.cities;

                suggestionsBox.innerHTML = '';
                if (cities.length > 0) {
                    cities.forEach(city => {
                        const div = document.createElement('div');
                        div.textContent = city;
                        div.addEventListener('click', () => {
                            input.value = city;
                            suggestionsBox.innerHTML = ''; 
                        });
                        suggestionsBox.appendChild(div);
                    });
                } else {
                    suggestionsBox.innerHTML = '<div>No cities found</div>';
                }
            } catch (error) {
                console.error("Error fetching city suggestions:", error);
                suggestionsBox.innerHTML = '<div>Error loading suggestions</div>';
            }
        } else {
            suggestionsBox.innerHTML = '';
        }
    });
}
function showError(message) {
    document.getElementById('form-error').style.display = 'block';
    document.getElementById('error-message').textContent = message;
}

    // Функция для отображения ошибок
    function displayError(message) {
        const errorElement = document.getElementById('form-error');
        const errorMessageElement = document.getElementById('error-message');

        // Отображаем ошибку
        errorElement.style.display = 'block';
        errorMessageElement.textContent = message;
    }

    document.querySelector('.registrationForm').addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());

        if (!data.username || !data.mail || !data.password) {
            displayError("All fields are required.");
            return;
        }

        this.submit();
    });