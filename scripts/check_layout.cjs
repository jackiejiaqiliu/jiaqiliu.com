// Optional browser-based layout QA. Uses an installed Playwright; never downloads it.
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const config = JSON.parse(fs.readFileSync(path.join(root, 'data/preview.json')));
const routes = JSON.parse(fs.readFileSync(path.join(root, 'data/routes.json')));
const base = `http://${config.host}:${config.port}`;

(async () => {
  const browser = await chromium.launch({channel: 'chrome', headless: true, timeout: 10000});
  const results = [];
  try {
    const context = await browser.newContext();
    // Third-party playback is outside this layout check; preserve the embed DOM.
    await context.route('**/*', route => {
      const url = route.request().url();
      return url.startsWith(base) || url.startsWith('data:') ? route.continue() : route.abort();
    });
    const page = await context.newPage();
    for (const width of [375, 768, 1440]) {
      await page.setViewportSize({width, height: 1000});
      for (const route of routes) {
        await page.goto(base + route.path, {waitUntil: 'load', timeout: 15000});
        await page.evaluate(() => document.fonts.ready);
        const measurement = await page.evaluate(() => {
          const viewport = document.documentElement.clientWidth;
          const icon = document.querySelector('.local-social-icon');
          const rect = icon?.getBoundingClientRect();
          const overflowing = [...document.querySelectorAll('body *')].filter(element => {
            const box = element.getBoundingClientRect();
            const style = getComputedStyle(element);
            return box.width > 0 && box.height > 0 && style.visibility !== 'hidden' &&
              (box.right > viewport + 1 || box.left < -1);
          }).slice(0, 12).map(element => ({tag: element.tagName, id: element.id,
            class: element.className?.baseVal ?? element.className,
            width: element.getBoundingClientRect().width,
            right: element.getBoundingClientRect().right,
            position: getComputedStyle(element).position}));
          const title = document.querySelector('#pro-gallery-comp-l9xopdjj .local-gallery-item > span');
          const style = title && getComputedStyle(title);
          return {viewport, scrollWidth: document.documentElement.scrollWidth,
            bodyScrollWidth: document.body.scrollWidth,
            icon: rect && {width: rect.width, height: rect.height, right: rect.right, left: rect.left},
            title: style && {font: style.fontFamily, weight: style.fontWeight, size: style.fontSize, lineHeight: style.lineHeight},
            overflowing};
        });
        results.push({route: route.path, width, ...measurement});
      }
    }
    const errors = results.filter(r => r.scrollWidth > r.viewport + 1 || r.bodyScrollWidth > r.viewport + 1 ||
      (r.icon && (r.icon.width > 30.1 || r.icon.right > r.viewport + 1 || r.icon.left < -1)));
    console.log(JSON.stringify({checks: results.length, errors, results}, null, 2));
    if (errors.length) process.exitCode = 1;
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.log(JSON.stringify({status: 'unavailable', error: error.message}, null, 2));
  process.exitCode = 2;
});
