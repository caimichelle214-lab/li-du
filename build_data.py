#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build assets/data.js from the three CSV files."""
import csv, json, math, re, statistics, collections, os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, '李杜')

def read(name):
    with open(os.path.join(SRC, name), encoding='utf-8-sig') as fh:
        return list(csv.reader(fh))

def build_poems(rows):
    poems, index = [], {}
    for title, line, pid, lidx in rows:
        pid, lidx = int(pid), int(lidx)
        if pid not in index:
            index[pid] = len(poems)
            poems.append({'id': pid, 't': title, 'lines': []})
        poems[index[pid]]['lines'].append((lidx, line))
    for p in poems:
        p['lines'].sort(key=lambda x: x[0])
        p['lines'] = [s for _, s in p['lines']]
        p['n'] = len(p['lines'])
    return poems, index

L = read('李白.csv')
D = read('杜甫.csv')
P = read('李白-杜甫.csv')

lp, lindex = build_poems(L)
dp, dindex = build_poems(D)

# rank = position when poems are ordered by their 全唐诗 poem id
lrank = {p['id']: i for i, p in enumerate(sorted(lp, key=lambda x: x['id']))}
drank = {p['id']: i for i, p in enumerate(sorted(dp, key=lambda x: x['id']))}

pairs = []
bad = 0
for r in P:
    sim = int(r[6])
    lid, li, did, di = int(r[7]), int(r[8]), int(r[9]), int(r[10])
    if lid not in lindex or did not in dindex:
        bad += 1
        continue
    if lp[lindex[lid]]['lines'][li] != r[2] or dp[dindex[did]]['lines'][di] != r[5]:
        bad += 1
        continue
    pairs.append([sim, lindex[lid], li, dindex[did], di])
print('pairs', len(pairs), 'skipped', bad)

sims = [p[0] for p in pairs]
meta = {
    'lPoems': len(lp), 'lLines': len(L),
    'dPoems': len(dp), 'dLines': len(D),
    'pairs': len(pairs),
    'lPoemsMatched': len({p[1] for p in pairs}),
    'dPoemsMatched': len({p[3] for p in pairs}),
    'simMin': min(sims), 'simMax': max(sims),
    'simMean': round(statistics.mean(sims) / 10000, 4),
    'simMedian': statistics.median(sims) / 10000,
    'sim9000': sum(1 for s in sims if s >= 9000),
    'sim8000': sum(1 for s in sims if s >= 8000),
    'sim9500': sum(1 for s in sims if s >= 9500),
}

# ---- similarity histogram, 30 bins of 100 (7000..9999) ----
hist = [0] * 30
for s in sims:
    hist[min(29, (s - 7000) // 100)] += 1

# ---- per-poem degree / strength ----
deg_l = collections.Counter()
deg_d = collections.Counter()
best_l = collections.defaultdict(int)
best_d = collections.defaultdict(int)
for s, li, lli, di, dli in pairs:
    deg_l[li] += 1
    deg_d[di] += 1
    best_l[li] = max(best_l[li], s)
    best_d[di] = max(best_d[di], s)

# ---- shared bigrams inside matched line pairs ----
CJK = re.compile(r'[\u4e00-\u9fff]')
def grams(s):
    s = ''.join(ch for ch in s if CJK.match(ch))
    return {s[i:i+2] for i in range(len(s) - 1)}
gram = collections.defaultdict(lambda: [0, 0])
for s, li, lli, di, dli in pairs:
    a = grams(lp[li]['lines'][lli])
    b = grams(dp[di]['lines'][dli])
    for g in a & b:
        gram[g][0] += 1
        gram[g][1] += s
top_grams = sorted(gram.items(), key=lambda kv: (-kv[1][0], -kv[1][1] / kv[1][0]))[:60]
bigrams = [[g, c, round(t / c / 10000, 3)] for g, (c, t) in top_grams]

# ---- bipartite network: strongest poem-level links ----
link = collections.Counter()
link_sim = collections.defaultdict(list)
for s, li, lli, di, dli in pairs:
    link[(li, di)] += 1
    link_sim[(li, di)].append(s)

top_l = deg_l.most_common(26)
top_d = deg_d.most_common(26)
lset = {i for i, _ in top_l}
dset = {i for i, _ in top_d}
edges = []
for (li, di), c in link.items():
    if li in lset and di in dset:
        ss = link_sim[(li, di)]
        edges.append([li, di, c, round(max(ss) / 10000, 3)])
edges.sort(key=lambda e: -e[2])

network = {
    'l': [[i, lp[i]['t'], deg_l[i]] for i, _ in top_l],
    'd': [[i, dp[i]['t'], deg_d[i]] for i, _ in top_d],
    'e': edges,
}

# ---- poem-level aggregated links for the 序号 map ----
plinks = []
for (li, di), c in link.items():
    plinks.append([lrank[lp[li]['id']], drank[dp[di]['id']], c, max(link_sim[(li, di)])])
pairs_compact = [[s / 10000.0, lrank[lp[li]['id']], drank[dp[di]['id']]] for s, li, lli, di, dli in pairs]

data = {
    'meta': meta,
    'hist': hist,
    'lp': [{'id': p['id'], 't': p['t'], 'n': p['n'], 'lines': p['lines'],
            'm': deg_l[i], 'b': round(best_l[i] / 10000, 3)} for i, p in enumerate(lp)],
    'dp': [{'id': p['id'], 't': p['t'], 'n': p['n'], 'lines': p['lines'],
            'm': deg_d[i], 'b': round(best_d[i] / 10000, 3)} for i, p in enumerate(dp)],
    'pairs': pairs,
    'bigrams': bigrams,
    'network': network,
}

out = os.path.join(BASE, 'assets', 'data.js')
with open(out, 'w', encoding='utf-8') as fh:
    fh.write('window.LD=')
    json.dump(data, fh, ensure_ascii=False, separators=(',', ':'))
    fh.write(';\n')
print('wrote', out, round(os.path.getsize(out) / 1024 / 1024, 2), 'MB')
print(json.dumps(meta, ensure_ascii=False, indent=1))
print('bigrams', bigrams[:12])
print('network', len(network['l']), len(network['d']), len(edges))
