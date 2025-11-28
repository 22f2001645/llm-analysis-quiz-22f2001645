const { chromium } = require("playwright");

(async () => {
    const url = process.argv[2];

    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();

    await page.goto(url, { waitUntil: "networkidle" });

    const content = await page.content();

    console.log(content);

    await browser.close();
})();
