import json,os,re,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));DIR=os.path.join(ROOT,"projects");os.makedirs(DIR,exist_ok=True)
def safe(n):return re.sub(r"[^a-zA-Z0-9_\-\u4e00-\u9fff]","_",n)[:80] or "project"
def save(name,data):
 p=os.path.join(DIR,safe(name)+".json");data["saved_at"]=int(time.time());open(p,"w",encoding="utf-8").write(json.dumps(data,ensure_ascii=False,indent=2));return os.path.basename(p)
def load(name):return json.load(open(os.path.join(DIR,safe(name)+".json"),encoding="utf-8"))
def list_projects():return sorted([x for x in os.listdir(DIR) if x.endswith(".json")])
