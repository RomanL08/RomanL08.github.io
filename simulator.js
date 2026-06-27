let cash = 1000;
let bitcoin = 0;
let price = 50000;
let marketTrend = 0;
let day = 0;
let candles = [];

let priceHistory = [price];
let candles = [];

function updateScreen() {
    document.getElementById("cash").textContent = cash.toFixed(2);
    document.getElementById("bitcoin").textContent = bitcoin.toFixed(6);
    document.getElementById("price").textContent = price.toFixed(2);
    document.getElementById("day").textContent = day;

    let portfolio = cash + bitcoin * price;
    document.getElementById("portfolio").textContent = portfolio.toFixed(2);

    let profit = portfolio - 1000;
    document.getElementById("profit").textContent = profit.toFixed(2);
}

function buyBitcoin() {
    const amount = 100;

    if (cash >= amount) {
        bitcoin += amount / price;
        cash -= amount;
    }

    updateScreen();
    drawChart();
}

function sellBitcoin() {
    cash += bitcoin * price;
    bitcoin = 0;

    updateScreen();
    drawChart();
}

function nextDay() {

    day++;

    // hier staat de rest van je code
    marketTrend = marketTrend * 0.99 + (Math.random() * 0.002 - 0.001);

    const volatility = 0.025;
    const change = marketTrend + (Math.random() * volatility * 2 - volatility);

    price = price * (1 + change);
    price = Math.max(1000, price);

    priceHistory.push(price);

    drawChart();
    updateScreen();
    drawChart();
}

async function loadRealBitcoinPrice() {
    try {
        const response = await fetch("https://api.coinbase.com/v2/prices/BTC-EUR/spot");
        const data = await response.json();

        price = Number(data.data.amount);

        priceHistory.push(price);

        updateScreen();
        drawChart();

    } catch (error) {
        alert("Could not load real Bitcoin price.");
        console.log(error);
    }
}

function drawChart() {
    const canvas = document.getElementById("priceChart");
    const ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (priceHistory.length < 2) return;

    const minPrice = Math.min(...priceHistory);
    const maxPrice = Math.max(...priceHistory);

    ctx.beginPath();

    priceHistory.forEach((p, index) => {
        const x = (index / (priceHistory.length - 1)) * canvas.width;

        const y = canvas.height - 
            ((p - minPrice) / (maxPrice - minPrice)) * canvas.height;

        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });

    ctx.strokeStyle = "#facc15";
    ctx.lineWidth = 3;
    ctx.stroke();
}

updateScreen();
drawChart();

loadCandles();

setInterval(loadCandles, 60000);