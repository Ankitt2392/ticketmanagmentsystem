var btn = 0;
const venuesContainer = document.getElementById("venues-container");

// const venueData = [
// 	{ name: "Venue 1",  cards: [ { name: "Show 1", time: 30 }, { name: "Show 2", time: 25 }, { name: "Show 3", time: 40 } ] },
// 	{ name: "Venue 2",  cards: [ { name: "Show 4", time: 30 }, { name: "Show 5", time: 25 }, { name: "Show 6", time: 40 } ] },
// 	{ name: "Venue 3",  cards: [ { name: "Show 7", time: 30 }, { name: "Show 8", time: 25 }, { name: "Show 9", time: 40 }, { name: "Show 10", time: 25 } ] }
// ];


var venueData = data;
const numVenueToPrint = venueData.length;
console.log(venueData);
// --- Global variable keeping track of number of venues---
var venues = venueData.length;

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
        <div class="venuebuttons" id="venueid">
        <button class="primary-btn venbutupd" id="venbutupd${i+1}" onClick="updelvenue(this, '${vcardDataItem.name}', '${vcardDataItem.place}', '${vcardDataItem.location}', '${vcardDataItem.capacity}', '${vcardDataItem.venueid}')">Update/Delete</button>
        </div>
	`;

	// Add the card element to the card container
	venuesContainer.appendChild(vcard);
    createShows(i);
}
const vcard = document.createElement("div");
vcard.classList.add("vvcard");
vcard.innerHTML = `<button class="venueadd_button" id="venueadd_button" href="{{ url_for('newvenue') }}"><img class="add-venue-img" id="add-venue-img" src="static/images/plus_icon.png" alt="Add a new Show"></button>`;
vcard.setAttribute('id', 'plusBtnvenue');
// Add the card element to the card container
venuesContainer.appendChild(vcard);



function updelvenue(id, name, place, vlocation, vcapacity, vid){
    location.href = 'updatevenue';
    sessionStorage.setItem('uvenue_name', name);
    sessionStorage.setItem('uvenue_place', place);
    sessionStorage.setItem('uvenue_loc', vlocation);
    sessionStorage.setItem('uvenue_cap', vcapacity);
    sessionStorage.setItem('uvenue_id' , vid);
}





function createShows(x) {
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
        console.log(cardDataItem.showid);
        card.innerHTML = `
            <h2>${cardDataItem.name}</h2>
            <p>Timings: ${cardDataItem.time}</p>
            <button class="actions_button" id="actions_button" onClick="updelshow(this, '${cardDataItem.name}', '${cardDataItem.rating}', '${cardDataItem.tag}', '${cardDataItem.price}', '${cardDataItem.showid}', '${cardDataItem.time}')">Actions</button>
        `;

        // Add the card element to the card container
        showsContainer.appendChild(card);
    }
    btn = btn + 1;
    const card = document.createElement("div");
    card.classList.add("card");
    card.innerHTML = `<button class="showadd_button" onclick="addShow(${venueData[x].venueid})" id="plusBtnshow${btn}" href=""{{ url_for('newshow') ><img class="add-show-img" id="add-show-img" src="static/images/plus_icon.png" alt="Add a new Show"></button>`;
    // card.setAttribute('id',`plusBtnshow${btn}`);
    // Add the card element to the card container
    showsContainer.appendChild(card);
}

// --- Function responsible for changing the page ---
function addShow(element) {
    let cookie = element;
    window.location.href = 'newshow';
    sessionStorage.setItem('venue_id', cookie);
}





const parentCard = document.querySelector('#venues-container');
const addChildBtn = document.querySelector('#venueadd_button');
const btnCard = document.querySelector('#plusBtnvenue');

addChildBtn.addEventListener('click', () => {
    window.location.href = 'newvenue';
    venues+=1;
    sessionStorage.setItem('venue_no', venues + 1);
    console.log(venues);
});


function updelshow(id, name, rat, tag, price, showid, time){
    location.href = 'updateshow';
    sessionStorage.setItem('ushow_name', name);
    sessionStorage.setItem('ushow_rating', rat);
    sessionStorage.setItem('ushow_tag', tag);
    sessionStorage.setItem('ushow_price', price);
    sessionStorage.setItem('ushow_showid', showid);
    sessionStorage.setItem('ushow_time', time);    
}