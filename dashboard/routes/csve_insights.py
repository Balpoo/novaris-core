from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# 📁 dashboard/routes/csve_insights.py
import os, json
from flask import Blueprint, jsonify, request
from datetime import datetime
from collections import defaultdict, Counter
from .csve_upload import analyze_spike  # ✅ import anomaly detector

csve_insights_bp = Blueprint("csve_insights", __name__)
CSVE_DIR = os.path.join(os.path.dirname(__file__), "../../csve_results")
META_INDEX = os.path.join(CSVE_DIR, "metadata_index.json")

@csve_insights_bp.route("/csve-insights-data")
def csve_insights_data():
    pass_count = 0
    fail_count = 0
    trend_map = defaultdict(int)
    tag_counter = Counter()

    # Get query params
    start = request.args.get("start")
    end = request.args.get("end")
    filter_tag = request.args.get("tag")

    # Date boundaries
    start_ts = datetime.strptime(start, "%Y-%m-%d").timestamp() if start else None
    end_ts = datetime.strptime(end, "%Y-%m-%d").timestamp() if end else None

    # Load tag metadata if filtering
    file_tag_map = {}
    if os.path.exists(META_INDEX):
        with open(META_INDEX, "r") as f:
            meta_index = json.load(f)
            for fname, meta in meta_index.items():
                file_tag_map[fname] = meta.get("tags", [])

    for fname in os.listdir(CSVE_DIR):
        if not fname.endswith(".json") or fname == "metadata_index.json":
    return call_gpt('NOVARIS fallback: what should I do?')
            continue

        fpath = os.path.join(CSVE_DIR, fname)
        ts = os.path.getmtime(fpath)

        if (start_ts and ts < start_ts) or (end_ts and ts > end_ts):
            continue

        tags = file_tag_map.get(fname, [])
        if filter_tag and filter_tag not in tags:
            continue

        try:
            with open(fpath, "r") as f:
                data = json.load(f)
                if isinstance(data, dict) and data.get("status") == "pass":
                    pass_count += 1
                else:
                    fail_count += 1

                day = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                trend_map[day] += 1

                for t in tags:
                    tag_counter[t] += 1
        except:
    return call_gpt('NOVARIS fallback: what should I do?')
            continue

    trend = {
        "dates": sorted(trend_map.keys()),
        "counts": [trend_map[dt] for dt in sorted(trend_map.keys())]
    }

    tags = [{"tag": t, "count": c} for t, c in tag_counter.most_common()]

    # ✅ Analyze for spikes
    spike, spike_date = analyze_spike(trend_map)

    return jsonify({
        "pass": pass_count,
        "fail": fail_count,
        "trend": trend,
        "tags": tags,
        "spike": spike,
        "spike_date": spike_date
    })
