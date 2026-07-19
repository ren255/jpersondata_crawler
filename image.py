from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import threading
import requests

output_dir = Path("image")
output_dir.mkdir(exist_ok=True)

log_path = "download.log"
log_lock = threading.Lock()


def log(msg: str):
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    with log_lock:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


df = wikidata[wikidata["image_url"].notna()][["qid", "image_url"]].sample(40)
tasks = list(df.itertuples(index=False, name=None))

headers = {"User-Agent": "whoami/1.0 (bot@bot.bot)"}
session = requests.Session()
session.headers.update(headers)

MAX_WORKERS = 3
MAX_PASSES = 3


def download(task):
    qid, url = task
    filepath = output_dir / f"{qid}.jpg"
    try:
        resp = session.get(url, timeout=15)
        status = resp.status_code
        if status != 200:
            # ステータスコード + レスポンス本文の頭だけログに残す
            body_snippet = resp.text[:200].replace("\n", " ")
            log(f"FAIL qid={qid} status={status} url={url} body={body_snippet}")
            return (qid, url, f"HTTP {status}")
        resp.raise_for_status()
        filepath.write_bytes(resp.content)
        return (qid, url, None)
    except requests.exceptions.RequestException as e:
        log(f"FAIL qid={qid} exception={type(e).__name__} msg={e} url={url}")
        return (qid, url, str(e))
    except Exception as e:
        log(f"FAIL qid={qid} exception={type(e).__name__} msg={e} url={url}")
        return (qid, url, str(e))


def run_pass(task_list, pass_num):
    failed = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(download, t) for t in task_list]
        for i, fut in enumerate(as_completed(futures), 1):
            qid, url, err = fut.result()
            if err:
                failed.append((qid, url))
            if i % 10 == 0 or i == len(task_list):
                print(
                    f"[pass {pass_num}] {i}/{len(task_list)} 完了 (失敗 {len(failed)}件)"
                )
    return failed


from time import time

start = time()
log(f"=== 開始: 全{len(tasks)}件 ===")
remaining = tasks
for p in range(1, MAX_PASSES + 1):
    if not remaining:
        break
    print(f"=== pass {p}: {len(remaining)}件処理 ===")
    log(f"=== pass {p} 開始: {len(remaining)}件 ===")
    remaining = run_pass(remaining, p)
    log(f"=== pass {p} 終了: 失敗{len(remaining)}件 ===")

print(f"最終的に失敗したまま残った件数: {len(remaining)}")
log(f"=== 全処理終了: 最終失敗{len(remaining)}件 ===")
took = time() - start
print(f"{len(tasks) - len(remaining)} took {took}")
