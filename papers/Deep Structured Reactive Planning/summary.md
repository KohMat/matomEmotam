# [日本語まとめ] Deep Structured Reactive Planning

[Jerry Liu](https://arxiv.org/search/cs?searchtype=author&query=Liu%2C+J), [Wenyuan Zeng](https://arxiv.org/search/cs?searchtype=author&query=Zeng%2C+W), [Raquel Urtasun](https://arxiv.org/search/cs?searchtype=author&query=Urtasun%2C+R), [Ersin Yumer](https://arxiv.org/search/cs?searchtype=author&query=Yumer%2C+E)

* [arxiv](https://arxiv.org/pdf/2101.06832.pdf)

## どんなもの？

Reactive planningは予測と計画を同時に行う経路計画法である。Reactive planningは自動運転車の行動が他の車の行動に及ぼす影響を考慮することができる。次のシナリオは一般的な運転でもよく遭遇するようなシナリオであるが、速やかに走行するためには他の車の行動の理解が求められる。

* 自動運転車が他の車に道を譲った場合、他の車がその道を先に走行する
* 自動運転車が道を譲らず走行した場合、他の車はその道を譲る

しかし予測を元に計画を行うシステム（non-reactive planner）はこのようなシナリオに対して快適な走行を行うことはできない。Non-reactive plannerは従来の自動運転に多く採用されているが、自動運転車の行動による他車両の行動の変化を無視する。大抵の場合、non-reactive plannerは目的の車線が利用可能になるまで待機する選択を行う。しかしながら、自動運転車の後ろに車がいる場合、待つという行動は交通の妨げになる。したがって単純に待つという戦略は理にかなっている運転とは言えない。自動運転車だけでなく他の車にとっても安全で快適な運転を行うことが望まれる。

![reactive_vs_non_reactive](./reactive_vs_non_reactive.png)

この論文はDeep Structured Reactive Planningを提案する。Deep Structured Reactive Planningはサンプルベースのプランニングである。サンプラーを使って経路を生成する。そして生成した経路の評価を行い、最も良い経路を選択する。

サンプルの生成にはTrajectory Samplerを使う。Trajectory Samplerは環境中にいる車（アクターと呼ぶ）の将来の経路を空間的に密にサンプリングするジオメトリックなサンプラーである。

経路の評価にはDeep Structured Modelsを使う。Deep Structured Modelsは深層モデルを使ったMRF (マルコフ確率場)である。各アクターの予測経路をノードとして構成されるアクター間の相互作用を捉えたグラフである。Deep Structured Modelsは深層モデルにより２つのエネルギーを計算する。１つは予測経路単体の良さを示すエネルギーである。もう１つは２つの予測経路の衝突に関するエネルギーである。計算したエネルギーはMRFを伝播するために使われる。伝播を行うことで、自動運転車両がある経路を選択するとき、他の車の予測経路がどれだけ起こりやすいかを示す周辺確率を計算する。

Deep Structured Reactive Planningは経路を選択するとき、Deep Structured Modelsが計算したエネルギーからなるコストを、同じく計算した周辺確率で重み付けすることでコストの期待値を計算する。一つの自動運転車の計画経路に対して各アクターにつき複数の候補を考慮する。こうすることで他のアクターの行動の不確実性を考慮することができる。安全性を犠牲にすることなくターゲットレーンへの合流や右左折などの複雑な操作をより効果的かつ効率的に完了することができる。

## 先行研究と比べてどこがすごい？何を解決したか？

* 
* 検証を行った結果、Deep Structured Reactive PlanningはNon-reactive plannerの性能を凌駕した。



## 手法は？

N個のアクターが走行している環境で自動運転車が走行するシナリオを考える。すべてのアクターの将来の行動を$$\mathcal{Y} = (\mathbf{y}_0, \mathbf{y}_1, \dots, \mathbf{y}_N)$$とする。$$\mathbf{y}_0$$は自動運転車、$$\mathcal{Y}_r = (\mathbf{y}_1, \dots, \mathbf{y}_N)$$は他のアクターである。

自動運転車の行動$$\mathbf{y}_0$$を条件とする他のアクターの行動の予測を考えるプランナーをreactive plannerと定義する。

自動運転車の行動$$\mathbf{y}_0$$と独立した予測モデルを使って他のアクターの行動を考えるプランナーをnon-reactive plannerと定義する。

### Structured Model for Joint Perception

$$p(\mathcal{Y}\mid \mathbf{X}; \mathbf{w}) = \frac{1}{Z} \exp (-C(\mathcal{Y}, \mathcal{X}; \mathbf{w}))$$

$$C(\mathcal{Y}, \mathcal{X}; \mathbf{w}) =
\sum_{i=0}^{N} C_{\text{traj}}(\mathbf{y}_i \mid \mathcal{X}; \mathbf{w_{traj}}) +
\sum_{i,j} C_{\text{inter}}(\mathbf{y}_i, \mathbf{y}_j)$$

$$C$$はすべてのアクターの経路の結合エネルギーである。

$$C_{\text{traj}}$$はアクターの固有のエネルギー。アクターの経路のコストを示す。ニューラルネットワークにより計算される。

$$C_{\text{inter}}$$はアクター間の相互作用のエネルギー。衝突によるエネルギー$$C_{\text{collision}}$$と安全な距離によるエネルギー$$C_{\text{safety distance}}$$で構成される。

![interaction_energy](/home/x/Workspace/matomEmotam/papers/Deep Structured Reactive Planning/interaction_energy.png)

### Reactive Inference objective

自動運転車の次の数秒間の計画を決定する。

将来の行動に対する確率とコスト

自動運転車の行動だけでなく自動運転車の行動に条件付けられた他のアクターの行動を取り入れたコスト

そのようなプランニングは他のアクターの反応と安全を本質的に考慮していることを示す。



経路計画の目的は

$$\DeclareMathOperator*{\argmin}{arg\,min}
\mathbf{y}_0^{*} = \argmin_{\mathbf{y}_0} f (\mathcal{Y}, \mathcal{X}; \mathbf{w})$$

となる自動運転車の経路$$\mathbf{y}_0^{*}$$を見つけることである。

$$f(\mathcal{Y}, \mathcal{X}; \mathbf{w}) =
\mathbb{E}_{\mathcal{Y}_r \sim p(\mathcal{Y}_r \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w})} [C(\mathcal{Y}, \mathcal{X}; \mathbf{w})]$$

$$p(\mathcal{Y}_r \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w})$$は同時確率$$p(\mathcal{Y} \mid \mathcal{X}; \mathbf{w})$$から導かれる。



すべてのアクターの経路の結合エネルギーを変形して、自動運転車に関係があるエネルギーと関係がないエネルギーに分ける。

$$C_{\text{traj}}(\mathbf{y}_0, \mathcal{X}; \mathbf{w}) +
\mathbb{E}_{\mathcal{Y}_r \sim p(\mathcal{Y}_r \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w})} \left[
\sum_{i=1}^{N} C_{\text{traj}}(\mathbf{y}_i \mid \mathcal{X}; \mathbf{w}) +
\sum_{i=1}^{N} C_{\text{inter}}(\mathbf{y}_0, \mathbf{y}_i) +
\sum_{i=1,j=1}^{N,N} C_{\text{inter}}(\mathbf{y}_i, \mathbf{y}_j)
\right]$$



### Inference for Conditional Planning Objective

自動運転車の固有エネルギーと他のアクターの固有エネルギーの計算は違う重みを用いる。

自己中心的なセンサーデータをよりよく活用し、SDV固有の行動をモデル化することができる

計算量を削減するため、他のアクター同士の相互作用のエネルギー$$C_{\text{inter}}(\mathbf{y}_i, \mathbf{y}_j)$$は無視する。

$$C_{\text{traj}}(\mathbf{y}_0, \mathcal{X}; \mathbf{w}) +
\mathbb{E}_{\mathcal{Y}_r \sim p(\mathcal{Y}_r \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w})} \left[
\sum_{i=1}^{N} C_{\text{traj}}(\mathbf{y}_i \mid \mathcal{X}; \mathbf{w}) +
\sum_{i=1}^{N} C_{\text{inter}}(\mathbf{y}_0, \mathbf{y}_i)
\right]$$

Trajectory Samplerで生成されるサンプルをつかって直接期待値を計算する

$$C_{\text{traj}}(\mathbf{y}_0, \mathcal{X}; \mathbf{w}) +
\sum_{\mathcal{Y}_r} p(\mathcal{Y}_r \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w}) \left[
\sum_{i=1}^{N} C_{\text{traj}}(\mathbf{y}_i \mid \mathcal{X}; \mathbf{w}) +
\sum_{i=1}^{N} C_{\text{inter}}(\mathbf{y}_0, \mathbf{y}_i)
\right]$$

変形して

$$C_{\text{traj}}(\mathbf{y}_0, \mathcal{X}; \mathbf{w}) +
\sum_{i=1}^{N} p(\mathbf{y}_i \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w}) C_{\text{traj}} (\mathbf{y}_i \mid \mathcal{X}; \mathbf{w}) +
\sum_{i=1}^{N} p(\mathbf{y}_i \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w}) C_{\text{inter}} (\mathbf{y}_0, \mathbf{y}_i)$$

この関数を目的関数とする

実用的には各項に重みをつける。これによりreactiveさを制御できる。



周辺確率$$p(\mathbf{y}_i \mid \mathbf{y}_0, \mathcal{X}; \mathbf{w}) $$はLoopy Belief Propagationにより計算する。

LBPはリカレントニューラルネットワークの特殊系として解釈することができる。

LBPであるメッセージ伝達によって計算した周辺分布は勾配の計算が可能である。

すなわちend-to-endで計算することができる。



### Goal Energy

のようにゴールへ到達するための、ゴールエネルギー$$C_{\text{goal}}^{\mathbf{y}_0}$$を使う。

ゴールエネルギーは自動運転車が走行するシナリオによって異なる。

ゴールが道路上のある位置の場合、L2距離をゴールエネルギーとする。

ゴールがレーンの場合、自動運転車の経路の各点と目的レーンとの平均距離をゴールエネルギーとする。

推論時にゴールエネルギーを計画の目的関数に加える。

### 学習

joint structured modelを観測した真のすべてのアクターの経路を使って訓練する。

自動運転車のベストな経路とアクターの行動の確率を含むエネルギーを学習する

クロスエントロピーを使って真の経路と予測経路の分布を近づける。

$$\mathcal{L} = \sum_{i} \mathcal{L}_i +  \sum_{i,j} \mathcal{L}_{i,j}$$

$$\mathcal{L}_i = \frac{1}{K}
\sum_{\mathbf{y} \notin  \Delta (\mathbf{y}_i^{*})}
p_{\text{g.t.}}(\mathbf{y}_i) \log p(\mathbf{y}_i, \mathcal{X}; \mathbf{w})$$

$$\mathcal{L}_{i, j} = \frac{1}{K^2}
\sum_{\mathbf{y}_i \notin  \Delta (\mathbf{y}_i^{*}), \mathbf{y}_j \notin  \Delta (\mathbf{y}_j^{*})}
p_{\text{g.t.}}(\mathbf{y}_i, \mathbf{y}_j) \log p(\mathbf{y}_i,\mathbf{y}_j, \mathcal{X}; \mathbf{w})$$

$$\Delta (\mathbf{y}_i^{*})$$は正解の経路と距離が近いが正解でない経路群

この経路群の損失を計算しないことで正解に近い経路に間違いとしない。





## どうやって有効だと検証した？

CARLAおよびUber ATGのSimbaでテストした。

Deep strucutred reactive planningの他に、Reactive planningすることの重要性を明確にするために、non-reactiveなプランナーを用意した。Non-reactiveなプランナーは自動運転車の経路に条件付けられないコストを使う。

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

CARLA LIDARの点群をラスタライズした図と過去2秒間の経路から4秒先までの経路を予測する。

Simbaのシミュレーション設定

テストするシナリオは大きく分けて２つある。

* レーンチェンジ
* 信号のない交差点で左折を行う

具体的にはレーンチェンジおよび左折のシナリオをさらに細かく分類し12個のアクター間の相互作用が高いテンプレートシナリオを用意した。

またシナリオ内のアクターはヒューリスティックによるカーフォロイングモデルに従い行動する。

各テンプレートシナリオごとに初期位置や速度を変化させ、25個のシナリオを作成した。計300個のシナリオのうち、250個をValidationデータに、50個をテストデータとした。

CARLAのシミュレーション設定





CARLAとSimbaそれぞれの環境で訓練データセットを使ってモデルを訓練した。各データセットは25秒間の経路で構成される。CARLAのデータセットはPRECOGで使われたオープンなデータセットである。

| タイプ/データの個数 | Train | Validation | Test |
| ------------------- | ----- | ---------- | ---- |
| Simba               | 6500  | 50         | 250  |
| CARLA               | 60000 | 50         | 100  |

Validationデータは50個、テストデータは250個作成した。





CARLAのデータセットはPRECOGと同様のものである。









## 課題は？議論はある？

他のアクター同士の相互作用のエネルギー$$C_{\text{inter}}(\mathbf{y}_i, \mathbf{y}_j)$$を無視することで、自動運転車の行動が原因となって隣接する他のアクター同士が衝突するシチュエーションを考慮できない。完全に無視するのではなく、近くのアクターに関しては相互作用のエネルギーを計算するなどの工夫が考えられる。

## 次に読むべき論文は？

* [Contingencies from Observations: Tractable Contingency Planning with Learned Behavior Models](../Contingencies from Observations: Tractable Contingency Planning with Learned Behavior Models/summary.md)
* [DSDNet: Deep Structured self-Driving Network](../DSDNet: Deep Structured self-Driving Network/summary.md)
* [PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings](../PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings/summary.md)

## 補足

### Reactive plannerとNon Reactive plannerの中間（Interpolation）

reactive plannerの目的関数で使われる自動運転車の経路で条件付けられるアクターの経路の確率に関して。

自動運転車の経路を１個だけでなく２，３、...、K個に増やす。この経路群でのアクターの経路の条件付き確率は、

と表せる。





## 個人的メモ

なし



PiPは既知の自動運転車の計画を条件として他のアクターの予測を行う。

PRECOGはflowベースでreactive planningを行う。自己回帰によって各ステップ生成を行うため、実行が遅い。またflowモデルがすべてのモードを生成しないため、衝突の可能性を見過ごす。結果的に障害物回避が完全に保証できない。