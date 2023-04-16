// const myDivs = document.getElementsByClassName('showadd_button');
// const myDivas = document.getElementsByTagName('button');

// myDivs[0].addEventListener('click', function () {
//   console.log("hi");

// });
// myDivs.classList.remove('card');
// myDivs.style = '';




const parentCards = document.querySelector('.venues');
const addChildBtns = document.querySelector('#showadd_button');
// const btnCards = document.querySelector('#plusBtnshow');

// addChildBtns.addEventListener('click', () => {
//   const card = document.createElement("div");
//   card.classList.add("card");

//   // Add the card data to the element
//   card.innerHTML = `
//         <h2>Show x</h2>
//         <p>Timings: x</p>
//         <button class="actions_button" id="actions_button">Actions</button>
//     `;
//   btnCards.parentNode.insertBefore(card, btnCards);
// });


function addShow(element) {
  console.log(element.id);
  const btnCards = document.querySelector(`#${element.id}`);
  const parent = btnCards.parentNode;
  const card = document.createElement("div");
  card.classList.add("card");
  card.classList.add("card"+6);

  // Add the card data to the element
  card.innerHTML = `
        <h2>Show x</h2>
        <p>Timings: x</p>
        <button class="actions_button" id="actions_button">Actions</button>
    `;
  parent.parentNode.insertBefore(card, parent);

}
