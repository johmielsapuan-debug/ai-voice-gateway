import 'dotenv/config';
import express from 'express';
import fetch from 'node-fetch';
const app = express();
app.use(express.static('public'));
app.use(express.text({ type: ['application/sdp','text/plain'] }));
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
if (!OPENAI_API_KEY){ console.warn('OPENAI_API_KEY is not set');}
app.post('/session', async(req,res)=>{ try{ const offer=req.body; const r=await fetch('https://api.openai.com/v1/realtime/calls',{ method:'POST', headers:{ 'Authorization':`Bearer ${OPENAI_API_KEY}`, 'Content-Type':'application/sdp'}, body:offer}); const answer=await r.text(); res.setHeader('Content-Type','application/sdp'); res.send(answer);}catch(e){ console.error(e); res.status(500).send('Error');}});
const port = process.env.PORT || 8787;
app.listen(port,()=>console.log(`Realtime gateway listening on ${port}`));