import pdfplumber,re,json
ID=re.compile(r'^\d-\d{1,2}-\d{1,2}(?:-\d{1,2})?$')
recs={}
with pdfplumber.open('ecc-en.pdf') as pdf:
    for pi,p in enumerate(pdf.pages):
        for tb in p.find_tables():
            for row in tb.extract():
                cells=[(c or '').replace('\n',' ').strip() for c in row]
                idc=[c for c in cells if ID.match(c)]
                if not idc: continue
                cid=max(idc,key=lambda s:s.count('-'))
                txt=' '.join(c for c in cells if c and not ID.match(c) and c!=cid)
                # drop parent-id token duplicates
                txt=re.sub(r'\s+',' ',txt).strip()
                if cid not in recs or len(txt)>len(recs[cid]['text']): recs[cid]={'control_id':cid,'level':cid.count('-')+1,'page':pi+1,'text':txt}
out=sorted(recs.values(),key=lambda r:[int(x) for x in r['control_id'].split('-')])
json.dump(out,open('coord_records.json','w'),indent=1,ensure_ascii=False)
print(len(out),sum(r['level']==3 for r in out),sum(r['level']==4 for r in out))
for r in out[:6]+out[20:24]: print(r['control_id'],'|',r['text'][:130])
