# PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings

[Nicholas Rhinehart](https://arxiv.org/search/cs?searchtype=author&query=Rhinehart%2C+N), [Rowan McAllister](https://arxiv.org/search/cs?searchtype=author&query=McAllister%2C+R), [Kris Kitani](https://arxiv.org/search/cs?searchtype=author&query=Kitani%2C+K), [Sergey Levine](https://arxiv.org/search/cs?searchtype=author&query=Levine%2C+S)

* [ICCV 2019](https://openaccess.thecvf.com/content_ICCV_2019/html/Rhinehart_PRECOG_PREdiction_Conditioned_on_Goals_in_Visual_Multi-Agent_Settings_ICCV_2019_paper.html)
* [Arxiv 30 Sep 2019](https://arxiv.org/abs/1905.01296)　論文には多くの視覚的な結果がある
* [site](https://sites.google.com/view/precog)
* [github](https://github.com/nrhine1/precog)

## どんなもの？

可変数のエージェント（車両）の確率予測モデルESP(Estimating Social-forecast Probabilities)を提案する。ESPは単一エージェントを予測するR2P2([link](https://people.eecs.berkeley.edu/~nrhinehart/papers/r2p2_cvf.pdf), [summary](../R2P2: A reparameterized pushforward policy for diverse, precise generative path forecasting/summary.md))をマルチエージェント間の相互作用を考慮して一般化したもので、エージェント間の尤もらしい将来の相互作用を確率的に説明する。ESPでは各エージェントの決断をfactorized潜在変数によって表現する。マルチエージェントと時間にまたがる分解により、任意の時間における任意エージェントの状態を独立に変えたときの効果を調べることができる。つまり潜在変数をサンプリングすることで、マルチエージェントの相互作用を考慮した予測を行うことができる。

またESPを用いた予測法PRECOG(PREdition Conditioned On Goal)を提案する。PRECOGは単一エージェントのプランニングを行うDeep Imitative Planning([arxiv](https://arxiv.org/pdf/1810.06544.pdf), [summary](../DEEP IMITATIVE MODELS FOR FLEXIBLE INFERENCE, PLANNING, AND CONTROL/summary.md))をマルチエージェント間の相互作用を考慮して一般化したプランニングを使う。ESPを用いてこのプランニングを行うことで自車両が目的地（ゴールに向かって）に向かうような自車両の潜在変数を求めることができる。予測時にこの求めた潜在変数を使う。

![EmbeddedImage](./EmbeddedImage.gif)

## 先行研究と比べてどこがすごい？何を解決したか？

### state-of-artなマルチエージェントの予測

提案するESPはVAEやGANと異なり厳密な尤度推定を行うモデルである。ESPによる予測が現実(nuScenes)およびシミュレーション上(CALRA)で３つのstate-of-artの方法の性能を上回ることを示した。またESPがエージェント間の相互作用を考慮する予測を実行できることを示した。

### ゴール条件付きマルチエージェント予測

エージェントが向かうべきゴールを条件に予測を行う初の生成型のマルチエージェント予測法PRECOG(PREdition Conditioned On Goal)を提案した。自車両のエージェントにゴールを条件付け、マルチエージェント環境でのImitative Planningを行うことで、相互に作用するその他のエージェントの予測性能が改善されることを示した。

## 技術や手法の核はどこ？

連続空間、離散時間、POMDPのマルチエージェントシステムを扱う。時刻$$t$$におけるすべてのエージェントの状態（位置）を$$\mathbf{S}_t \in \mathbb{R}^{A \times D}$$とする。$$A$$はエージェント個数、$$D=2$$である。変数を関数と区別するためにボールドで表す。大文字は確率変数であることを示す。$$\mathbf{S}_t^a$$は時刻$$t$$におけるエージェント$$a$$の2次元位置$$x,y$$を示す。$$t=0$$は現在時刻、$$a$$が$$r$$もしくは$$1$$の場合は自車両、$$h$$もしくは$$2\sim$$の場合は他車両、人を示す。添字を省略した$$\mathbf{S}$$は$$\mathbf{S}_{1:T}^{1:A} \in \mathbb{R}^{T \times A \times D}$$を示す。すなわちすべてのエージェントの予測である。$$\chi$$はLIDARや道路などの高次元の観測である。実験した例ではLIDARの情報を俯瞰図で表現した観測$$\chi= \mathbb{R}^{200 \times 200 \times 2}$$を使った。各グリッドの面積は$$0.5 m^2$$であり、地面の上と下にあるポイントの2ビンのヒストグラムである。各エージェントは$$\phi \doteq \{\mathbf{s}_{-\tau:0}, \chi \}$$にアクセスできる。

### Estimating Social-forecast Probability (ESP)

ESPはマルチエージェントのTステップ先のダイナミクスを確率的に予測する尤度ベースの生成モデル$$\mathbf{S} \sim q(\mathbf{S} \mid \phi;\mathcal{D})$$である。$$\mathcal{D}$$はデータセットである。エキスパートの軌跡を模倣する確率モデル$$q(\mathbf{S} \mid \phi)$$ は遷移確率の積として表すことができる。
$$
q(\mathbf{S})= \prod_{t=1}^T q(\mathbf{S}_t \mid \mathbf{S}_{1:t-1}, \phi)
$$

各エージェントの遷移確率を正規分布と仮定すると、すべてのエージェントの遷移確率およびエージェント$$a$$の状態遷移は次で表せる。
$$
q(\mathbf{S}_t \mid \mathbf{S}_{1:t-1}, \phi)
= \prod_{a=1}^A
\mathcal{N}(\mathbf{S}_t^a ; \mu_t^a, \sigma_t^a{\sigma_t^a}^{\top})
$$

$$
\mathbf{S}_{t}^{a} = f(\mathbf{Z}_t^a) = \mu_{\theta}^a(\mathbf{S}_{1:t-1}, \phi) + \sigma_{\theta}^a(\mathbf{S}_{1:t-1}, \phi) \cdot \mathbf{Z}_t^a
$$

$$f(\cdot)$$は観測$$\phi$$および正規分布に従う潜在変数$$\mathbf{Z}_t^a$$から計画$$\mathbf{S}$$にワープする可逆かつ微分可能な関数、$$\mathbf{Z}_t$$ : 正規分布に従う潜在変数$$\mathbf{Z} \sim q_0 = \mathcal{N}(0, I)$$、$$\mu_{\theta}^a(\cdot)$$および$$\sigma_{\theta}^a(\cdot)$$は状態$$\mathbf{S}_{t}$$の平均および分散を出力するネットワーク関数である。パラメータ$$\theta$$はエキスパートの軌跡を模倣する確率モデル$$q(S \mid \phi;\mathcal{D})$$ を尤度を最大化して求められる。

ESPによる予測は次の通りである。

1. K個のすべてのエージェントの潜在変数$$^{1:K}\mathbf{z}$$をサンプリングする

    $$^{1:K}\mathbf{z}_{1:T}^{1:A} \overset{iid}{\sim} \mathcal{N}(0, I)$$

2. 潜在空間からワープする

   $$^{1:K}\mathbf{s}_{1:T}^{1:A} \leftarrow f(^{1:K}\mathbf{z}_{1:T}^{1:A}, \phi) $$

### ネットワークアーキテクチャ(詳細はAppendix C)

エージェントが２個の場合の状態$$\mathbf{S}_{t}$$の平均および分散を出力するESPのアーキテクチャを示す。RNN(GRU)とCNNはそれぞれ$$\mathbf{s}_{-\tau:0}$$と$$\chi$$を処理して$$\alpha$$と$$\Gamma$$を出力する。各エージェントごとに$$\alpha$$、$$\mathbf{s}_t$$、$$\Gamma(\mathbf{S}_{t}^a)$$および$$\lambda$$はConcatenationされ、RNN(GRU)により処理される。$$\Gamma(\mathbf{S}_{t}^a)$$は、位置$$\mathbf{S}_{t}^a$$に対応したサブピクセルにもどづいてbilinear保管された特徴ベクトルである。RNNは位置を直接出力する代わりにベレの方法([wiki](https://en.wikipedia.org/wiki/Verlet_integration))のステップ$$m_{\theta}^a(\mathbf{S}_{1:t-1}, \phi)$$と位置の分散$$\sigma_{\theta}^a(\mathbf{S}_{1:t-1}, \phi)$$を出力する。位置の平均は次式で計算できる。
$$
\mu_{\theta}(\mathbf{S}_{1:t-1}, \phi) = 2 \mathbf{S}_{t-1} - \mathbf{S}_{t-2} + m_{\theta}(\mathbf{S}_{1:t-1}, \phi)
$$
<img src="/home/x/Workspace/matomEmotam/papers/PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings/EmbeddedImage.png" alt="EmbeddedImage" style="zoom: 50%;" />

### PREdiction Conditioned On Goals (PRECOG)

エージェント（自車両）が設定したゴールに止まるような制御変数$$z^{r*}$$を次の最適化問題を解く(プランニングする)ことで求めたあと、ESPと同様に自車両以外のエージェントの決定をサンプリングし、予測を行う。
$$
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator*{\argmax}{arg\,max}
\begin{equation}
z^{r *} = \argmax_{z^r} \mathcal{L}(\mathbf{z}^r, \mathcal{G}, \phi)
\end{equation}
$$
$$\mathcal{L}(\mathbf{z}^r, \mathcal{G})$$はマルチエージェントの模倣尤度とゴールの尤度の和の期待値
$$
\mathcal{L}(\mathbf{z}^r, \mathcal{G}, \phi) = \mathbb{E}_{\mathbf{Z}^h} \left[ \log q(f(\mathbf{Z}) \mid \phi) + \log q(\mathcal{G} \mid f(\mathbf{Z}), \phi) \right]
$$
である。実際にはこの最適化問題は解くとき、他エージェントの潜在変数$$\mathbf{Z}^h$$を正規分布$$\mathcal{N}(0, \mathbf{I})$$からサンプリングしてゴールの尤度による重み付き平均を行うことで期待値の近似を行う。近似された期待値は
$$
\hat{\mathcal{L}}(\mathbf{z}^r, \mathcal{G}, \phi)
= \frac{1}{K} \sum_{k=1}^{K}
\log(
p(f(^k\mathbf{z}) \mid \phi)
p(\mathcal{G} \mid f(^k\mathbf{z}), \phi)
)
$$
である。$$^{1:K}\mathbf{z}$$はサンプリングされたK個のすべてのエージェントの潜在変数である。$$^{k}\mathbf{z}$$は最適化問題で求める制御変数$$\mathbf{z}^r$$と$$k$$番目のサンプリングが含まれている。$$^k\mathbf{z}=[\mathbf{z}^r, ^k\mathbf{z}^h]$$。

この近似期待値をつかったGradient Ascentによるアルゴリズムは次のとおりである。

![multimitativeplanning](./multimitativeplanning.png)

この制御変数$$z^{r*}$$を使った予測は次のとおりである

![precog_algorithm](./precog_algorithm.png)

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
