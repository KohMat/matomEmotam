# DEEP IMITATIVE MODELS FOR FLEXIBLE INFERENCE, PLANNING, AND CONTROL

Nicholas Rhinehart, Rowan McAllister, Sergey Levine

* [Published as a conference paper at ICLR 2020](https://openreview.net/pdf?id=Skl4mRNYDr)
* [Arxiv 1st Oct. 2019](https://arxiv.org/pdf/1810.06544.pdf)
* [github](https://github.com/nrhine1/deep_imitative_models)
* [site](https://sites.google.com/view/imitative-models)

## どんなもの？

自動運転のためのPath Planningを提案する。模倣学習(Imitation Learning)によってエキスパートの軌跡を模倣する確率モデル（Imitative Model）$$q(S \mid \phi)$$ を使い、観測$$\phi$$からゴールに到達するエキスパートのような経路計画$$s^*$$を、エキスパート軌跡との尤度とゴールとの尤度を最大化することで求める(Imitative Planning)。ゴールの尤度に有効な移動間領域を指定することで、potholesのようなものを避けるように計画する(Costed planning)ことも可能である。

![PathPlanning](./PathPlanning.png)

![imitaive_planning_to_goals](./imitaive_planning_to_goals.png)

![goalsettings](./goalsettings.png)

## 先行研究と比べてどこがすごい？何を解決したか？

* Imitation Planningという推論フレームワークを行うことで、柔軟にゴールへ到達することができる。
* 訓練時にゴールの設定を必要せず、エキスパートの軌跡との尤度を最大化することでネットワークを訓練する。
* 実行時に複雑なゴールの設定を行うことができる。今までのImitation Learning（IL)の方法は訓練時にゴールの設定を必要とする。またゴールの設定は簡単なものに限られる（右左折など）。
* モデルベース強化学習(MBRL)のような複雑な報酬関数の設計を必要としない。ゴールの尤度を設定する報酬関数の設計は必要。
* CARLA上で６つのILとMBRLの性能を上回った。
* ゴール設定にノイズが入った場合でもロバストである。

## 技術や手法の大事なことはどこ？

実行時にGradient ascentによって式(1)を最適化することでゴールに到達するエキスパートのような計画を計算する。実際には以下のAlgorithm 2で示すように潜在空間$$z$$を通して最適化計算を行う。

![imitative_plan](./imitative_plan.png)

ここで

* $$q$$ : エキスパートの軌跡を模倣する確率モデル$$q_{\theta}(S \mid \phi)$$ 
* $$f$$: 観測$$\phi$$および正規分布に従う潜在変数$$ Z \sim q_0 = \mathcal{N}(0, I)$$から計画$$S$$にワープする可逆かつ微分可能な関数 $$ S = f_{\theta}(Z; \phi) $$ （論文では関数$$f$$にR2P2を使う。）
* パラメータ$$\theta$$は、エキスパートの軌跡を使い$$q(S\mid\phi)$$を最大化することで求める。

> Nicholas Rhinehart, Kris M. Kitani, and Paul Vernaza. R2P2: A reparameterized pushforward policy for diverse, precise generative path forecasting. In European Conference on Computer Vision (ECCV), September 2018.
>
> 車両の経路を予測する論文である。計画Sは２次元座標x,yからなるwaypointで構成される。論文内で使われたネットワークのアーキテクチャは以下の図のように自己回帰的に動作する。 ネットワークは位置の平均ではなく、１,２サンプル前の位置との平均速度、位置の分散を出力する。
>
> ![deep_imitative_model](./deep_imitative_model.png)

ゴールの尤度関数設計は自由度が高く、ゴール内ならば１，ゴール外ならば０を返すという簡単な関数を尤度関数とすることができる。

![goal_likelihood](./goal_likelihood.png)

例えば以下のような尤度関数である。

* ゴールへ向かうルートとして与えられた各waypointの半径以内にいる場合は１，そうでない場合は０
* 移動可能領域をポリゴンで表現し、ポリゴン内ならば１、そうでない場合は０

その他にも、１，０のバイナリの代わりにゴール内のより良い場所を目指すようにガウシアン関数を用いたりできる。論文中にいくつかのゴール尤度関数が提案されている。

## どうやって有効だと検証した？

CARLAを使い以下を検証した。[結果](https://sites.google.com/view/imitative-models)を動画で見ることができる。

1. 最低限の報酬関数の設計とオフライン学習によって解釈可能なエキスパートのような計画を生成できるか？この手法が有効であるか？
2. 実際の車両の設定のもとでstate-of-the-artの性能を達成できるか？
3. 新しいタスクに対してどれだけ柔軟であるか？
4. ゴール設定へのロバスト性はどれだけあるか？

### 検証1  性能

様々なゴール尤度の設定のImitative PlanningをCALRA上で実行した。StaticおよびDynamicな環境のいずれも、いくつかの手法の性能を上回った。この結果からの質問1,2に対して肯定的な回答(affirmative answers)を示している。

![start_of_art_result](./start_of_art_result.png)

### 検証2  ゴールノイズに対するロバスト性

ゴールにノイズを混ぜた状況でナビゲーションするテストを行った。以下のいずれの場合も高い確率でナビゲーションを成功させることができた。このことから質問４に対する回答はYesである。

1. waypointsからなるゴールの半分を、大きく変動
2. ゴールを対向車線に設定

### 検証3  potholeの回避

potholeに対する回避実験を行った。Gaussian Final-State Mixtureおよび) Energy-based likelihoodを組み合わせたゴール尤度を使用することで、ランダムに設置されたpotholeをセンターラインに近づいたり、時には反対レーンに行くなどして避けることができた。

### 検証4  経路計画の信頼度推定

モデルが陽に計画の尤度を計算することができるので、計画が安全であるか安全でないかの分類問題の実験を行った。エキスパートが実際に行った良好なwaypointとオフロードである悪いwaypointが含まれる1650のテストケースに対してリコール97.5％、精度90.2%を示している。

また各検証データのエキスパートの最終位置に対する経路計画を行った。そして、あるウェイポイントが計算した計画の信頼区間に含まれる確率、すなわち信頼度を計算した。信頼区間は、計画の基準の平均値から1標準偏差を引いた値を計画の基準の閾値とした区間である。

1. エキスパートが時間Tに実際に到着したウェイポイントに対して89.4%の信頼度を示した
2. 提供されたルートに沿って20m進んだ先のウェイポイントに対して73.8%の信頼度を示した
3. 2)のウェイポイントから2.5mずれたウェイポイントに対して2.5%の信頼度を示した

この結果から、有効なウェイポイントを正しく判定する傾向があることがわかる。

### 検証5(課題) 信号のノイズに対するロバスト性

20％の確率で緑を赤に、赤を緑に変更するノイズを加えた状態で実験を行った。概ね成功しているものの、赤信号に対してより違反を行うという傾向が見られた。また交差点付近で停止と発進を繰り返し行う挙動が見られた。ノイズを加えた状態で訓練することによりよりロバストになる可能性がある。

![traffic_light_noise](./traffic_light_noise.png)

## 課題は？議論はある？

ゴールノイズに対する実験で、decoy waypointが交差点内の有効な場所ではあるが、目的地へ向かう方向ではない場所に設定されたときに、プランナが一時的に最適なルートを生成できないことがある。

観測のノイズおよび分布外の観測に対するロバスト性に対していくつかの課題がある。観測ノイズに関しては、例えば提案モデルは現在の観測しか使っていないが、ベイジアンフィルタリングを使うことで観測ノイズを軽減できるかもしれない。しかしながら高次元のフィルタリングは多くの場合手に負えないので、ディープラーニングをつかった近似ベイジアンフィルタリングを行う必要がある。分布外の観測に対しては、Deep Ensemble Networkを使う方法が考えられる。

> Balaji Lakshminarayanan, Alexander Pritzel, and Charles Blundell. Simple and scalable predictive uncertainty estimation using deep ensembles. In Neural Information Processing Systems (NeurIPS), pp. 6402–6413, 2017.

ゴール内の尤度とエキスパートの尤度のバランスはどうしたらいいだろうか？

## 次に読むべき論文は？

[A. Filos, P. Tigas, R. McAllister, N. Rhinehart, S. Levine, and Y. Gal, “Can autonomous vehicles identify, recover from, and adapt to distribution shifts?” arXiv preprint arXiv:2006.14911, 2020.](../Can autonomous vehicles identify, recover from, and adapt to distribution shifts/summary.md)

[N. Rhinehart, R. McAllister, K. Kitani, and S. Levine, “PRECOG: prediction conditioned on goals in visual multi-agent settings,” in Proceedings of the IEEE International Conference on Computer Vision, 2019, pp. 2821–2830.](../PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings/summary.md)