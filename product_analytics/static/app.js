let products = [];
let sortField = '', sortDir = 1;

async function fetchData() {
    const params = new URLSearchParams({
        min_price: document.getElementById("min_price").value,
        max_price: document.getElementById("max_price").value,
        min_rating: document.getElementById("min_rating").value,
        min_reviews: document.getElementById("min_reviews").value
    });
    const res = await fetch(`/api/products/?${params}`);
    products = await res.json();
    renderTable();
    renderCharts();
}

function sortBy(field) {
    if (sortField === field) sortDir *= -1;
    else {
        sortField = field;
        sortDir = 1;
    }
    products.sort((a, b) => (a[field] > b[field] ? 1 : -1) * sortDir);
    renderTable();
}

function renderTable() {
    const tbody = document.querySelector("#productTable tbody");
    tbody.innerHTML = "";
    products.forEach(p => {
        const row = `<tr>
      <td>${p.name}</td>
      <td>${(+p.price).toFixed(2)}₽</td>
      <td>${(+p.discounted_price).toFixed(2)}₽</td>
      <td>${p.rating}</td>
      <td>${p.review_count}</td>
      <td><a href="${p.link}" target="_blank" rel="noopener noreferrer">Открыть карточку товара</a></td>
    </tr>`;
        tbody.insertAdjacentHTML('beforeend', row);
    });
}

function renderCharts() {
    if (window.priceChartObj) window.priceChartObj.destroy();
    if (window.discountChartObj) window.discountChartObj.destroy();

    const buckets = [0, 2000, 4000, 6000, 8000, 10000];
    const counts = buckets.map((min, i) => {
        const max = buckets[i + 1] ?? Infinity;
        return products.filter(p => p.price >= min && p.price < max).length;
    });
    window.priceChartObj = new Chart("priceChart", {
        type: 'bar',
        data: {
            labels: ['0–2k', '2–4k', '4–6k', '6–8k', '8–10k', '10k+'],
            datasets: [{label: 'Товары по цене', data: counts, backgroundColor: '#4e79a7'}]
        }
    });

    const discounts = products.map(p => (p.price - p.discounted_price));
    const ratings = products.map(p => p.rating);
    window.discountChartObj = new Chart("discountChart", {
        type: 'line',
        data: {
            labels: ratings,
            datasets: [{
                label: 'Скидка vs Рейтинг',
                data: discounts,
                backgroundColor: 'rgba(255,99,132,0.3)',
                borderColor: 'rgba(255,99,132,1)',
                pointRadius: 4,
                tension: 0.25
            }]
        },
        options: {
            scales: {
                x: {title: {display: true, text: 'Рейтинг'}},
                y: {title: {display: true, text: 'Скидка'}}
            }
        }
    });
}

fetchData();