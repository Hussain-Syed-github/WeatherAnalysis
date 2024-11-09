document.getElementById("citySelector").addEventListener("change", function() {
    const city = this.value;
    fetch(`/api/weather_summary/${city}`)
        .then(response => response.json())
        .then(data => {
            let summary = `<h2>Weather Summary for ${city}</h2>`;
            data.forEach(day => {
                summary += `<p>${day.date}: Avg Temp - ${day.avg_temp.toFixed(1)}°C, Max Temp - ${day.max_temp.toFixed(1)}°C, Min Temp - ${day.min_temp.toFixed(1)}°C, Condition - ${day.condition}</p>`;
            });
            document.getElementById("weatherSummary").innerHTML = summary;
        });
});
