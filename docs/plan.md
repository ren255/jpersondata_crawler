occupations          54322
birth_places           976
alma_maters          12787
positions_held        5256
genres                 743
death_places            66
death_causes           112
death_manners           29
fathers                 84
mothers                 20
spouses                757
siblings              1793
children              2735
awards                3817
parties                797
notable_works         1328
military_branches       19
military_ranks          40
main_columns = [
    "qid",  # 236k
    "kanji",  # 236k
    "hiragana",  # 213k
    "description",  # 181k
    "gender",  # 223k
    "birth_year",  # 200k
    "death_year",  # 65k
    "age",  # 197k
    "death_age",  # 63k
    "label",  # 236k
    "name_en",  # 226k
    "is_japanese_name", # 236k
    # Career/Attributes
    "occupations",  # 210k
    "birth_places",  # 137k
    "alma_maters",  # 97k
    "positions_held",  # 16k
    "genres",  # 12k
    "death_places",  # 9.2k
    # physical
    "height_cm",  # 28k
    "weight_kg",  # 16k
    "bmi",  # 16k
    "death_causes",  # 5.8k
    "death_manners",  # 6.7k
    # family
    "fathers",  # 8.9k
    "mothers",  # 2.7k
    "spouses",  # 6.8k
    "siblings",  # 5.4k
    "children",  # 7.1k
    # others
    "awards",  # 17k
    "parties",  # 4.8k
    "notable_works",  # 3.5k
    "military_branches",  # 3.1k
    "military_ranks",  # 3.0k
    # url
    "wiki_url",  # 236k
    "image_url",  # 35k
]
common_columns = [
    "qid",  # 236k
    "kanji",  # 232k
    "hiragana",  # 213k
    "gender",  # 223k
    "birth_year",  # 200k
    "death_year",  # 65k
    "age",  # 197k
    "death_age",  # 63k
    "description",  # 181k
    "occupations",  # 210k
    "birth_places",  # 137k
    "alma_maters",  # 97k
    "height_cm",  # 28k
    "weight_kg",  # 16k
    "awards",  # 17k
    "is_japanese_name", # 236k
]



qid	kanji	hiragana	gender	description	occupations	birth_places	alma_maters	awards
count	236506	231730	213118	222835	181018	210378	137358	97175	16624
unique	231116	218919	185239	9	64264	22491	6186	13921	3350
top	Q11531057	松本 幸四郎	やまもと ひろし	男性	日本のサッカー選手	俳優	東京都	東京大学	勲二等瑞宝章
freq	14	14	24	165389	5873	9904	21627	11453	980


これから以下ををpy persentで一つの.py書きなさい。実行するな。csvファイルは上げない。
コメント、plt内すべてを英語でかけ。

-!pip install
-読み込む。
-"|"区切りを読むための関数を定義/処理
-ワードクラウド(下の名前だけ1文字ごと分割): 4 * 4. 上2つを女 した2つを男。それぞれの性別の中で上を漢字したをひらがな。横は 4つbirth yearごとに。 pd.qcut(subset, q=4). is_japanese_name=tureのみ使え。
- ワードクラウド(分割なし下の名前をそのまま使え。): 4 * 4. 上2つを女 した2つを男。それぞれの性別の中で上を漢字したをひらがな。横は 4つbirth yearごとに。 pd.qcut(subset, q=4). is_japanese_name=tureのみ使え。
- ワードクラウド: 男女左右, 職業を。 1*2
- ワードクラウド: 男女左右, positions_heldを。 1*2
-人口ピラミッド。
-グラフ: 職業 * 性別を一つの丸としてx軸を 平均年齢、yを平均 BMI. 左右で男女分ける
-グラフ: 職業 * 性別を一つの丸としてx軸を 平均身長、yを平均 体重. 左右で男女分ける
-上を1800年以降で5年bin/したを1800前で25年bin。左右を男女で分ける。2 *2 の積立グラフ。   それぞれで100%としてtop10 の職業だけラベル残りをその他として割合推移を示す。
-出身校 * 職業 で10 * 10 のマトリックス。左右男女。 logで一マスの最大と最小の人数を男女それぞれprint.
