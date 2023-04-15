var btn = 0;
const venuesContainer = document.getElementById("venues-container");

var venueData = data;
const numVenueToPrint = venueData.length;


for (let i = 0; i < numVenueToPrint; i++) {
	// Create a new card element
	const vcard = document.createElement("div");
	vcard.classList.add("vcard");
	vcard.classList.add("vcard"+(i+1));
    vcard.setAttribute('id', 'shows-container'+(i+1));
    console.log(vcard)
	// Add the card data to the element
	const vcardDataIndex = i % venueData.length; // Use modulo to cycle through the data
	const vcardDataItem = venueData[vcardDataIndex];
	vcard.innerHTML = `
		<h1>${vcardDataItem.name}</h1>
	`;

	// Add the card element to the card container
	venuesContainer.appendChild(vcard);
    createShows(i, vcardDataItem.name);
}






function createShows(x, venue_name) {
    //Show creation
    const showsContainer = document.getElementById("shows-container"+(x+1));

    const numCardsToPrint = venueData[x].cards.length;

    for (let i = 0; i < numCardsToPrint; i++) {
        // Create a new card element
        const card = document.createElement("div");
        card.classList.add("card");
        card.classList.add("card"+(i+1));
        card.setAttribute('id', 'card-cont');
        console.log(card)

        // Add the card data to the element
        const cardDataIndex = i; // Use modulo to cycle through the data
        const cardDataItem = venueData[x].cards[cardDataIndex];
        card.innerHTML = `
            <h2>${cardDataItem.name}</h2>
            <p>Timings: ${cardDataItem.time}</p>
            <button class="bookings_button" id="bookings_button${x+1}" onclick="bookings(this, '${cardDataItem.name}', '${venue_name}')">Book Tickets</button>
        `;

        // Add the card element to the card container
        showsContainer.appendChild(card);
    }
    btn = btn + 1;
}

// document.getElementById("bookings_button").onclick = function () {
//     location.href = 'ticketbooking';
// };
function bookings(element, show_name, venue_name){
    // console.log(venue_name);
    // var str = element.id;
    // var venueID = str.charAt(str.length-1);
    document.getElementById("booking_show").value = show_name
    document.getElementById("booking_venue").value = venue_name
    // sessionStorage.setItem("booking_venue", venue_name);
    // sessionStorage.setItem("booking_show", show_name);
    document.getElementById("booking_form").submit(); 
    // console.log('wait');
    // location.href = 'ticketbooking'; 
}