function fetchLeaderboardData() {
    return fetch('data.json')
        .then(response => response.json())
        .then(obj => {
            // Create a dictionary from the fetched data
            const dictionary = {};
            for (const key in obj) {
                if (obj.hasOwnProperty(key)) {
                    const name = obj[key].name;
                    const score = obj[key].score;
                    dictionary[name] = { score };
                }
            }
            return dictionary;
        })
        .catch(error => {
            console.error("Something went wrong", error);
            return {};
        });
}

// Function to update the leaderboard
async function updateLeaderboard() {
    const data = await fetchLeaderboardData();
    const tbody = document.querySelector('#leaderboard tbody');
    tbody.innerHTML = ''; // Clear existing data

    // Convert dictionary to an array of objects for easy sorting and rendering
    const dataArray = Object.keys(data).map(name => ({
        name,
        score: data[name].score
    }));

    // Sort by score in descending order
    dataArray.sort((a, b) => b.score - a.score);

    dataArray.forEach((item, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index+1}</td>
            <td>${item.name}</td>
            <td>${item.score.toFixed(2)}</td>
        `;
        tbody.appendChild(row);
    });
}

setInterval(updateLeaderboard, 0); // Updates every 5 seconds