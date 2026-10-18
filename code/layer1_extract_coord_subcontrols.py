import pdfplumber,re,json
ID=re.compile(r'^\d-\d{1,2}-\d{1,2}-\d{1,2}$'); ANY=re.compile(r'^\d-\d{1,2}-\d{1,2}(?:-\d{1,2})?$')
rec=json.load(open('coord_records.json')); subs={}
with pdfplumber.open('ecc-en.pdf') as pdf:
    for pi,p in enumerate(pdf.pages):
        ws=[w for w in p.extract_words() if 50<w['top']<p.height-45]
        rt=sorted(r.bbox[1] for tb in p.find_tables() for r in tb.rows)
        sid=sorted([w for w in ws if ID.match(w['text'])],key=lambda w:(w['top'],w['x0']))
        anyid=sorted([w for w in ws if ANY.match(w['text']) and w['x0']<200],key=lambda w:w['top'])
        for w in sid:
            nxt=[v['top'] for v in anyid if v['top']>w['top']+3]
            rowb=[t for t in rt if t>w['top']+2]
            bot=min(nxt+rowb+[p.height-45])-1
            body=[v for v in ws if v['x0']>=w['x1']+1 and w['top']-2<=v['top']<bot and not ANY.match(v['text'])]
            body.sort(key=lambda v:(round(v['top']/3),v['x0']))
            txt=re.sub(r'\s+',' ',' '.join(v['text'] for v in body)).strip()
            if w['text'] not in subs or len(txt)>len(subs[w['text']]['text']): subs[w['text']]={'control_id':w['text'],'level':4,'page':pi+1,'text':txt}
allr=rec+list(subs.values()); allr.sort(key=lambda r:[int(x) for x in r['control_id'].split('-')])
json.dump(allr,open('coord_records_all.json','w'),indent=1,ensure_ascii=False)
print(len(allr),sum(r['level']==3 for r in allr),sum(r['level']==4 for r in allr))
for r in allr:
    if r['level']==4 and r['control_id'] in('1-5-3-1','1-10-4-1','2-5-3-4','5-1-3-4','5-1-3-10'): print(r['control_id'],'|',r['text'][:140])
