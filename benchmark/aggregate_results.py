from pathlib import Path
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
rows=[]
def add(ver,name,rmse,std=np.nan,n=12,note=''):
    rows.append(dict(version=ver,representative_model=name,train_devices=n,rmse_25C=float(rmse),std=float(std) if pd.notna(std) else np.nan,note=note))

# v0.1
p=ROOT/'versions/v0.1/results/mvp_benchmark.csv'
if p.exists():
    d=pd.read_csv(p); q=d[d.model=='source_prior']; add('v0.1','frozen Hartono prior + GP',q.rmse.mean(),q.rmse.std(),int(q.train_devices.mode().iloc[0]),'exact historical predictor; rerun at N=12')
# v0.2
p=ROOT/'versions/v0.2/results/benchmark_v02.csv'
if p.exists():
    d=pd.read_csv(p); q=d[(d.model=='adaptive_multisource')&(d.train_devices==12)]; add('v0.2','adaptive source prior + GP',q.rmse.mean(),q.rmse.std(),12,'quick run uses available v0.2 seeds')
# v0.3
p=ROOT/'versions/v0.3/results/source_usefulness_v03.csv'
if p.exists():
    d=pd.read_csv(p); q=d[(d.model=='full_source_graph')&(d.train_devices==12)]; add('v0.3','full source-factor graph',q.rmse.mean(),q.rmse.std(),12,'diagnostic-era predictor')
# v0.4: auditor has two candidate-role audits; report average to avoid test-set cherry-picking.
p=ROOT/'versions/v0.4/results/automatic_source_auditor_v04.csv'
if p.exists():
    d=pd.read_csv(p); q=d[d.train_devices==12]; add('v0.4','automatic source auditor',q.selected_rmse.mean(),q.selected_rmse.std(),12,'mean across Hartono-as-C and Chakar-as-C audits; not a single final predictor')
# v0.5
p=ROOT/'versions/v0.5/results/safe_adaptive_fusion_v05.csv'
if p.exists():
    d=pd.read_csv(p); q=d[d.train_devices==12]; add('v0.5','safe path-MKL fusion',q.adaptive_fusion_rmse_25C.mean(),q.adaptive_fusion_rmse_25C.std(),12,'directional transfer-CV safety blend')
# v0.6
p=ROOT/'versions/v0.6/results/adaptive_granularity_v06.csv'
if p.exists():
    d=pd.read_csv(p); q=d[(d.train_devices==12)&(d.family=='adaptive_granularity')]; add('v0.6','adaptive granularity',q.rmse.mean(),q.rmse.std(),12,'coarse-to-fine context alignment')
# v0.7
p=ROOT/'versions/v0.7/results/optional_diffraction_v07.csv'
if p.exists():
    d=pd.read_csv(p); q=d[d.model=='v07_optional_diffraction']; add('v0.7','optional diffraction expert',q.rmse_25C.mean(),q.rmse_25C.std(),12,'no diffraction source present: must reduce to v0.6')
# v0.8
p=ROOT/'versions/v0.8/results/stage_shared_specific_v08.csv'
if p.exists():
    d=pd.read_csv(p); q=d[(d.train_devices==12)&(d.model=='v08_stage_shared_specific')]; add('v0.8','shared/private stage experts',q.rmse_25C.mean(),q.rmse_25C.std(),12,'prototype stage model; local gains but not globally best')

out=pd.DataFrame(rows)
out['rank']=out.rmse_25C.rank(method='min').astype(int)
base=out.loc[out.version=='v0.1','rmse_25C']
if len(base): out['improvement_vs_v01_pct']=(float(base.iloc[0])-out.rmse_25C)/float(base.iloc[0])*100
else: out['improvement_vs_v01_pct']=np.nan
(ROOT/'results/tables').mkdir(parents=True,exist_ok=True)
out.to_csv(ROOT/'results/tables/version_comparison.csv',index=False)
md=['# v0.1–v0.8 representative comparison','', '> Important: this table is an evolution audit, not a perfectly controlled leaderboard. v0.4 is an auditor rather than one predictor; v0.7 intentionally equals v0.6 when diffraction data are missing. All entries use the fully held-out 25 °C domain and N=12 where the historical version permits it.','',out.to_markdown(index=False,floatfmt='.4f'),'']
(ROOT/'results/VERSION_COMPARISON.md').write_text('\n'.join(md),encoding='utf-8')

fig,ax=plt.subplots(figsize=(10,5.5))
ax.bar(out.version,out.rmse_25C,yerr=out['std'].fillna(0),capsize=4)
ax.set_ylabel('25 °C hold-out RMSE')
ax.set_xlabel('Model version')
ax.set_title('PSC multi-source model evolution (representative N=12 audit)')
ax.grid(axis='y',alpha=.25)
for i,r in out.iterrows(): ax.text(i,r.rmse_25C+0.004,f"{r.rmse_25C:.3f}",ha='center',fontsize=8)
fig.tight_layout(); (ROOT/'results/figures').mkdir(parents=True,exist_ok=True); fig.savefig(ROOT/'results/figures/version_rmse_comparison.png',dpi=180); plt.close(fig)
print(out.to_string(index=False))
