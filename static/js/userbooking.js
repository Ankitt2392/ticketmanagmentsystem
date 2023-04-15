const venuesContainer = document.getElementById("venues-container");

// var venueData = [{"venue": "Venu1", "show": "Show1"}, {"venue": "Venu1", "show": "Show2"}, {"venue": "Venu2", "show": "Show3"}, {"venue": "Venu1", "show": "Show5"}, {"venue": "Venu3", "show": "Show1"}];
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
	// vcard.innerHTML = `
	// 	<h1>${vcardDataItem.venue}: ${vcardDataItem.show}</h1>
	// `;

	vcard.innerHTML = `
		<h1>${vcardDataItem.venue}: ${vcardDataItem.show}</h1>
        <button class="rate-button" id="RateButton${i}" onclick="changepage(this, '${vcardDataItem.venue}', '${vcardDataItem.show}'); this.disabled = true;">Rate</button>
	`;

	// Add the card element to the card container
	venuesContainer.appendChild(vcard);
}

function changepage(element, venue, show){
	// const btn = document.getElementById(element.id);
	// btn.innerHTML = 'Rating submitted';
	// btn.remove;
	sessionStorage.setItem('rating_venue', venue);
	sessionStorage.setItem('rating_show', show);
	window.location.href = '/rate';
}