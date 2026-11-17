// usage: node render.js W H out.mp4   |   node render.js W H stills t1,t2,...
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const [W, H, out, times] = [+process.argv[2], +process.argv[3], process.argv[4], process.argv[5]];
const FPS = 30, DUR = 15;
(async () => {
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: W, height: H } });
  await page.goto('file://' + path.join(__dirname, 'tour.html') + `?w=${W}&h=${H}`);
  await page.evaluate(() => window.ready);
  const grab = async t => {
    const d = await page.evaluate(t => { renderAt(t); return document.getElementById('c').toDataURL('image/png'); }, t);
    return Buffer.from(d.split(',')[1], 'base64');
  };
  if (out === 'stills') {
    for (const t of times.split(',').map(Number)) fs.writeFileSync(path.join(__dirname, `still_${W}x${H}_${t}.png`), await grab(t));
  } else {
    const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', out], { stdio: ['pipe', 'ignore', 'inherit'] });
    for (let f = 0; f < FPS * DUR; f++) {
      const buf = await grab(f / FPS);
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
