document.addEventListener('DOMContentLoaded', function () {
    const today = new Date().toISOString().split('T')[0];

    const createEventButton = document.getElementById('createEventButton');
    const createEventMenu = document.getElementById('createEventMenu');
    const blurredBackground = document.getElementById('blurred-background');
    const selectedDateElement = document.getElementById('selected-date');
    const displayedDateElement = document.getElementById('displayed-date');
    const eventForm = document.getElementById('createEventForm');

    // Функция для получения списка событий по дате
    const fetchEventsForDate = async (date) => {
        const eventsContainer = document.getElementById('events-container');
        const noEventsMessage = document.getElementById('no-events-message');
        const eventList = document.getElementById('event-list');

        try {
            // Добавляем время 00:00:00, если сервер ожидает полный формат datetime
            const fullDate = `${date}T00:00:00`;
            const response = await axios.get('/get_events', { params: { event_date: fullDate } });
            const events = response.data.events; // Убедись, что сервер возвращает массив `events`

            if (events.length > 0) {
                noEventsMessage.style.display = 'none';
                eventList.style.display = 'block';
                eventsContainer.innerHTML = events.map(event => `
                    <li>
                        <h3>${event.name}</h3>
                        <p>${event.description || 'No description available'}</p>
                        <p><strong>Date:</strong> ${event.event_date}</p>
                        <p><strong>Category:</strong> ${event.category}</p>
                    </li>
                `).join('');
            } else {
                eventList.style.display = 'none';
                noEventsMessage.style.display = 'block';
            }
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    };

    // Функция для показа/скрытия меню создания событий
    const toggleCreateEventMenu = (selectedDate) => {
        const isMenuVisible = createEventMenu.style.display === 'block';
        createEventMenu.style.display = isMenuVisible ? 'none' : 'block';
        blurredBackground.style.display = isMenuVisible ? 'none' : 'block';
        if (selectedDate) {
            displayedDateElement.textContent = selectedDate;
        }
    };

    // Функция для получения погоды по дате
    const fetchWeatherForDate = async (date) => {
        const weatherResultElement = document.getElementById('weather-result');
        if (weatherResultElement) {
            try {
                const response = await axios.get('/weather', { params: { date } });
                const weatherForecast = response.data.forecast || [];
                weatherResultElement.innerHTML = weatherForecast.length ? weatherForecast.join('<br>') : 'No weather data available.';
            } catch (error) {
                weatherResultElement.textContent = 'Error retrieving weather. Check if your city is correct!';
            }
        }
    };

    // Инициализация календаря
    const calendarEl = document.getElementById('calendar');
    if (calendarEl) {
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            initialDate: today,
            dateClick: (info) => {
                const selectedDate = info.dateStr;
                selectedDateElement.textContent = selectedDate;
                localStorage.setItem('selectedDate', selectedDate);
                fetchWeatherForDate(selectedDate);
                fetchEventsForDate(selectedDate);
                toggleDateHighlight(info.dayEl);
            },
        });
        calendar.render();

        // Восстановление последней выбранной даты
        const lastSelectedDate = localStorage.getItem('selectedDate') || today;
        selectedDateElement.textContent = lastSelectedDate;
        fetchWeatherForDate(lastSelectedDate);
        fetchEventsForDate(lastSelectedDate);
    }

    // Функция выделения выбранной даты
    const toggleDateHighlight = (dayElement) => {
        const previouslySelectedDay = document.querySelector('.fc-day.fc-day-selected');
        if (previouslySelectedDay) {
            previouslySelectedDay.classList.remove('fc-day-selected');
        }
        dayElement.classList.add('fc-day-selected');
    };

    // Обработчик формы создания события
    eventForm?.addEventListener('submit', (event) => {
        event.preventDefault();
        const selectedDate = displayedDateElement.textContent;
        document.getElementById('selected-date-input').value = selectedDate;
        eventForm.submit();
    });

    // Открытие меню создания события
    createEventButton?.addEventListener('click', () => {
        const selectedDate = selectedDateElement.textContent || today;
        toggleCreateEventMenu(selectedDate);
    });

    // Закрытие меню создания события
    document.getElementById('cancelEventButton')?.addEventListener('click', (e) => {
        e.preventDefault();
        toggleCreateEventMenu();
    });
});
