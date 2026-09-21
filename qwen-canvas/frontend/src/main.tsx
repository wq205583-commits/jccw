import React,{useRef,useState} from "react";
import {createRoot} from "react-dom/client";
import {Stage,Layer,Image as KImage} from "react-konva";
import "./style.css";

const API="http://127.0.0.1:8000";
function App(){
 const [nodes,setNodes]=useState<any[]>([]),[prompt,setPrompt]=useState(""),[busy,setBusy]=useState(false);
 const [scale,setScale]=useState(1),[pos,setPos]=useState({x:0,y:0}); const input=useRef<HTMLInputElement>(null);
 const addBlob=(blob:Blob)=>{
   const url=URL.createObjectURL(blob); const img=new Image();
   img.onload=()=>setNodes(n=>[...n,{img,x:80+n.length*35,y:80+n.length*35,w:Math.min(img.width,700),h:Math.min(img.height,700)*img.height/img.width}]);
   img.src=url;
 };
 const upload=(e:any)=>{[...e.target.files].forEach((f:any)=>addBlob(f));};
 const gen=async()=>{
   if(!prompt.trim()) return; setBusy(true);
   try{const fd=new FormData();fd.append("prompt",prompt);fd.append("width","1024");fd.append("height","1024");fd.append("steps","30");fd.append("seed","-1");
   const r=await fetch(API+"/api/generate",{method:"POST",body:fd}); if(!r.ok)throw new Error(await r.text());
   const j=await r.json(); addBlob(await (await fetch(API+j.url)).blob());}
   catch(e:any){alert(e.message)} finally{setBusy(false)}
 };
 return <div className="app">
  <header><b>Qwen Canvas</b><span>Qwen-Image-2.1 · RTX 4080 16G</span></header>
  <aside className="tools"><button onClick={()=>input.current?.click()}>＋ 图片</button><input ref={input} hidden type="file" accept="image/*" multiple onChange={upload}/><button onClick={()=>setNodes([])}>清空</button></aside>
  <main><Stage width={window.innerWidth-390} height={window.innerHeight-52} draggable x={pos.x} y={pos.y} scaleX={scale} scaleY={scale}
   onDragEnd={e=>setPos({x:e.target.x(),y:e.target.y()})}
   onWheel={e=>{e.evt.preventDefault();setScale(s=>Math.max(.15,Math.min(4,s*(e.evt.deltaY>0?.9:1.1))))}}>
   <Layer>{nodes.map((n,i)=><KImage key={i} image={n.img} x={n.x} y={n.y} width={n.w} height={n.h} draggable/>)}</Layer>
  </Stage></main>
  <section className="panel"><h3>AI 创作</h3><label>提示词</label><textarea value={prompt} onChange={e=>setPrompt(e.target.value)} placeholder="例如：古风庭院，电影级光影…"/><div className="hint">v0.1：文生图 · 无限画布 · 本地推理</div><button className="generate" disabled={busy} onClick={gen}>{busy?"生成中…":"✦ 生成"}</button></section>
 </div>
}
createRoot(document.getElementById("root")!).render(<App/>);
