# PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings

[Nicholas Rhinehart](https://arxiv.org/search/cs?searchtype=author&query=Rhinehart%2C+N), [Rowan McAllister](https://arxiv.org/search/cs?searchtype=author&query=McAllister%2C+R), [Kris Kitani](https://arxiv.org/search/cs?searchtype=author&query=Kitani%2C+K), [Sergey Levine](https://arxiv.org/search/cs?searchtype=author&query=Levine%2C+S)

* [ICCV 2019](https://openaccess.thecvf.com/content_ICCV_2019/html/Rhinehart_PRECOG_PREdiction_Conditioned_on_Goals_in_Visual_Multi-Agent_Settings_ICCV_2019_paper.html)
* [Arxiv 30 Sep 2019](https://arxiv.org/abs/1905.01296)　論文には多くの視覚的な結果がある
* [site](https://sites.google.com/view/precog)
* [github](https://github.com/nrhine1/precog)

## どんなもの？

可変数のエージェントの確率予測モデルを提案する。

可変数のエージェント間で将来の相互作用の確率予測モデルを提案する。

joint state(各物体の状態をひとつにまとめた状態)

すべてのエージェントのjoint-stateを予測するfactorized flow based生成モデルを提案する

エージェント間の尤もらしい将来の相互作用を確率的に説明する。

エージェントの決断の不確かさを捉えるために潜在変数を使う。

各エージェントの決断をモデル化するためにfactorized潜在変数を使う。

複数のエージェントのダイナミクスが結びついている場合でも

マルチエージェントと時間にまたがる分解により、任意の時間における任意エージェントの決定を独立に変えたときの効果を調べることができる。



![EmbeddedImage](./EmbeddedImage.gif)

## 先行研究と比べてどこがすごい？何を解決したか？

### state-of-artなマルチエージェントの予測

Estimating Social-forecast Probabilities(ESP)を提案した。ESPはVAEやGANと異なり厳密な尤度推定を行う。ESPが現実(nuScenes)およびシミュレーション上(CALRA)で３つのstate-of-artの方法の性能を上回ることを示した。またESPがエージェント間の相互作用を考慮することを示した。

### ゴール条件付きマルチエージェント予測

エージェントが向かうべきゴールを条件に予測を行う初の生成型マルチエージェント予測法PRECOG(PREdition Conditioned On Goal)を提案した。エージェントに新しいゴールを条件付け、マルチエージェント環境でのImitative Planningを行うことで、予測性能が改善されることを示した。マルチエージェント環境でのImitative PlanningはDeep Imitative Planning([arxiv](https://arxiv.org/pdf/1810.06544.pdf), [link](../DEEP IMITATIVE MODELS FOR FLEXIBLE INFERENCE, PLANNING, AND CONTROL/summary.md))を一般化したものである。

## 技術や手法の核はどこ？

複数のエージェント（車両）が時間$$T$$に渡って相互作用する連続雨間、離散時間、POMDPプロセスを扱う。時刻$$t$$におけるすべてのエージェントの状態を$$S_t \in \mathbb{R}^{A \times D}$$とする。Aはエージェントの個数、D=2である。$$S_t^a$$は時刻$$t$$におけるエージェント$$a$$の2次元位置$$x,y$$を示す。$$t=0$$は現在時刻、$$a$$が$$r$$もしくは$$1$$の場合は自車両、$$h$$もしくは$$2\sim$$の場合は他車両、人を示す。添字を省略した$$S$$は$$S_{1:T}^{1:A}$$を示す。すなわちすべてのエージェントの予測である。$$\chi$$はLIDARや道路などの高次元の観測である。実験した例ではLIDARを用いた観測$$\chi= \mathbb{R}^{200 \times 200 \times 2}$$を使った。



## どうやって有効だと検証した？

### ESPの検証

**Didactic Example**：簡素な交差点でのナビゲーションを使い予測性能を検証した。交差点には人間（オレンジ）およびロボット（青）が存在する。人間は常に4ステップ直進し、その後直進もしくは左折のどちらかの行動を行う（50％の確率）。ロボットは直視しようと試みるが、人間が左折した場合には譲歩する。このナビゲーションシミュレーションを行い、データセットを作成し、ESPおよびベースラインR2P2-MAの訓練を行った。学習したそれぞれの方法の予測結果を次に示す。R2P2-MAはエージェント間の相互作用を考慮していないので、50％の確率で人間とロボットがぶつかる予測を行った。これに対してESPは人間の決定に対して反応していることを示している。

![didactic_example](./didactic_example.png)

**CARLAおよびnuScenes**：CALRAおよびnuScenesから10個のデータセットを作成し、予測性能を検証した。すべてのデータセットでESPの性能がベースラインを上回った。ESP, no LIDARは観測からLIDARを除いたESPである。ESP, RoadはnuScenesの道路領域をバイナリマスクで表現した入力を追加したESPである。ESP, flexは、可変数のエージェントに対応するESPである。

![esp_performance](./esp_performance.png)

### PRECOGの検証

CALRAおよびnuScenesを使い、PRECOGの予測性能を検証した。Planingを行うエージェントは自車両のみとした。各データの最後の位置をゴールとして設定した。ゴールの尤度は正規分布を用いた。[DESIRE](https://arxiv.org/abs/1704.04394)およびESPと比較した結果は次のとおりである。ゴールを設定して予測することにより、自車両$$\hat{m}_K^1$$だけでなく、その他すべての予測が向上することを示している。エージェントは近い順からソーティングされており、一番近い車両$$\hat{m}_K^2$$が最も影響を受けていることも示している。

![precog_result](./precog_result.png)

## 課題は？議論はある？

将来の方向としては、自車両だけでなく他車両のゴールを条件付けた予測がある。

個人的に

* Didactic Exampleで自車両は人間が左折したとき、人間もしくはロボットが交差点前に止まるパターンを検証してみたい。
* 上に書かれているとおり、PRECOGの検証で、自車両だけでなく、観測範囲内の道路の構造上到達しうる点も加えて検証をしてみたい

## 次に読むべき論文は？

未定
