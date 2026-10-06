document.addEventListener("DOMContentLoaded", () => {
    console.log("Page Loaded - Real Share!");
});
function calculateReturns() {
    const investment = document.getElementById("investment").value;

    if (investment && investment > 0) {
        const roi = 10; // Assume a fixed ROI of 10% for simplicity
        const totalReturns = (investment * roi) / 100;

        document.getElementById("roi").textContent = roi;
        document.getElementById("total-returns").textContent = totalReturns.toFixed(2);
    } else {
        alert("Please enter a valid investment amount!");
    }
}
