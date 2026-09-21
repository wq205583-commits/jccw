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
