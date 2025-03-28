document.addEventListener('DOMContentLoaded', function () {
    const today = new Date().toISOString().split('T')[0];

    const createEventButton = document.getElementById('createEventButton');
    const createEventButtonSmall = document.getElementById('createEventButtonSmall');
    const createEventMenu = document.getElementById('createEventMenu');
    const blurredBackground = document.getElementById('blurred-background');
    const selectedDateElement = document.getElementById('selected-date');
    const displayedDateElement = document.getElementById('displayed-date');
    const eventForm = document.getElementById('createEventForm');
    const noEventsMessage = document.getElementById('no-events-message');
    const eventsContainer = document.getElementById('events-container');

    // Функция загрузки мероприятий
    const fetchEventsForDate = async (date) => {
        eventsContainer.innerHTML = '';

        try {
            // Лог для проверки даты
            console.log('Sending event_date:', date);

            // Отправка запроса с датой
            const response = await axios.get('/get_events', { params: { event_date: date } });
            const events = response.data.events;

            if (events.length > 0) {
                noEventsMessage.style.display = 'none';  // Скрываем "No events on this date"
                createEventButton.style.display = 'none'; // Прячем большую кнопку
                createEventButtonSmall.style.display = 'block'; // Показываем маленькую кнопку

                events.forEach(event => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <h3>${event.name}</h3>
                        <p><strong>Time:</strong> ${event.event_date.split('T')[1]}</p>
                        <button class="view-details" data-id="${event.id}">View Details</button>
                    `;
                    eventsContainer.appendChild(li);
                });
            } else {
                noEventsMessage.style.display = 'block';  // Показываем "No events on this date"
                createEventButton.style.display = 'block'; // Показываем большую кнопку
                createEventButtonSmall.style.display = 'none'; // Прячем маленькую кнопку
            }
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    };

    // Функция получения событий при выборе даты в календаре
    const fetchEventsForDateWithUIUpdate = async (date) => {
        const eventList = document.getElementById('event-list');
        try {
            const fullDate = date;
            const response = await axios.get('/get_events', { params: { event_date: fullDate } });
            const events = response.data.events;

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

    // Функция для открытия меню создания события
    const toggleCreateEventMenu = (selectedDate) => {
        const isMenuVisible = createEventMenu.style.display === 'block';
        createEventMenu.style.display = isMenuVisible ? 'none' : 'block';
        blurredBackground.style.display = isMenuVisible ? 'none' : 'block';
        if (selectedDate) {
            displayedDateElement.textContent = selectedDate;
        }
    };

    // Функция загрузки погоды для выбранной даты
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

    // Функция для создания карточки события
    function createEventCard(event) {
        const eventCard = document.createElement("div");
        eventCard.classList.add("event-card");

        eventCard.innerHTML = `
            <h3>${event.name}</h3>
            <p><strong>Time:</strong> ${event.event_time}</p>
            <p><strong>Description:</strong> ${event.description}</p>
            <p><strong>Category:</strong> ${event.category ? "Outdoor" : "Indoor"}</p>
        `;

        document.getElementById("events-message").appendChild(eventCard);
    }

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
                fetchEventsForDateWithUIUpdate(selectedDate);
                toggleDateHighlight(info.dayEl);
            },
        });
        calendar.render();

        // Восстановление последней выбранной даты
        const lastSelectedDate = localStorage.getItem('selectedDate') || today;
        selectedDateElement.textContent = lastSelectedDate;
        fetchWeatherForDate(lastSelectedDate);
        fetchEventsForDateWithUIUpdate(lastSelectedDate);
    }

    // Подсветка выбранной даты в календаре
    const toggleDateHighlight = (dayElement) => {
        const previouslySelectedDay = document.querySelector('.fc-day.fc-day-selected');
        if (previouslySelectedDay) {
            previouslySelectedDay.classList.remove('fc-day-selected');
        }
        dayElement.classList.add('fc-day-selected');
    };

    // Обработчик отправки формы создания событий
    eventForm?.addEventListener('submit', (event) => {
        event.preventDefault();
        const selectedDate = displayedDateElement.textContent;
        document.getElementById('selected-date-input').value = selectedDate;
        eventForm.submit();
    });

    // Обработчик открытия меню создания событий (большая кнопка)
    createEventButton?.addEventListener('click', () => {
        const selectedDate = selectedDateElement.textContent || today;
        toggleCreateEventMenu(selectedDate);
    });

    // Обработчик закрытия меню создания событий
    document.getElementById('cancelEventButton')?.addEventListener('click', (e) => {
        e.preventDefault();
        toggleCreateEventMenu();
    });

    if (createEventButtonSmall) {
        createEventButtonSmall.addEventListener('click', () => {
            createEventButton.click();
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        flatpickr("#event-time-picker", {
            enableTime: true,
            noCalendar: true,
            dateFormat: "H:i",
            time_24hr: true
        });
    });

    // Загружаем все события при загрузке страницы
    const fetchAllEvents = async () => {
        try {
            const response = await axios.get('/get_events');  // Замените на правильный эндпоинт
            const events = response.data.events;

            if (events.length > 0) {
                noEventsMessage.style.display = 'none';
                createEventButton.style.display = 'none';
                createEventButtonSmall.style.display = 'block';

                events.forEach(event => {
                    createEventCard(event);  // создаем карточки для всех событий
                });
            } else {
                noEventsMessage.style.display = 'block';
                createEventButton.style.display = 'block';
                createEventButtonSmall.style.display = 'none';
            }
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    };

    // Загрузка всех событий при загрузке страницы
    fetchAllEvents();
});
