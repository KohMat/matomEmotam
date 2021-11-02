# [日本語まとめ] Deep Structured Reactive Planning

[Jerry Liu](https://arxiv.org/search/cs?searchtype=author&query=Liu%2C+J), [Wenyuan Zeng](https://arxiv.org/search/cs?searchtype=author&query=Zeng%2C+W), [Raquel Urtasun](https://arxiv.org/search/cs?searchtype=author&query=Urtasun%2C+R), [Ersin Yumer](https://arxiv.org/search/cs?searchtype=author&query=Yumer%2C+E)

* [arxiv](https://arxiv.org/pdf/2101.06832.pdf)

## どんなもの？

Reactive planningは予測と計画を同時に行う経路計画法である。Reactive planningは自動運転車の行動が他の車の行動に及ぼす影響を考慮することができる。次のシナリオは一般的な運転でもよく遭遇するようなシナリオであるが、速やかに走行するためには他の車の行動の理解が求められる。

* 自動運転車が他の車に道を譲った場合、他の車がその道を先に走行する
* 自動運転車が道を譲らず走行した場合、他の車はその道を譲る

しかし予測を元に計画を行うシステム（non-reactive planner）はこのようなシナリオに対して快適な走行を行うことはできない。自動運転車の行動が他の車に及ぼす影響を無視しているからである。Non-reactive plannerは従来の自動運転に多く採用されている。大抵の場合、non-reactive plannerは目的の車線が利用可能になるまで待機する選択を行う。しかしながら、自動運転車の後ろに車がいる場合、待つという行動は交通の妨げになる。したがって単純に待つという戦略は理にかなっている運転とは言えない。自動運転車だけでなく他の車にとっても安全で快適な運転を行うことが望まれる。

![reactive_vs_non_reactive](./reactive_vs_non_reactive.png)

この論文はDeep Structured Reactive Planningを提案する。Deep Structured Reactive Planningはサンプルベースのプランニングである。サンプラーを使って経路を生成する。そして生成した経路の評価を行い、最も良い経路を選択する。

サンプルの生成にはTrajectory Samplerを使う。Trajectory Samplerは環境中にいる車（アクターと呼ぶ）の将来の経路を走行空間を効率よくサンプリングするジオメトリックなサンプラーである。

経路の評価にはDeep Structured Modelsを使う。Deep Structured Modelsは深層モデルを使ったMRF (マルコフ確率場)である。各アクターの予測経路をノードとして構成される。アクター間の相互作用を捉えたグラフである。Deep Structured Modelsは深層モデルにより２つのエネルギーを計算する。１つは予測経路単体の良さを示すエネルギーである。もう１つは２つの予測経路の衝突に関するエネルギーである。計算したエネルギーはMRFを伝播するために使われる。伝播を行うことで、自動運転車両がある経路を選択するとき、他の車の予測経路がどれだけ起こりやすいかを示す周辺確率を計算する。

Deep Structured Reactive Planningは経路を選択するとき、Deep Structured Modelsが計算したエネルギーで構成されたコストを、同じく計算した周辺確率で重み付けすることでコストの期待値を計算する。一つの自動運転車の計画経路に対して各アクターにつき複数の候補を考慮する。こうすることで他のアクターの行動の不確実性を考慮することができる。安全性を犠牲にすることなくターゲットレーンへの合流や右左折などの複雑な操作をより効果的かつ効率的に完了することができる。

## 先行研究と比べてどこがすごい？何を解決したか？

* 自動運転車の行動だけでなく自動運転車の行動に条件付けられた他のアクターの行動を取り入れたプランニングは他のアクターの反応と安全を本質的に考慮していることを示した。

* 検証を行った結果、Deep Structured Reactive PlanningはNon-reactive plannerの性能を凌駕した。

## 手法は？

N個のアクターが走行している環境で自動運転車が走行するシナリオを考える。すべてのアクターの将来の行動を$$\mathcal{Y} = (\mathbf{y}_0, \mathbf{y}_1, \dots, \mathbf{y}_N)$$とする。$$\mathbf{y}_0$$を自動運転車、$$\mathcal{Y}_r = (\mathbf{y}_1, \dots, \mathbf{y}_N)$$を他のアクターとする。また自動運転車はLIDARの点群とHDマップなどの情報にアクセスできるとする。

### Deep Structured Model

環境コンテクスト$$\mathcal{X}$$を条件とするアクターの将来の経路の同時分布をDeep Structured Modelで表す。

$$p(\mathcal{Y}\mid \mathcal{X}; \mathbf{w}) = \frac{1}{Z} \exp (-C(\mathcal{Y}, \mathcal{X}; \mathbf{w}))$$

$$C$$はすべてのアクターの経路の結合エネルギーである。結合エネルギーはアクターの固有のエネルギー$$C_{\text{traj}}$$とアクター間の相互作用のエネルギー$$C_{\text{inter}}$$で構成される。

$$C(\mathcal{Y}, \mathcal{X}; \mathbf{w}) =
\sum_{i=0}^{N} C_{\text{traj}}(\mathbf{y}_i \mid \mathcal{X}; \mathbf{w_{traj}}) +
\sum_{i,j} C_{\text{inter}}(\mathbf{y}_i, \mathbf{y}_j)$$

アクターの固有のエネルギー$$C_{\text{traj}}$$はアクターの経路の良さをコストとして示す。アクターの固有のエネルギー$$C_{\text{traj}}$$はニューラルネットワークにより計算する。用いるネットワークはDSDNet ([summary](../DSDNet: Deep Structured self-Driving Network/summary.md))で使われたネットワークと同じである。また自動運転車の固有エネルギーと他のアクターの固有エネルギーの計算は違う重みを用いる。アクター間の相互作用のエネルギー$$C_{\text{inter}}$$は衝突によるエネルギー$$C_{\text{collision}}$$と安全な距離によるエネルギー$$C_{\text{safety distance}}$$で構成される。安全な距離を4mである。

![interaction_energy](/home/x/Workspace/matomEmotam/papers/Deep Structured Reactive Planning/interaction_energy.png)

Deep Structured Modelを使ってグラフを伝播することで様々な周辺確率を計算できる。推論時は$$p(\mathbf{y}_i \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w}) $$、訓練時は$$p(\mathbf{y}_i, \mathcal{X}; \mathbf{w})$$および$$p(\mathbf{y}_i,\mathbf{y}_j, \mathcal{X}; \mathbf{w})$$を計算する。周辺確率はLoopy Belief Propagation (LBP)を使うことで効率的に計算できる。LBPはリカレントニューラルネットワークの特殊系として解釈することができる。つまりLBPによって計算した周辺分布は勾配の計算が可能である。

### Trajectory Sampler

連続空間で表現されるアクターの経路のエネルギーを推論することは非常に困難である。エネルギーの推論を簡単にするためにDSDNet ([summary](../DSDNet: Deep Structured self-Driving Network/summary.md))と同様に、走行空間を効率よくサンプルするTrajectory Samplerを用いる。Trajecotry Samplerは将来の経路を直線や円弧で出力する。

### Reactive Inference objective

次の最適化問題を解くことで現在時刻から数秒間先までの経路$$\mathbf{y}_0^{*}$$を計画する。

$$\DeclareMathOperator*{\argmin}{arg\,min}
\mathbf{y}_0^{*} = \argmin_{\mathbf{y}_0} f (\mathcal{Y}, \mathcal{X}; \mathbf{w})$$

関数$$f (\mathcal{Y}, \mathcal{X}; \mathbf{w})$$は自動運転車の経路を条件とする他のアクターの経路の分布全体にわたる結合エネルギーの期待値である。

$$\begin{align}
f(\mathcal{Y}, \mathcal{X}; \mathbf{w}) &=
\mathbb{E}_{\mathcal{Y}_r \sim p(\mathcal{Y}_r \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w})} [C(\mathcal{Y}, \mathcal{X}; \mathbf{w})]
\\
&= C_{\text{traj}}(\mathbf{y}_0, \mathcal{X}; \mathbf{w}) +
\mathbb{E}_{\mathcal{Y}_r \sim p(\mathcal{Y}_r \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w})} \left[
\sum_{i=1}^{N} C_{\text{traj}}(\mathbf{y}_i \mid \mathcal{X}; \mathbf{w}) +
\sum_{i=1}^{N} C_{\text{inter}}(\mathbf{y}_0, \mathbf{y}_i) +
\sum_{i=1,j=1}^{N,N} C_{\text{inter}}(\mathbf{y}_i, \mathbf{y}_j)
\right]\
\end{align} $$

実装では計算量を削減するため、他のアクター同士の相互作用のエネルギー$$C_{\text{inter}}(\mathbf{y}_i, \mathbf{y}_j)$$は無視する。そしてTrajectory Samplerで生成されるサンプルをつかって直接期待値を計算する。つまり次の計算を行う。

$$C_{\text{traj}}(\mathbf{y}_0, \mathcal{X}; \mathbf{w}) +
\sum_{i=1}^{N} p(\mathbf{y}_i \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w}) C_{\text{traj}} (\mathbf{y}_i \mid \mathcal{X}; \mathbf{w}) +
\sum_{i=1}^{N} p(\mathbf{y}_i \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w}) C_{\text{inter}} (\mathbf{y}_0, \mathbf{y}_i)$$

### Goal Energy

DIM ([summary](../DEEP IMITATIVE MODELS FOR FLEXIBLE INFERENCE, PLANNING, AND CONTROL/summary.md))やPRECOG ([summary](../PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings/summary.md))の方法と同様にゴールエネルギーを計画の目的関数に加える。ゴールエネルギーを加えることで自動運転車の目的を達成するように経路計画を行う。ゴールエネルギーは自動運転車が走行するシナリオに応じて変えることができる。例えば交差点の右左折では目的の道路を2次元点で表し、経路の最終地点とL2距離をエネルギーとする。レーンチェンジでは目的のレーンをPolylineで表し、経路の各点とpolylineの距離の平均をエネルギーとする。

### 学習

訓練データであるアクターの経路を使ってDeep Structured Modelを訓練する。LBPを使って観測を条件とするアクターの経路の周辺確率$$p(\mathbf{y}_i, \mathcal{X}; \mathbf{w})$$および同時確率$$p(\mathbf{y}_i,\mathbf{y}_j, \mathcal{X}; \mathbf{w})$$を計算する。そして計算した確率をクロスエントロピーを使って真の経路と予測経路の分布を近づける。ただし真の経路に近い経路は損失計算から除く。すべての予測経路をクロスエントロピーの計算に使うと、真の経路に距離が近い経路が間違いと評価されるためである。不当な評価を避けることで確率の推定性能が向上する。

$$\mathcal{L} = \sum_{i} \mathcal{L}_i +  \sum_{i,j} \mathcal{L}_{i,j}$$

$$\mathcal{L}_i = \frac{1}{K}
\sum_{\mathbf{y} \notin  \Delta (\mathbf{y}_i^{*})}
p_{\text{g.t.}}(\mathbf{y}_i) \log p(\mathbf{y}_i, \mathcal{X}; \mathbf{w})$$

$$\mathcal{L}_{i, j} = \frac{1}{K^2}
\sum_{\mathbf{y}_i \notin  \Delta (\mathbf{y}_i^{*}), \mathbf{y}_j \notin  \Delta (\mathbf{y}_j^{*})}
p_{\text{g.t.}}(\mathbf{y}_i, \mathbf{y}_j) \log p(\mathbf{y}_i,\mathbf{y}_j, \mathcal{X}; \mathbf{w})$$

$$\Delta (\mathbf{y}_i^{*})$$は正解の経路と距離が近いが正解でない経路群である。

## どうやって有効だと検証した？

CARLAおよびUber ATGのSimbaのシミュレーターで走行性能、予測性能、Ablation Studyの検証を行った。テストするシミュレーターごとのデータセットで検証に使われるモデルを訓練した。訓練に使用したCARLAのデータセットはPRECOGで使われたオープンなデータセットと同じものである。CARLAのデータセットは60000個の6秒間のシークエンスを含む。LIDARの点群をラスタライズした俯瞰図と最初の2秒間の経路をモデルへの入力データ、2~4秒の経路を予測する経路とした。Simbaのデータセットは1000回以上の自動運転車の走行からなる6500個のシークエンスを含む。各シークエンスの長さは25秒である。

### 走行テスト

Deep structured reactive planningの走行性能を検証するため、CARLAおよびSimbaのシミュレーターでテストした。テストシナリオは次の２つである。

* レーンチェンジ
* 信号のない交差点で左折を行う

いずれのシナリオも次の条件で終了する。

* 自動運転車がゴールに到達した
* シミュレーションの制限時間になった
* 自動運転車が衝突した

#### Simbaの具体的な設定

レーンチェンジおよび左折のシナリオをさらに細かく分類して12個のテンプレートシナリオを用意した。12個のテンプレートシナリオはアクター間の相互作用が高いシナリオである。シナリオ内のアクターはヒューリスティックによるカーフォロイングモデルに従い行動する。シミュレーションは10Hzで動作する。シミュレーション内のLIDARにより自動運転車の周囲の点群を記録する。初期位置や速度を変化させ、各テンプレートシナリオごとに25回シミュレーションを行った。作成された計300個のエピソードのうち、50個をValidationデータに、250個をテストデータとした。

#### CARLAの具体的な設定

Simbaと異なりテンプレートシナリオの数を6個とした。またシナリオ内のアクターはCARLAのAPIで提供されているBasicAgentを元にしたモデルに従い動作する。初期位置や速度を変化させ、各テンプレートシナリオごとに25回シミュレーションを行った。作成された計150個のエピソードのうち、50個をValidationデータに、100個をテストデータとした。

#### 比較手法

Deep strucutred reactive planningの他にPRECOG ([summary](../PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings/summary.md))とReactive planningすることの重要性を明確にするためのnon-reactiveなプランナーを用意した。Non-reactiveなプランナーは自動運転車の経路に条件付けられないコストを使う。

$$\begin{align}
f_{\text{nonreactive}} &=
\mathbb{E}_{\mathcal{Y}_r \sim
p(\mathcal{Y}_r \mid \mathcal{X}; \mathbf{w})}
[C(\mathcal{Y}, \mathcal{X}; \mathbf{w})] \\
&= C_{\text{traj}}(\mathbf{y}_0, \mathcal{X}; \mathbf{w}) +
\mathbb{E}_{\mathcal{Y}_r \sim
p(\mathcal{Y}_r \mid \mathcal{X}; \mathbf{w})
} \left[
\sum_{i=1}^{N} C_{\text{inter}}(\mathbf{y}_0, \mathbf{y}_i)
\right]
\end{align}$$

#### 走行テスト結果

CARLAおよびSimbaのシミュレーターでテストした結果は次のとおりである。

![simulation_test](./simulation_test.png)

Succ (%)はSucess Rateである。自動運転車がレーンチェンジや左折を成功させた割合である。TTC (s)はtime to completionである。シナリオの完走にかかった時間である。Goalはゴールまでの距離である。CR (%)はCollision Rateである。Brakeはブレーキした回数である。CARLAのみ有効である。

提案手法であるReactive PlannerがSuccess Rate、TTC、Goalのメトリックで他の手法より良い結果である。またCollision RateはReactive Planner、Non−Reactive Plannerともに同等の値である。Reactive Plannerが目的関数通り、他のアクターの反応を考慮していることを示している。事故する割合が上がるようなアグレッシブな動作をすることなく、他のアクターがいる中でより効果的にゴールへのナビゲーションが行えていることを示している。またReactiveおよびNon−Reactive PlannerがPRECOGよりも良い結果である。

#### レーンチェンジの走行結果

次の図はターゲットのレーンへ合流するシナリオを走行した結果である。Reactive Plannerはターゲットレーンに合流することができた。Non−Reactive Plannerはできなかった。Reactive Plannerの結果ではターゲットレーンにいる車が自動運転車を入れさせるために減速している。その一方でNon−Reactive Plannerは時間の経過とともにレーンの左側にゆっくりとよっている。

![lane_merge_result](./lane_merge_result.png)

### 予測テスト

PRECOGのデータセットおよびNuScenesで予測性能をテストした。使用した評価メトリックはminMSDである。提案手法は比較手法比べて同等もしくは上回っていることがわかる。DSDNet ([summary](../DSDNet: Deep Structured self-Driving Network/summary.md))と同様に、アクターごとの離散経路のサンプルをエネルギーベースのモデルで評価することが効果的であることを示している。

![prediction_result_carla](./prediction_result_carla.png)

![prediction_result_nuscenes](./prediction_result_nuscenes.png)

### Ablation Study

訓練に用いる損失関数を変えたときの性能をテストした。Cross-entropyはグランドトルースと近い経路も損失に加える純粋なCross-entorpyを使った結果である。提案手法が最も良い結果である。

![ablation_study](./ablation_study.png)

## 課題は？議論はある？

計画時に他のアクター同士の相互作用のエネルギー$$C_{\text{inter}}(\mathbf{y}_i, \mathbf{y}_j)$$を無視することで、自動運転車の行動が原因となって隣接する他のアクター同士が衝突するシチュエーションを考慮できない。完全に無視するのではなく、近くのアクターに関しては相互作用のエネルギーを計算するなどの工夫が考えられる。

## 補足

### Reactive plannerの定義

自動運転車の行動$$\mathbf{y}_0$$を条件に他のアクターの行動の予測を考えるプランナーをreactive plannerと定義する。また自動運転車の行動$$\mathbf{y}_0$$と独立した予測モデルを使って他のアクターの行動を考えるプランナーをnon-reactive plannerと定義する。

### Reactive plannerとNon Reactive plannerの補間

Reactive planningはひとつの自動運転車の計画経路を条件にアクターの行動の予測するプランナーである。ひとつだけでなく、複数の自動運転車の計画を条件にアクターの行動を予測する場合、計画の目的関数は次式で表せる。

$$C_{\text{traj}}(\mathbf{y}_0, \mathcal{X}; \mathbf{w}) +
\sum_{i=1}^{N} p(\mathbf{y}_i \mid S^{\mathbf{y}_0}, \mathcal{X}; \mathbf{w}) C_{\text{traj}} (\mathbf{y}_i \mid \mathcal{X}; \mathbf{w}) +
\sum_{i=1}^{N} p(\mathbf{y}_i \mid S^{\mathbf{y}_0}, \mathcal{X}; \mathbf{w}) C_{\text{inter}} (\mathbf{y}_0, \mathbf{y}_i)$$

$$S^{\mathbf{y}_0}$$は自動運転車の計画$$\mathbf{y}_0$$と距離が近い上位k個の経路である。目的関数は$$k=1$$のときReactive planning、$$k=K$$のときNon−Reactive planningとなることがわかる。kを変化させることでReactivityを補間することができる。kが1より大きいとき、他のアクターは自動運転車の計画を正確に知らないこと仮定している。kが大きくなればなるほど、自動運転車の意図が不明確であることを仮定している。次の表は異なる$$k$$で自動運転車を走行したときの検証結果である。

![Interpolating_result](./Interpolating_result.png)

$$k$$の数が増えるほど（Non-reactiveになるほど）、ほぼ一定のCollision Rateに対して次の傾向が見られる。

* Success Rateが下がる
* TTCが増える

シミュレーション結果から示せないが、どちらの極端な場合よりも、補間された計画目標が安全に計画を立てながら、高い成功率を達成できると考える。

### PRECOGの走行テストの結果が悪い原因の考察

PRECOGは生成モデルであるESPを使って観測を条件としてアクターの経路を生成する。そして生成した経路を使ってReactive Planningを行う。PRECOGの検証結果が悪い原因として2つの仮設が考えられる。1つめはout-of-distributionである。訓練データにない状況で経路を効果的に予測できないことが起因していると思われる。２つめは評価するべき経路の生成を保証しないことである。潜在変数を通して生成を行うため、経路計画に必要とする経路を生成するまで多くの試行回数を必要とする可能性がある。

## 次に読むべき論文は？

* [Contingencies from Observations: Tractable Contingency Planning with Learned Behavior Models](../Contingencies from Observations: Tractable Contingency Planning with Learned Behavior Models/summary.md)
* [DSDNet: Deep Structured self-Driving Network](../DSDNet: Deep Structured self-Driving Network/summary.md)
* [PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings](../PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings/summary.md)

## 個人的メモ

なし
