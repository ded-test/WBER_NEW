document.addEventListener('DOMContentLoaded', function () {
    const today = new Date().toISOString().split('T')[0];

    const createEventButton = document.getElementById('createEventButton');
    const createEventMenu = document.getElementById('createEventMenu');
    const blurredBackground = document.getElementById('blurred-background');
    const selectedDateElement = document.getElementById('selected-date');
    const displayedDateElement = document.getElementById('selected-date');
    const eventForm = document.getElementById('createEventForm');
    const noEventsMessage = document.getElementById('no-events-message');
    const eventsMessage = document.getElementById('events-message');
    const eventList = document.getElementById('event-list');
    const createEventButtonNoEvents = document.getElementById('createEventButtonNoEvents');

    // Функция для получения событий по дате
    const fetchEventsForDate = async (date) => {
        try {
            const response = await axios.get('/get_events', { params: { event_date: date } });
            const events = response.data.events || [];

            if (events.length > 0) {
                noEventsMessage.style.display = 'none';
                eventsMessage.style.display = 'block';
                eventList.innerHTML = events.map(event => {
                    const categoryText = event.category ? "Outdoor" : "Indoor";

                    return `
                        <div class="event-card">
                            <div class="event-info">
                                <h3><strong>Name:</strong> ${event.name}</h3>
                                <p>${event.description || 'No description available'}</p>
                                <p><strong>Category:</strong> ${categoryText}</p>
                                <p><strong>Date:</strong> ${event.event_time}</p>
                            </div>
                            <div class="event-actions">
                                <button class="edit-btn" data-event-id="${event.id}">✏️</button>
                                <button class="delete-btn" data-event-id="${event.id}">🗑️</button>
                            </div>
                        </div>
                    `;
                }).join('');

                // Добавление обработчиков событий для кнопок редактирования и удаления
                document.querySelectorAll('.edit-btn').forEach(button => {
                    button.addEventListener('click', function() {
                        const eventId = this.getAttribute('data-event-id');
                        editEvent(eventId);
                    });
                });

                document.querySelectorAll('.delete-btn').forEach(button => {
                    button.addEventListener('click', function() {
                        const eventId = this.getAttribute('data-event-id');
                        deleteEvent(eventId);
                    });
                });
            } else {
                eventList.innerHTML = '';
                noEventsMessage.style.display = 'block';
                eventsMessage.style.display = 'none';
            }
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    };

    document.getElementById('update-cancelEventButton').onclick = () => {
        document.getElementById('blurred-background-update').style.display = 'none'; // Скрыть фон
        document.getElementById('createEventMenuUpf').style.display = 'none'; // Скрыть форму редактирования
    };

    // Функция для отображения/скрытия меню создания события
const toggleCreateEventMenu = (selectedDate) => {
    const isMenuVisible = createEventMenu.style.display === 'block';
    createEventMenu.style.display = isMenuVisible ? 'none' : 'block';
    blurredBackground.style.display = isMenuVisible ? 'none' : 'block';
    if (selectedDate) {
        document.getElementById('displayed-date-create').textContent = selectedDate; // Установите отображаемую дату
        document.getElementById('selected-date-input').value = selectedDate; // Установите скрытое поле даты
    }
};

    // Функция для получения погоды для заданной даты
    const fetchWeatherForDate = async (date) => {
        const weatherResultElement = document.getElementById('weather-result');
        if (!weatherResultElement) return;

        try {
            const response = await axios.get('/weather', { params: { date } });
            const weatherForecast = response.data.forecast || [];
            weatherResultElement.innerHTML = weatherForecast.length ? weatherForecast.join('<br>') : 'No weather data available.';
        } catch (error) {
            weatherResultElement.textContent = 'Error retrieving weather data!';
        }
    };

window.editEvent = async (eventId) => {
    const eventData = await fetch(`/get_event_for_update/${eventId}`);
    const event = await eventData.json();

    document.getElementById('update-event-id').value = event.id;
    document.getElementById('update-selected-date-input').value = event.event_date; // Установите скрытое поле даты
    document.getElementById('displayed-date-update').textContent = event.event_date; // Установите отображаемую дату
    document.getElementById('update-event-name').value = event.name;
    document.getElementById('update-event_time').value = event.event_time;
    document.getElementById('update-event-description').value = event.description;

    // Установка значения категории
    if (event.category) {
        document.getElementById('update-category-indoor').checked = true;
    } else {
        document.getElementById('update-category-outdoor').checked = true;
    }

    // Отображение формы редактирования
    document.getElementById('blurred-background-update').style.display = 'block';
    document.getElementById('createEventMenuUpf').style.display = 'block';
};

    // Функция для удаления события
    window.deleteEvent = async (eventId) => {
        const confirmDelete = confirm("Are you sure you want to delete this event?");
        if (!confirmDelete) return;

        try {
            const response = await fetch("/delete_event", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    event_id: eventId,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                alert(data.message);
                fetchEventsForDate(selectedDateElement.textContent); // обновляем список событий
            } else {
                alert(`Error: ${data.detail}`);
            }
        } catch (error) {
            console.error("Error deleting event:", error);
            alert("Failed to delete event.");
        }
    };

    function createEvent(eventData) {
    // Отправка данных для создания события
    $.ajax({
        url: '/create_event',
        method: 'POST',
        data: eventData,
        success: function(response) {
            // Закрытие меню создания события
            closeEventCreationMenu();

            // Повторный запрос на получение событий
            getEvents();
        },
        error: function(error) {
            console.error('Ошибка при создании события:', error);
        }
    });
}

function closeEventCreationMenu() {
    // Логика для закрытия меню
    $('#eventCreationMenu').hide();
}

function getEvents() {
    $.ajax({
        url: '/get_event',
        method: 'GET',
        success: function(events) {
            // Обработка полученных событий
            displayEvents(events);
        },
        error: function(error) {
            console.error('Ошибка при получении событий:', error);
        }
    });
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

        // Обработчик формы создания события
    eventForm?.addEventListener('submit', (event) => {
        event.preventDefault();
        const selectedDate = displayedDateElement.textContent;
        document.getElementById('selected-date-input').value = selectedDate;
        eventForm.submit();
    });

    // Функция для выделения выбранной даты
    const toggleDateHighlight = (dayElement) => {
        document.querySelectorAll('.fc-day-selected').forEach(el => el.classList.remove('fc-day-selected'));
        dayElement.classList.add('fc-day-selected');
    };

    createEventButton?.addEventListener('click', () => {
        const selectedDate = selectedDateElement.textContent || today;
        toggleCreateEventMenu(selectedDate);
    });

    // Открытие меню создания события для кнопки без событий
    createEventButtonNoEvents?.addEventListener('click', () => {
        const selectedDate = selectedDateElement.textContent || today;
        toggleCreateEventMenu(selectedDate);
    });

    // Закрытие меню создания события
    document.getElementById('cancelEventButton')?.addEventListener('click', (e) => {
        e.preventDefault();
        toggleCreateEventMenu();
    });
});


