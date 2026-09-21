import React,{useRef,useState} from "react";
import {createRoot} from "react-dom/client";
import {Stage,Layer,Image as KImage,Transformer} from "react-konva";
import "./style.css";
const API="http://127.0.0.1:8000";
type NodeT={id:string,img:HTMLImageElement,x:number,y:number,w:number,h:number,file?:File};
function App(){
 const [nodes,setNodes]=useState<NodeT[]>([]),[selected,setSelected]=useState<string[]>([]),[prompt,setPrompt]=useState(""),[busy,setBusy]=useState(false);
 const [mode,setMode]=useState("generate"),[ratio,setRatio]=useState("1:1"),[steps,setSteps]=useState(30),[seed,setSeed]=useState(-1),[transparent,setTransparent]=useState(false);
 const [scale,setScale]=useState(1),[pos,setPos]=useState({x:0,y:0}); const input=useRef<HTMLInputElement>(null);
 const sizes:any={"1:1":[1024,1024],"3:4":[896,1200],"4:3":[1200,896],"16:9":[1344,768],"9:16":[768,1344]};
 const addFile=(file:File)=>{const url=URL.createObjectURL(file),img=new Image();img.onload=()=>setNodes(n=>[...n,{id:crypto.randomUUID(),img,x:100+n.length*35,y:100+n.length*35,w:Math.min(img.width,640),h:Math.min(img.width,640)*img.height/img.width,file}]);img.src=url};
 const addBlob=(blob:Blob)=>addFile(new File([blob],"qwen-result.png",{type:"image/png"}));
 const generate=async()=>{if(!prompt.trim())return;setBusy(true);try{
  const fd=new FormData(),[w,h]=sizes[ratio];fd.append("prompt",prompt);fd.append("mode",mode);fd.append("width",w);fd.append("height",h);fd.append("steps",String(steps));fd.append("seed",String(seed));fd.append("transparent",String(transparent));
  if(mode==="edit"){nodes.filter(n=>selected.includes(n.id)).slice(0,10).forEach(n=>n.file&&fd.append("images",n.file!));}
  const r=await fetch(API+"/api/generate",{method:"POST",body:fd}),j=await r.json();if(j.error)throw new Error(j.error);if(!r.ok)throw new Error(JSON.stringify(j));
  addBlob(await(await fetch(API+j.url)).blob());setSeed(j.seed);
 }catch(e:any){alert(e.message)}finally{setBusy(false)}};
 return <div className="app"><header><b>Qwen Canvas</b><span>Qwen-Image-2.1 · RTX 4080 16G</span><i>{selected.length} 个已选</i></header>
 <aside className="tools"><button onClick={()=>input.current?.click()}>＋图片</button><input ref={input} hidden type="file" accept="image/*" multiple onChange={e=>[...(e.target.files||[])].forEach(addFile)}/><button onClick={()=>setSelected([])}>取消选中</button><button onClick={()=>{setNodes([]);setSelected([])}}>清空</button></aside>
 <main><Stage width={window.innerWidth-390} height={window.innerHeight-52} draggable x={pos.x} y={pos.y} scaleX={scale} scaleY={scale} onDragEnd={e=>setPos({x:e.target.x(),y:e.target.y()})} onWheel={e=>{e.evt.preventDefault();setScale(s=>Math.max(.15,Math.min(4,s*(e.evt.deltaY>0?.9:1.1))))}}><Layer>
 {nodes.map(n=><KImage key={n.id} image={n.img} x={n.x} y={n.y} width={n.w} height={n.h} draggable stroke={selected.includes(n.id)?"#fff":undefined} strokeWidth={selected.includes(n.id)?3:0} onClick={e=>{e.cancelBubble=true;setSelected(s=>e.evt.shiftKey?(s.includes(n.id)?s.filter(x=>x!==n.id):[...s,n.id]):[n.id])}}/>)}
 </Layer></Stage></main>
 <section className="panel"><h3>AI 创作</h3><div className="tabs"><button className={mode==="generate"?"on":""} onClick={()=>setMode("generate")}>文生图</button><button className={mode==="edit"?"on":""} onClick={()=>setMode("edit")}>图片编辑</button></div>
 <label>提示词</label><textarea value={prompt} onChange={e=>setPrompt(e.target.value)} placeholder={mode==="edit"?"Shift 选择最多10张图片，然后输入修改要求":"描述你要生成的图片…"}/>
 <label>比例</label><select value={ratio} onChange={e=>setRatio(e.target.value)}>{Object.keys(sizes).map(x=><option>{x}</option>)}</select>
 <label>Steps: {steps}</label><input type="range" min="10" max="50" value={steps} onChange={e=>setSteps(+e.target.value)}/>
 <label>Seed</label><input className="seed" type="number" value={seed} onChange={e=>setSeed(+e.target.value)}/>
 <label className="check"><input type="checkbox" checked={transparent} onChange={e=>setTransparent(e.target.checked)}/> 原生透明 RGBA</label>
 <div className="hint">{mode==="edit"?`将使用已选的 ${Math.min(selected.length,10)} 张参考图`:"生成新图片"} · 预览分辨率</div>
 <button className="generate" disabled={busy} onClick={generate}>{busy?"Qwen 正在生成…":"✦ 生成"}</button></section></div>
}
createRoot(document.getElementById("root")!).render(<App/>);
