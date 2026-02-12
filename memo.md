# 目的
1日の終わりに下記記載の内容を元にファイルを整形。

参考jsonの形式は以下の通り
/Users/310tea/Documents/学習アウトプット/normalized_data/normalized_data_2026-02-02_to_2026-02-08.json

移動先は以下の通り
/Users/310tea/Documents/学習アウトプット/daily


 # 含めるべきセクション
 - 日付
 - Statsセクション (休憩時間、運動時間、純粋な学習時間合計、DayMode、Deep score)
 - 1日の最初に計画したTop1とDone条件を満たせているかを定量面と定性面から分析したフィードバックを記載するセクション
 - 1日の休憩時間や運動時間なども考慮して最終的な純粋な学習時間の計測を行い、計画時間と実際時間との乖離を定量面と定性面から分析したフィードバックを記載するセクション
- Worked、Slipped、Insights、Study Strategy for Next Dayセクションに記載されているテキストを記載するセクション
 - その日の学習内容を■ Technical Learningsというセクションを作成して記載する

 # フォーマット
- markdown形式

 # 構成
 - 日付 YYYY-MM-DD形式
 -  Statsセクション
 -  Workedセクション
 -  Slippedセクション
 -  Insightsセクション
 -  StatsセクションのTop1 と Done条件を満たせているかを定量面と定性面から分析したフィードバックを記載するセクション
-  Study Strategy for Next Dayセクション
 -  Technical Learningsセクション 

 # 要件
 - Statsセクションの休憩時間、運動時間、純粋な学習時間合計などは指定されている該当のsessionsから算出を行う
 - 以下の週末のに使用する分析プロンプトを参考に、精度が向上するように整形する
/Users/310tea/Documents/学習アウトプット/prompts/analysis_prompt_v2.md
 - 上記の#構成が現在最新なので、それに沿って整形する
 - 最終的に週末分析用のプロンプトもアップデートを行う