# Reproduce el snapshot de la primera ejecución (2026-10-17) a partir de los datos leídos de Escalafy y Shopify.
# Se corre desde una carpeta que tenga narrative.json; queda como referencia del formato, no lo usa la tarea programada.
import json
K = ["spend","impressions","reach","clicks","link_clicks","landing_page_views","adds_to_cart","checkouts_initiated","purchases","video_plays","thruplays"]
rows = """52611570448264|US - VID Demo (V02)|60.13217|438|415|8|7|4|0|0|0|118|24
52611566930464|US - IMG Hook|20.23752|208|196|9|6|7|0|0|0|0|0
52611569096864|AR - VID Pack Dúo (V10)|19.68763|2752|2569|152|106|87|0|0|0|934|224
52611569551464|MX - VID Pack Dúo (V10)|18.89544|4864|4469|218|72|54|0|0|0|1713|368
52611570408464|CO - VID Pack Dúo (V10)|18.01485|4137|3703|298|276|225|1|0|0|1628|540
52611561197464|MX - IMG Hero|14.20357|657|566|17|13|12|1|0|0|0|0
52611567263464|AR - VID Demo (V02)|12.35394|3337|3017|137|159|117|0|0|0|797|285
52611566793064|CO - IMG Pack Dúo|11.79315|5291|4422|105|65|39|0|0|0|0|0
52611561196864|MX - IMG Hook|9.49946|462|444|14|8|11|0|0|0|0|0
52611566930264|US - IMG Duo Pack|7.55155|140|129|3|2|1|0|0|0|0|0
52611554302064|AR - IMG Hook|6.70746|966|876|20|17|12|0|0|0|0|0
52611554780664|AR - IMG Pack Dúo|5.70853|1577|1493|41|19|19|0|0|0|0|0
52611566792464|CO - IMG Hero|5.59439|1136|1071|10|7|5|0|0|0|0|0
52611566792864|CO - IMG Hook|4.76884|391|370|6|6|8|0|0|0|0|0
52611566930064|US - IMG Hero|4.36067|53|50|1|2|0|0|0|0|0|0
52611570448064|US - VID Duo Pack (V10)|3.36366|36|35|1|1|0|0|0|0|11|2
52611561197064|MX - IMG Pack Dúo|3.24850|450|288|8|6|5|0|0|0|0|0
52611520180064|AR - IMG Hero|1.45329|127|121|1|1|1|0|0|0|0|0
52611570408664|CO - VID Demo (V02)|0.33256|120|113|1|0|0|1|0|0|34|10
52611569551664|MX - VID Demo (V02)|0.02593|15|15|0|0|0|0|0|0|1|0"""
ads=[]
for r in rows.splitlines():
    p=r.split("|"); vals=[float(x) for x in p[2:]]
    m=dict(zip(K,[v if i==0 else int(v) for i,v in enumerate(vals)])); m["purchase_value"]=0
    ads.append({"id":p[0],"name":p[1],"market":p[1][:2],"format":"video" if "VID" in p[1] else "imagen","state":"paused","metrics":m})
camps={"52611520179664":("Ventas AR - Compra - Pixel tienda - Sep 2026",10000),"52611566792664":("Ventas CO - Compra - Pixel tienda - Sep 2026",10000),
       "52611561196664":("Ventas MX - Compra - Pixel tienda - Sep 2026",10000),"52611566930864":("Ventas US - Purchase - Pixel tienda - Sep 2026",15400)}
adsets={"52611520179864":"52611520179664","52611561197264":"52611561196664","52611566793264":"52611566792664","52611566930664":"52611566930864"}
objects=[{"level":"campaign","id":k,"name":v[0],"status":"PAUSED","state":"paused","budget":v[1],"budget_type":"daily","budget_currency":"ARS"} for k,v in camps.items()]
objects+=[{"level":"adset","id":k,"parent_id":v,"status":"CAMPAIGN_PAUSED","state":"paused"} for k,v in adsets.items()]
objects+=[{"level":"ad","id":a["id"],"name":a["name"],"status":"CAMPAIGN_PAUSED","state":"paused"} for a in ads]
objects+=[{"level":"ad","id":i,"name":n,"status":"CAMPAIGN_PAUSED","state":"paused"} for i,n in [("52611566930464x","")] if False]
daily_raw={"09-25":(6.93016,1938,15,9),"09-26":(31.18918,2277,31,28),"09-30":(25.25905,3372,55,37),"10-01":(40.76852,7116,201,137),"10-02":(33.27640,5334,90,77),
 "10-06":(20.07525,1991,34,31),"10-07":(5.92221,109,4,4),"10-10":(55.97717,4611,338,280),"10-11":(0,0,0,1),"10-14":(8.53516,409,5,3)}
from datetime import date,timedelta
daily=[]
d=date(2026,9,18)
while d<=date(2026,10,17):
    k=d.strftime("%m-%d"); s,i,lc,lpv=daily_raw.get(k,(0,0,0,0))
    daily.append({"date":d.isoformat(),"spend":s,"impressions":i,"link_clicks":lc,"landing_page_views":lpv}); d+=timedelta(days=1)
cur={"spend":227.93310,"impressions":27157,"reach":24362,"clicks":1050,"link_clicks":773,"landing_page_views":607,"video_plays":5236,"thruplays":1453,"adds_to_cart":3,"checkouts_initiated":0,"purchases":0,"purchase_value":0}
prev={"spend":82.50253,"impressions":23568,"reach":19446,"clicks":1212,"link_clicks":1289,"landing_page_views":None,"video_plays":7746,"thruplays":4441,"adds_to_cart":0,"checkouts_initiated":0,"purchases":0,"purchase_value":0}
snap=json.load(open("narrative.json"))
snap.update({"objects":objects,"ads":ads,"daily":daily,"totals":{"current":cur,"previous":prev}})
json.dump(snap,open("snapshot.json","w"),ensure_ascii=False,indent=2)
# market aggregation for narrative check
agg={}
for a in ads:
    g=agg.setdefault(a["market"],[0,0,0,0]); m=a["metrics"]; g[0]+=m["spend"]; g[1]+=m["impressions"]; g[2]+=m["link_clicks"]; g[3]+=m["landing_page_views"]
for k,(s,i,lc,lpv) in agg.items(): print(k, round(s,2), i, lc, lpv, "cpm",round(s/i*1000,2),"c/lpv",round(s/lpv,2) if lpv else None, "share",round(s/227.9331*100,1))
fmt={}
for a in ads:
    g=fmt.setdefault(a["format"],[0,0,0]); m=a["metrics"]; g[0]+=m["spend"]; g[1]+=m["landing_page_views"]; g[2]+=m["impressions"]
for k,(s,lpv,i) in fmt.items(): print(k, round(s,2), lpv, i, round(s/lpv,3))
print(sum(a["metrics"]["spend"] for a in ads))
