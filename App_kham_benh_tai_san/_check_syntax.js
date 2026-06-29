const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const scripts = html.match(/<script>([\s\S]*?)<\/script>/g);
if (scripts) {
  scripts.forEach((content, i) => {
    try {
      require('vm').Script(content.replace(/<\/?script>/g, ''));
    } catch (e) {
      console.error('Syntax error in script ' + i + ':', e.message);
    }
  });
}
