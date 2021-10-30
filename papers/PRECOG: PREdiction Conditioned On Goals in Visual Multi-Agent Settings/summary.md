# [日本語まとめ] PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings

[Nicholas Rhinehart](https://arxiv.org/search/cs?searchtype=author&query=Rhinehart%2C+N), [Rowan McAllister](https://arxiv.org/search/cs?searchtype=author&query=McAllister%2C+R), [Kris Kitani](https://arxiv.org/search/cs?searchtype=author&query=Kitani%2C+K), [Sergey Levine](https://arxiv.org/search/cs?searchtype=author&query=Levine%2C+S)

* [ICCV 2019](https://openaccess.thecvf.com/content_ICCV_2019/html/Rhinehart_PRECOG_PREdiction_Conditioned_on_Goals_in_Visual_Multi-Agent_Settings_ICCV_2019_paper.html)
* [Arxiv 30 Sep 2019](https://arxiv.org/abs/1905.01296)　論文には多くの視覚的な結果がある
* [site](https://sites.google.com/view/precog)
* [github](https://github.com/nrhine1/precog)

## どんなもの？

自動運転車が人間とともに道路上で動作するためには、他のドライバーの行動を予測することが必要である。特に自動運転の条件判断や経路計画に必要とされる予測はただ漠然とした単純な予測ではない。自動運転車が目的を達成する意図に応じて他のエージェントが何をする可能性が高いかを示す予測が必要とされる。

この論文は条件判断のために複数の車（マルチエージェント）の行動を予測する方法ESPおよびPRECOGを提案する。ESPおよびPRECOGともに自車両も含めたマルチエージェントの相互作用を考慮した予測を行う。行動は２次元位置で構成される経路として出力される。

![EmbeddedImage](./EmbeddedImage.gif)

ESP(Estimating Social-forecast Probabilities)は単一エージェントの経路を予測するR2P2([link](https://people.eecs.berkeley.edu/~nrhinehart/papers/r2p2_cvf.pdf), [summary](../R2P2: A reparameterized pushforward policy for diverse, precise generative path forecasting/summary.md))にマルチエージェント間の相互作用を捉えるように変更を加えたフローベース生成モデルである。ESPは潜在変数からすべてのエージェントの経路を生成する。また経路を生成するだけでなく、エージェントの行動を確率的に説明する。各時刻の各エージェントの状態を表すFactorized潜在変数により、任意の時間における任意エージェントの状態を独立に変えたときの効果を確率で出力する。

PRECOG (PREdition Conditioned On Goal)はESPを使った条件付き予測を行う方法である。PRECOGは自動運転車の目的地などの有り得そうな将来の状態をゴールとみなす。そして自動運転車がゴールへ向かうような経路を計画する。計画により予測経路とともにその経路を表す潜在変数が得られる。得られた自動運転車の潜在変数と正規分布からサンプリングした他のエージェントの潜在変数をESPで予測経路に変換する。このように計算された他のエージェント経路は自動運転車の経路に条件付けられた経路となる。自動運転車が目的地へ向かう場合に集中して予測するので予測する経路の可能性を絞ることができる。結果として自車両だけでなく相互に作用する他のエージェントの軌道の予測精度を高めることができる。

## 先行研究と比べてどこがすごい？何を解決したか？

* ESPがエージェント間の相互作用を考慮する予測を実行できることを示した。
* ESPがCALRAおよびnuScenesのデータセットで３つのstate-of-artの方法の性能を上回ることを示した。
* PRECOGが自車両だけでなく相互に作用するその他のエージェントの予測性能が改善されることをCALRAおよびnuScenesのデータセットを使い示した。

## 手法は？

### Estimating Social-forecast Probability (ESP)

ESPは観測$$\phi \doteq \{\mathbf{s}_{-\tau:0}, \chi \}$$を予測に使う。

* 過去から現在までのすべてエージェントの位置$$\mathbf{s}_{-\tau:0}$$
* LiDARの点群もしくは道路の構造物を俯瞰図で表現したボクセル$$\chi = \mathbb{R}^{200 \times 200 \times 2}$$

ESPはフローベースの生成モデル$$\mathbf{S} \sim q(\mathbf{S} \mid \phi)$$である。逆変換可能な関数$$f_{\theta}(\cdot)$$を使い現在時刻から$$T$$ステップ先までのすべてのエージェントの経路$$\mathbf{S} \in \mathbb{R}^{T \times A \times D}$$を生成する。

$$\mathbf{Z} \sim \mathcal{N}(0, I); \mathbf{S} = f_{\theta}(\mathbf{Z}; \phi)$$

関数$$f_{\theta}(\cdot)$$は各エージェント$$a$$の１ステップ先の更新式で構成される。

$$\mathbf{S}_{t}^{a} = f_{\theta}(\mathbf{Z}_t^a) = \mu_{\theta}^a(\mathbf{S}_{1:t-1}, \phi) + \sigma_{\theta}^a(\mathbf{S}_{1:t-1}, \phi) \cdot \mathbf{Z}_t^a \in \mathbb{R}^{D}$$

$$\mathbf{S}_{t}^{a}$$および$$\mathbf{Z}_{t}^{a}$$は時刻$$t$$におけるエージェント$$a$$の位置と潜在変数である。パラメータ$$\mu_{\theta}^a(\cdot) \in \mathbb{R}^{D}$$および$$\sigma_{\theta}^a(\cdot)\in \mathbb{R}^{D \times D}$$は状態$$\mathbf{S}_{t}$$の平均および標準偏差を出力するネットワーク関数である。この更新式を繰り返し適用することで現在時刻からTステップ先までの経路を計算する。

> 各遷移確率は正規分布と仮定している。ESPは次式で表すこともできる。$$q(\mathbf{S} \mid \phi)= \prod_{t=1}^T q(\mathbf{S}_t \mid \mathbf{S}_{1:t-1}, \phi)$$
>
> $$q(\mathbf{S}_t \mid \mathbf{S}_{1:t-1}, \phi)
> = \prod_{a=1}^A
> \mathcal{N}(\mathbf{S}_t^a ; \mu_{\theta}^a, \sigma_{\theta}^a{\sigma_{\theta}^a}^{\top})$$

ネットワーク関数の具体的なアーキテクチャは図で示すように観測マップ$$\chi$$から特徴マップ$$\Gamma$$を計算するCNN、過去のエージェントの経路から特徴を個々に計算するRNN、そして将来の経路を計算するRNNで構成される。

<img src="./EmbeddedImage.png" alt="EmbeddedImage" style="zoom: 50%;" />

このモデルは次の手順で動作する。

1. 時刻$$t$$に得られた観測からRNN(GRU)とCNNで、それぞれ特徴量$$\alpha$$と特徴マップ$$\Gamma$$を計算する

2. 時刻$$1:T$$までの以下のステップを繰り返す

   1. 時刻$$t$$の各エージェントの位置$$\mathbf{s}_{t-1}^a$$に対応した特徴マップ$$\Gamma$$の空間特徴量$$\Gamma(\mathbf{s}_{t-1}^a)$$をbilinear補間により取り出す

      $$\Gamma^{1:A} = \{ \Gamma(\mathbf{s}_{t-1}^1),..., \Gamma(\mathbf{s}_{t-1}^A) \}$$

   2. 各特徴量$$\alpha$$、$$\mathbf{s}_{t}^{1:A}$$、$$\Gamma^{1:A}$$をConcatenationして特徴$$p_{t-1}$$を構成する

   3. 特徴$$p_{t-1}$$から予測用のRNN(GRU)を使い、ベレの方法([wiki](https://en.wikipedia.org/wiki/Verlet_integration))のステップ$$m_{\theta}$$と位置の標準偏差$$\sigma_{\theta}$$を計算する

   4. ベレの方法から位置の平均を求める

      $$\mu = 2 \mathbf{s}_{t-1}^a - \mathbf{s}_{t-2}^a + m_{\theta}$$

   5. Reparametrization Trickを使い状態$$\mathbf{s}_{t}^a$$を計算する

      $$\mathbf{s}_{t}^a = \mu_{\theta} + \sigma_{\theta} \cdot \mathbf{z}_t^a$$


このモデルは訓練データ$$\mathcal{D}$$を使って対数尤度を最大化するように訓練される。

$$\max_{\theta} \mathbb{E}_{(s, \phi) \sim \mathcal{D}} \log p_{\theta}(\mathbf{S} \mid \phi)$$

### PREdiction Conditioned On Goals (PRECOG)

PRECOGのアルゴリズムは次の通りである。

1. Imitative planningにより自動運転車がゴールに止まるような潜在変数$$\mathbf{z}_{1:T}^0$$を求める

2. その他のエージェントの潜在変数$$^{1:K}\mathbf{z}$$を正規分布から$$K$$回サンプリングする

   $$^{1:K}\mathbf{z}_{1:T}^{1:A-1} \overset{iid}{\sim} \mathcal{N}(0, I)$$

   そして自動運転車の潜在変数と連結する。

   $$^{1:K}\mathbf{z}_{1:T}^{1:A} = [\mathbf{z}_{1:T}^{0}, ^k\mathbf{z}_{1:T}^{1:A-1}]$$

3. 関数$$f_{\theta}(\cdot)$$を使い、潜在変数を予測経路に変換する

   $$^{1:K}\mathbf{s}_{1:T}^{1:A} \leftarrow f(^{1:K}\mathbf{z}_{1:T}^{1:A}, \phi) $$

Imitative planningは"Deep Imitative Models for Flexible Inference, Planning, and Control"([arxiv](https://arxiv.org/pdf/1810.06544.pdf), [summary](../DEEP IMITATIVE MODELS FOR FLEXIBLE INFERENCE, PLANNING, AND CONTROL/summary.md))で提案された経路計画法である。Imitative planningはESPを使って次の最適化問題を解く。

$$\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator*{\argmax}{arg\,max}
\begin{equation}
z^{0 *} = \argmax_{z^r} \mathcal{L}(\mathbf{z}^0, \mathcal{G}, \phi)
\end{equation}$$

目的関数$$\mathcal{L}(\mathbf{z}^r, \mathcal{G})$$はマルチエージェントの模倣尤度とゴールの尤度の和の期待値である。

$$\mathcal{L}(\mathbf{z}^0, \mathcal{G}, \phi) = \mathbb{E}_{\mathbf{Z}^{1:A}} \left[ \log q(f(\mathbf{Z}) \mid \phi) + \log q(\mathcal{G} \mid f(\mathbf{Z}), \phi) \right]$$

ゴールの尤度$$q(\mathcal{G} \mid f(\mathbf{Z}), \phi)$$は自車両からゴールに向かうまでのウェイポイント$$\mathbf{w}$$を使った$$\mathcal{N}(\mathbf{w}; \mathbf{S}_T^r, \epsilon \mathbf{I})$$である。また期待値$$\mathcal{L}(\mathbf{z}^r, \mathcal{G})$$は次で示すようにゴールの尤度による重み付き平均を行い近似する。

$$\hat{\mathcal{L}}(^{1:K}\mathbf{z}, \mathcal{G}, \phi)
= \frac{1}{K} \sum_{k=1}^{K}
\log(
p(f(^k\mathbf{z}) \mid \phi)
p(\mathcal{G} \mid f(^k\mathbf{z}), \phi)
)$$

Imitative planningはこの最適化問題をGradient Ascentで求める。

![multimitativeplanning](./multimitativeplanning.png)

## どうやって有効だと検証した？

### ESPの検証

**Didactic Example**：簡素な交差点でのナビゲーションを使い予測性能を検証した。交差点には人間（オレンジ）およびロボット（青）が存在する。人間は常に4ステップ直進し、その後50％の確率で直進もしくは左折のどちらかの行動を行う。ロボットは交差点を直進しようと試みるが人間が左折した場合には譲歩する。このナビゲーションシミュレーションを行い、データセットを作成し、ESPおよびベースラインR2P2-MAの訓練を行った。R2P2-MAは相互作用を考慮しないESPである。予測用のRNNはすべてのエージェントではなく個々の特徴量のみを用いて次の状態を計算する。

![didactic_example](./didactic_example.png)

R2P2-MAはエージェント間の相互作用を考慮していないので50％の確率で人間とロボットがぶつかる予測を行った。これに対してESPは人間の決定に対して反応していることを示している。

**CARLAおよびnuScenes**：CALRAおよびnuScenesから10個のデータセットを作成し予測性能を検証した。ESP, no LIDARは観測からLIDARを除いたESPである。ESP, RoadはnuScenesの道路領域をバイナリマスクで表現した入力を追加したESPである。ESP, flexは可変数のエージェントに対応するESPである。

![esp_performance](./esp_performance.png)

CALRAおよびnuScenesのデータセットでESPの性能が比較手法のの性能を上回った。

### PRECOGの検証

CALRAおよびnuScenesを使いPRECOGの予測性能を検証した。Planingを行うエージェントは自車両のみとした。各データの最後の位置をゴールとして設定した。ゴールの尤度は正規分布を用いた。[DESIRE](https://arxiv.org/abs/1704.04394)およびESPと比較した結果は次のとおりである。

![precog_result](./precog_result.png)

ゴールを設定して予測することにより、自車両$$\hat{m}_K^1$$だけでなくその他の予測が向上することを示している。エージェントは近い順からソーティングされており、一番近い車両$$\hat{m}_K^2$$が最も影響を受けていることを示している。

## 課題は？議論はある？

さらなる精度向上のため、自動運転車だけでなく他のエージェントにもゴールや事前知識を使って条件付けることが考えられる。

## 次に読むべき論文は？

[Contingencies from Observations: Tractable Contingency Planning with Learned Behavior Models](../Contingencies from Observations: Tractable Contingency Planning with Learned Behavior Models/summary.md)

[Deep Imitative Models for Flexible Inference, Planning, and Control](../DEEP IMITATIVE MODELS FOR FLEXIBLE INFERENCE, PLANNING, AND CONTROL/summary.md)

[Deep Structured Reactive Planning](../Deep Structured Reactive Planning/summary.md)

## 補足

### 仮定及び各変数の詳細

連続空間、離散時間、POMDPのマルチエージェントシステムを扱う。時刻$$t$$におけるすべてのエージェントの状態（位置）を$$\mathbf{S}_t \in \mathbb{R}^{A \times D}$$とする。$$A$$はエージェント個数、$$D=2$$である。変数を関数と区別するためにボールドで表す。大文字は確率変数であることを示す。$$\mathbf{S}_t^a$$は時刻$$t$$におけるエージェント$$a$$の2次元位置$$x,y$$を示す。$$t=0$$は現在時刻、$$a$$が$$r$$もしくは$$1$$の場合は自車両、$$h$$もしくは$$2\sim$$の場合は他車両を示す。添字を省略した$$\mathbf{S}$$は$$\mathbf{S}_{1:T}^{1:A} \in \mathbb{R}^{T \times A \times D}$$を示す。すなわちすべてのエージェントの予測である。$$\chi$$はLIDARや道路などの高次元の観測である。実験した例ではLIDARの情報を俯瞰図で表現した観測$$\chi= \mathbb{R}^{200 \times 200 \times 2}$$を使った。各グリッドの面積は$$0.5 m^2$$であり、地面の上と下にあるポイントの2ビンのヒストグラムである。各エージェントは$$\phi \doteq \{\mathbf{s}_{-\tau:0}, \chi \}$$にアクセスできる。

### 可変数のエージェントに対応するESP

エージェント数が時刻$$1:T$$の間で変わるようなデータに対しては予め最大エージェント数$$A_{train}$$を決めた上でネットワークを設計する。そして予測経路を出力するRNNにマスク$$M \in \{ 0, 1 \} ^{A_{train}}$$を使うことで欠落しているエージェントを表現することで対応できる。

## 個人的メモ

* アーキテクチャ詳細はAppendix Cに紹介されており大きなアーキテクチャの構造の変化はないものの、性能を向上させるための空間特徴量の抽出方法など、いくつかの変更点がある。
* Didactic Exampleの行動パターン数を増やして検証したい。。例えば自車両は人間が左折したとき、人間もしくはロボットが交差点前に止まるパターン
* 上に書かれているとおり、PRECOGの検証で、自車両だけでなく、観測範囲内の道路の構造上到達しうる点も加えて検証をしたい。