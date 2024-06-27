const all_seats = document.querySelectorAll('.row .seat');
const cta_btn = document.querySelector('button.purchase_btn');
const movieSelect = document.getElementById('movie');

let ticketPrice = +movieSelect.value;

// Function to contact API
async function contactAPI(url, body) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

    return response.json();
}

// Function to update selected count and total
function updateSelectedCount() {
    const selectedSeats = document.querySelectorAll('.row .seat.selected');
    const seatsIndex = [...selectedSeats].map(seat => [...all_seats].indexOf(seat));

    localStorage.setItem('selectedSeats', JSON.stringify(seatsIndex));

    const selectedSeatsCount = selectedSeats.length;

    document.getElementById('count').innerText = selectedSeatsCount;
    document.getElementById('total').innerText = selectedSeatsCount * ticketPrice;

    setMovieData(movieSelect.selectedIndex, movieSelect.value);
}

// Function to set movie data in localStorage
function setMovieData(movieIndex, moviePrice) {
    localStorage.setItem('selectedMovieIndex', movieIndex);
    localStorage.setItem('selectedMoviePrice', moviePrice);
}

// Function to refresh occupied seats
function refreshSeat() {
    const movie_title = movieSelect.options[movieSelect.selectedIndex].id;

    contactAPI("/tickets/occupied/", { movie_title }).then(data => {
        const occupied_seat = data['occupied_seats'];
        const movie_title = data["movie"];

        const seat_LocalStorage = localStorage.getItem('selectedSeats') ? JSON.parse(localStorage.getItem('selectedSeats')) : null;
        const movie_index = localStorage.getItem("selectedMovieIndex");

        all_seats.forEach(seat => {
            seat.classList.remove("occupied");
        });

        const LS_movie = movieSelect.options[movie_index].textContent;

        if (LS_movie === movie_title) {
            if (occupied_seat !== null && occupied_seat.length > 0) {
                all_seats.forEach((seat, index) => {
                    if (occupied_seat.indexOf(index) > -1) {
                        seat.classList.add('occupied');
                        seat.classList.remove('selected');
                    }
                });
            }

            if (seat_LocalStorage !== null) {
                seat_LocalStorage.forEach((seat, index) => {
                    if (occupied_seat.includes(seat)) {
                        seat_LocalStorage.splice(index, 1);
                        localStorage.setItem("selectedSeats", JSON.stringify(seat_LocalStorage));
                    }
                });
            }
        }
        updateSelectedCount();
    });
}

// Event listener for movie selection change
movieSelect.addEventListener('change', e => {
    ticketPrice = +e.target.value;
    setMovieData(e.target.selectedIndex, e.target.value);
    updateSelectedCount();
    refreshSeat();
});

// Event listener for seat selection
document.addEventListener('click', e => {
    if (e.target.classList.contains('seat') && !e.target.classList.contains('occupied')) {
        e.target.classList.toggle('selected');
        updateSelectedCount();
    }
});

// Function to populate UI from localStorage
function populateUI() {
    const selectedSeats = JSON.parse(localStorage.getItem('selectedSeats'));

    if (selectedSeats !== null && selectedSeats.length > 0) {
        all_seats.forEach((seat, index) => {
            if (selectedSeats.indexOf(index) > -1) {
                seat.classList.add('selected');
            }
        });
    }

    const selectedMovieIndex = localStorage.getItem('selectedMovieIndex');

    if (selectedMovieIndex !== null) {
        movieSelect.selectedIndex = selectedMovieIndex;
    }
}

// Function to handle payment process
function handlePayment() {
    const movie_title = movieSelect.options[movieSelect.selectedIndex].id;
    const seat_list = JSON.parse(localStorage.getItem("selectedSeats"));

    if (seat_list !== null && seat_list.length > 0) {
        const data = {
            movie_title,
            seat_list
        };

        contactAPI("/tickets/payment/", data).then(res => {
            if (res["payment_url"]) {
                // Redirect the customer to payment URL
                window.location.href = res["payment_url"];
            } else {
                console.log('Error: Payment URL not available');
            }
        }).catch(err => {
            console.error('Error during payment:', err);
        });
    } else {
        console.log('No seats selected');
    }
}

// Event listener for purchase button click
cta_btn.addEventListener("click", e => {
    handlePayment();
});

// Initial setup
updateSelectedCount();
