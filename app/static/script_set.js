function hideMessage() {
    const successMessage = document.getElementById('success-message');
    const errorMessage = document.getElementById('error-message');

    if (successMessage) {
        setTimeout(() => {
            successMessage.style.display = 'none';
        }, 5000); // 5 секунд
    }

    if (errorMessage) {
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 5000); // 5 секунд
    }
}


window.onload = function () {
    hideMessage();

    const savedCity = localStorage.getItem('city');
    const cityInput = document.getElementById('city-input');
    const currentCity = document.getElementById('current-city');

    if (savedCity) {
        if (cityInput) cityInput.value = savedCity;
        if (currentCity) currentCity.innerText = savedCity;
    }
};

const form = document.getElementById('city-form');
if (form) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const cityInput = document.getElementById('city-input');
        const city = cityInput?.value.trim();

        if (city) {
            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ city }).toString(),
                });

                if (response.ok) {
                    localStorage.setItem('city', city);
                    const currentCity = document.getElementById('current-city');
                    if (currentCity) currentCity.innerText = city;
                }
            } catch (error) {
                console.error("Error updating city:", error);
            }
        }
    });
}

const input = document.getElementById('city-input');
const suggestionsBox = document.getElementById('suggestions');

if (input && suggestionsBox) {
    input.addEventListener('input', async () => {
        const query = input.value.trim();
        suggestionsBox.innerHTML = '';

        if (query.length > 0) {
            try {
                const response = await fetch(`/cities?prefix=${encodeURIComponent(query)}`);
                if (!response.ok) {
                    throw new Error(`Server error: ${response.status}`);
                }
                const data = await response.json();
                const cities = data.cities;

                if (cities && cities.length > 0) {
                    cities.forEach(city => {
                        const div = document.createElement('div');
                        div.textContent = city;
                        div.classList.add('suggestion-item');
                        div.addEventListener('click', () => {
                            input.value = city;
                            suggestionsBox.innerHTML = '';
                        });
                        suggestionsBox.appendChild(div);
                    });
                }
            } catch (error) {
                console.error("Error fetching city suggestions:", error);
            }
        }
    });
}
