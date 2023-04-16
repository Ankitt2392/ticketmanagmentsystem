const myDiv = document.getElementById('venueadd_button');
  // Add a click event listener to the div
  myDiv.addEventListener('click', function() {
    
});
myDiv.classList.remove('vvcard');
myDiv.style = '';





const parentCard = document.querySelector('#venues-container');
const addChildBtn = document.querySelector('#venueadd_button');
const btnCard = document.querySelector('#plusBtnvenue');

addChildBtn.addEventListener('click', () => {
    const vcard = document.createElement("div");
	vcard.classList.add("vcard");

	// Add the card data to the element
	vcard.innerHTML = `
		<h1>Venue x</h1>
	`;
    btnCard.parentNode.insertBefore(vcard, btnCard);
});