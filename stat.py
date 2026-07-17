#%%
population = pd.read_csv("source/FEH_00200524_260717083209.csv", encoding="Shift-JIS")
population = population[["year", "age", "man", "woman"]]

import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import matplotlib as mpl

plt.rcParams["font.family"] = "Noto Sans CJK JP"
mpl.rcParams["axes.unicode_minus"] = False  # マイナス記号の文字化け防止

# --- 1. wikidataの生存者(推定)を年齢×性別で集計し、割合化 ---
alive = wikidata[
    wikidata["death_year"].isna()
    & wikidata["birth_year"].notna()
    & (wikidata["current_age"] < 120)
]

wiki_dist = {}
for g, label in [("男性", "wiki_man"), ("女性", "wiki_woman")]:
    s = alive.loc[alive["gender"] == g, "current_age"]
    counts = s.value_counts().sort_index()
    counts = counts.reindex(range(0, 120), fill_value=0)
    wiki_dist[label] = counts / counts.sum()

# --- 2. populationを最新年に絞り、age列をクリーニングして割合化 ---
pop = population.copy()
latest_year = pop["year"].max()
pop = pop[pop["year"] == latest_year].copy()


def clean_age(a):
    a = str(a)
    if "以上" in a:
        return 100
    m = re.search(r"\d+", a)
    return int(m.group()) if m else np.nan


pop["age_num"] = pop["age"].apply(clean_age)
pop = pop.dropna(subset=["age_num"])
pop = pop[pop["age_num"] <= 119]  # 総数行など除外

for col in ["man", "woman"]:
    pop[col] = pop[col].astype(str).str.replace(",", "", regex=False).astype(float)

pop_dist = {}
for col, label in [("man", "stat_man"), ("woman", "stat_woman")]:
    s = pop.groupby("age_num")[col].sum().sort_index()
    s = s.reindex(range(0, 120), fill_value=0)
    pop_dist[label] = s / s.sum()

# --- 3. 4本の滑らかな曲線をプロット ---
ages = np.arange(0, 120)

fig, ax = plt.subplots(figsize=(10, 6))

series = {
    "wiki_man": ("Wikidata 男性", "tab:blue", "-"),
    "wiki_woman": ("Wikidata 女性", "tab:red", "-"),
    "stat_man": (f"人口統計 男性 ({latest_year}年)", "tab:blue", "--"),
    "stat_woman": (f"人口統計 女性 ({latest_year}年)", "tab:red", "--"),
}

for key, (label, color, ls) in series.items():
    y = wiki_dist[key] if key.startswith("wiki") else pop_dist[key]
    y_smooth = gaussian_filter1d(y.values, sigma=2)
    ax.plot(ages, y_smooth, label=label, color=color, linestyle=ls)

ax.set_xlabel("年齢")
ax.set_ylabel("割合")
ax.set_title("年齢分布: Wikidata（生存者）vs 日本人口統計")
ax.legend()
plt.tight_layout()
plt.show()


#%%
has_birth = wikidata["birth_year"].notna()
has_death = wikidata["death_year"].notna()

cross_tab = pd.crosstab(
    index=has_birth.rename("Birth Year Exist"),
    columns=has_death.rename("Death Year Exist"),
    margins=True,  
)

print(f"生死不明. 120歳以上: {wikidata[wikidata['death_age'].isna() & (wikidata['current_age'] >= 120)].shape[0]}, 120歳未満: {wikidata[wikidata['death_age'].isna() & (wikidata['current_age'] < 120)].shape[0]}")
cross_tab