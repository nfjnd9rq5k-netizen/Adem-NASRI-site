const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch(); const p=await (await b.newContext()).newPage();
 await p.goto('file://'+path.join(__dirname,'cv.html'),{waitUntil:'load'});
 await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(1200);
 await p.pdf({path:path.join(__dirname,'cv-adem-nasri.pdf'), format:'A4', printBackground:true,
   margin:{top:'13mm',bottom:'13mm',left:'14mm',right:'14mm'}});
 console.log('PDF genere');
 await b.close();})();
