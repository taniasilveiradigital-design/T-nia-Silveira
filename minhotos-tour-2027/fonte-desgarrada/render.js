const { chromium } = require('playwright'); const { spawn } = require('child_process'); const fs = require('fs'); const path = require('path');
const [mode, arg] = [process.argv[2], process.argv[3]]; const FPS = 30, DUR = 60;
(async () => {
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.join(__dirname, 'video.html')); await page.evaluate(() => window.ready);
  const grab = async (t, fmt) => { const d = await page.evaluate(([t, f]) => { renderAt(t); return document.getElementById('c').toDataURL(f, .93); }, [t, fmt]); return Buffer.from(d.split(',')[1], 'base64'); };
  if (mode === 'stills') { for (const t of arg.split(',').map(Number)) fs.writeFileSync(path.join(__dirname, `s_${t}.png`), await grab(t, 'image/png')); }
  else {
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-i', 'musica.wav', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-t', String(DUR), '-movflags', '+faststart', arg], { stdio: ['pipe', 'inherit', 'inherit'], cwd: __dirname });
    for (let f = 0; f < FPS * DUR; f++) { const b = await grab(f / FPS, 'image/jpeg'); if (!ff.stdin.write(b)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
