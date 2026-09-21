from pathlib import Path

p=Path(__file__).resolve().parent/"infinite-canvas"/"web"/"src"/"stores"/"use-config-store.ts"
s=p.read_text(encoding="utf-8")
if 'id: "local-qwen"' not in s:
    marker='channels: [\n        {'
    q='''channels: [
        {
            id: "local-qwen",
            name: "本地 Qwen-Image-2.1",
            baseUrl: "http://127.0.0.1:8000",
            apiKey: "local-qwen",
            apiFormat: "openai",
            models: [{ name: "Qwen-Image-2.1", capability: "image" }],
        },
        {'''
    s=s.replace(marker,q,1)
    s=s.replace('model: "default::gpt-image-2",','model: "local-qwen::Qwen-Image-2.1",',1)
    s=s.replace('imageModel: "default::gpt-image-2",','imageModel: "local-qwen::Qwen-Image-2.1",',1)
    s=s.replace('models: ["default::gpt-image-2",', 'models: ["local-qwen::Qwen-Image-2.1", "default::gpt-image-2",',1)
# Ensure existing browser configs also receive local Qwen after updates.
needle='const channels = normalizeChannels(config);'
replacement='''let channels = normalizeChannels(config);
                if (!channels.some((channel) => channel.id === "local-qwen")) {
                    channels = [{
                        id: "local-qwen",
                        name: "本地 Qwen-Image-2.1",
                        baseUrl: "http://127.0.0.1:8000",
                        apiKey: "local-qwen",
                        apiFormat: "openai",
                        models: [{ name: "Qwen-Image-2.1", capability: "image" }],
                    }, ...channels];
                }'''
s=s.replace(needle,replacement,1)
p.write_text(s,encoding="utf-8")
print("[OK] Local Qwen provider installed into Infinite Canvas.")


# Runtime migration: persisted Zustand config can keep the old imageModel.
# Add a tiny startup module that force-selects local Qwen once when the provider is first installed.
main=Path(__file__).resolve().parent/"infinite-canvas"/"web"/"src"/"main.tsx"
if main.exists():
    m=main.read_text(encoding="utf-8")
    tag='qwen-local-provider-v2'
    if tag not in m:
        inject='''\n// qwen-local-provider-v2: migrate existing browser config to local Qwen once.\ntry {\n  const key="infinite-canvas:ai_config_store";\n  const raw=localStorage.getItem(key);\n  if(raw){\n    const saved=JSON.parse(raw); const cfg=saved?.state?.config;\n    if(cfg){\n      const q={id:"local-qwen",name:"本地 Qwen-Image-2.1",baseUrl:"http://127.0.0.1:8000",apiKey:"local-qwen",apiFormat:"openai",models:[{name:"Qwen-Image-2.1",capability:"image"}]};\n      cfg.channels=Array.isArray(cfg.channels)?cfg.channels:[];\n      if(!cfg.channels.some((x:any)=>x.id==="local-qwen")) cfg.channels.unshift(q);\n      cfg.imageModel="local-qwen::Qwen-Image-2.1"; cfg.model=cfg.imageModel;\n      cfg.models=Array.from(new Set(["local-qwen::Qwen-Image-2.1",...(cfg.models||[])]));\n      localStorage.setItem(key,JSON.stringify(saved));\n    }\n  }\n}catch(e){ console.warn("Qwen local provider migration",e); }\n'''
        # imports may precede app startup; append migration before first createRoot/render area.
        pos=m.find("createRoot")
        if pos>=0:
            line=m.rfind("\n",0,pos)
            m=m[:line]+inject+m[line:]
        else:
            m+=inject
        main.write_text(m,encoding="utf-8")
