// Local development only. GitHub Pages serves docs/ directly.
import {createServer} from 'node:http';
import {readFile, stat} from 'node:fs/promises';
import {resolve, extname} from 'node:path';
const root=resolve('docs');
const args=process.argv.slice(2);
const portArg=args.indexOf('--port');
const port=Number(portArg>=0?args[portArg+1]:(process.env.PORT||4173));
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.svg':'image/svg+xml','.pdf':'application/pdf','.docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document','.xml':'application/xml','.txt':'text/plain','.webmanifest':'application/manifest+json'};
createServer(async(req,res)=>{
 try{
  let path=decodeURIComponent(new URL(req.url,'http://local').pathname);
  if(path.startsWith('/eswar-test-repository/'))path=path.slice('/eswar-test-repository'.length);
  if(path==='/__qa_mobile'){
   res.writeHead(200,{'content-type':'text/html; charset=utf-8'});
   res.end('<!doctype html><title>Mobile layout QA</title><style>body{font:16px Arial;background:#dbe2ea;margin:20px}iframe{display:block;width:390px;height:844px;border:1px solid #687988;background:white}</style><p>390 × 844 CSS pixels</p><iframe title="Mobile portfolio preview" src="/"></iframe>');return;
  }
  let file=resolve(root,'.'+path);
  if(!file.startsWith(root+'/')&&file!==root){res.writeHead(403);res.end();return;}
  if((await stat(file)).isDirectory())file=resolve(file,'index.html');
  const buf=await readFile(file);res.writeHead(200,{'content-type':types[extname(file)]||'application/octet-stream','content-length':buf.length});res.end(req.method==='HEAD'?undefined:buf);
 }catch{res.writeHead(404,{'content-type':'text/html; charset=utf-8'});res.end(await readFile(resolve(root,'404.html')));}
}).listen(port,'0.0.0.0',()=>console.log(`Preview ready on ${port}`));
