var chartData = data;
const chartContainer = document.getElementById("chartContainer");
console.log(chartData);

var chartDataLength = chartData.length;

//show.append({"name": sho.show_name, "showid": sho.show_id, "rating": avg_rating})
//venu.append({"name": ven.venue_name, "cards": show, "venueid": ven.venue_id})


for (let i = 0; i < chartDataLength; i++) {
	const cancard = document.createElement("canvas");
	cancard.classList.add("cancard");
    cancard.setAttribute('id', 'myChart'+(i+1));
    console.log(cancard);
	chartContainer.appendChild(cancard);
    let movieList = [];
    let ratingList = [];
    for (let j=0; j<chartData[i].cards.length; j++){
        movieList.push(chartData[i].cards[j].name);
        ratingList.push(chartData[i].cards[j].rating);
    }
    console.log(movieList);
    console.log(ratingList);
    var venueName = chartData[i].name;
    createChart(i, venueName, movieList, ratingList);
}

function createChart(i, cvenueName, cmovieList, cratingList) {
    const ctx = document.getElementById('myChart'+(i+1));
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: cmovieList,
            datasets: [{
            label: '',
            data: cratingList,
            borderWidth: 2,
            barThickness: 50
            }]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: cvenueName,
                    font: {
                        size: 24
                    }
                }
            },
            responsive: false,
            scales: {
            x: {
                title: {
                    color: 'black',
                    display: true,
                    text: 'Shows',
                    font: {
                        size: 18
                    }
                }
            }
            }
        }
    });
}