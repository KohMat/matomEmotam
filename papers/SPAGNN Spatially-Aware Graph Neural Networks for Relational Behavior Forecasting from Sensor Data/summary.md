# [日本語まとめ] SPAGNN: Spatially-Aware Graph Neural Networks for Relational Behavior Forecasting from Sensor Data

[Sergio Casas](https://arxiv.org/search/cs?searchtype=author&query=Casas%2C+S), [Cole Gulino](https://arxiv.org/search/cs?searchtype=author&query=Gulino%2C+C), [Renjie Liao](https://arxiv.org/search/cs?searchtype=author&query=Liao%2C+R), [Raquel Urtasun](https://arxiv.org/search/cs?searchtype=author&query=Urtasun%2C+R)

* [arxiv](https://arxiv.org/pdf/1910.08233.pdf)
* [ieee](https://ieeexplore.ieee.org/document/9196697)

## どんなもの？

自動運転のために、環境中にいる車両などのエージェントの合理的な行動の予測を行うSpAGNN (spatially-aware graph neural network)を提案する。SpAGNNは環境内のエージェント間の相互作用を捉えたモデルである。Gaussian belief propagationと同じようにメッセージ伝達によって繰り返し伝播し、ノードである各エージェントの状態を更新する。そして更新した状態から予測経路を計算する。予測経路の各点は正規分布やフォンミーゼス分布などのパラメータである。SpAGNNはCNNで構成される物体検出器の後段に接続される。一連のモデルはセンサー信号からEnd-to−Endで予測の実行および訓練することができる。

![qualitative](./qualitative.png)

## 先行研究と比べてどこがすごい？何を解決したか？

- 提案手法は物体検出と経路予測を一つのネットワークで行う。検出が完璧であると仮定している既存の予測アプローチとは異なる。
- エージェント間の相互作用とくに空間的関係を考慮するため、空間認識グラフニューラルネットワーク(SpAGNN)を使う。Ablation StudyにおいてSpAGNNの代わりに標準のGNNを用いた場合性能が低くなることを示した。空間認識を行うことで性能が上がることからSpAGNNの利点を示した。
- SpAGNNを使ったモデルはATG4DおよびnuScenceの検出も含めた予測タスクでstate-of-the-artの性能を上回った。

## 手法は？

図に示すようにセンサーデータからバックボーン（図の上段左半分）により特徴量を計算し、物体検出（図の上段右半分）と予測（図の下段）を行う。全体の処理時間は0.1秒である。SpAGNNは現在から３秒後までの経路を予測する。

![spagnn_diagram](./spagnn_diagram.png)

### バックボーンと入力表現

CNNで特徴量の計算を行うため、LIDARの点群とHDマップの道路構造物をボクセル化する。ボクセル化の方法は俯瞰図を使った物体検出法PIXOR([arxiv](https://arxiv.org/abs/1902.06326))と同じ方法を使う。つまりLIDARとHDマップをCNNで処理できるように俯瞰図でラスタライズする。道路やレーン、交差点、横断歩道、標識、信号の状態など様々な情報が17チャンネルに渡って描画する。LIDARの点群は点群の高さに応じて違うチャンネルの俯瞰図に描画する。またモデルが物体の動きの特徴量を計算できるようにするため、現在時刻のLIDARの点群だけでなく過去の点群も使う。自己車両の動きを考慮して過去のLIDARの点群を現在フレームの車両中心に変換した後、ボクセル化を行う。

バックボーンの処理は次のとおりである。

1. ボクセル化されたLIDARの点群とHDマップの道路構造物から$$\text{CNN}_L$$および$$\text{CNN}_M$$を使い、LIDARの点群およびHDマップの特徴量を計算する。
2. 計算した特徴量をチャンネル次元でconcatenationする。
3. $$\text{CNN}_F$$で統合された特徴量を計算する。

$$\text{CNN}_L$$、$$\text{CNN}_M$$、$$\text{CNN}_F$$はPIXORと同じアーキテクチャを使う。ただし計算量削減のためレイヤーの数を減らしたものを使う。

### 物体検出

バックボーンで計算した特徴量から２つのCNNヘッダーを使いConfidence map (背景 or 車) $$c_i$$とバウンディングボックス$$b_i = (x, y, w, h, \sin(\theta), \cos(\theta))$$を計算する。No maximum suppressionを使い、物体として検出するバウンディングボックス数を絞る。

### Gaussian MRFとGraph Neural Network

合理的な行動の確率的な予測方法としてGaussian MRFを用いる方法がある。この方法はあるシーン$$\Omega$$の条件のもとのマルチエージェントの将来の経路$$\{ s_1, \dots, s_N \}$$の同時確率多変量正規分布であると仮定して次のようにモデル化する。

$$p(s_1, \dots, s_N \mid \Omega) \propto \exp( \mathbf{s} ^\intercal \mathbf{A} \mathbf{s} + \mathbf{b} ^\intercal \mathbf{s})$$

各エージェントが相互に関係しあっている仮定すると同時確率は単項ポテンシャルエネルギー$$\phi_i (s_i, \Omega)$$とペアごとのポテンシャルエネルギー$$\psi_{ij} (s_i, s_j \Omega)$$を使って次のように変形できる。つまり各予測経路をノードとした無向グラフで表現する。

$$p(s_1, \dots, s_N \mid \Omega) \propto
\prod_i \phi_i (s_i, \Omega) \prod_{ij} \psi_{ij} (s_i, s_j \Omega)$$

このモデルからエージェントがある経路をとる周辺確率$$p(s_i \mid \Omega)$$は周辺確率をGaussian Belief Propagation、もっと詳しくいえばメッセージ伝達法で求めることができる。メッセージ伝達方法は隣接しているノード間にメッセージを定義する。そしてそのメッセージをポテンシャルを用いて繰り返し収束するまで更新する方法である。収束後はメッセージから目的の周辺確率を計算する。

一方でGNNはグラフを処理できる強力なモデルである。入力のグラフのサイズにモデルサイズが影響しない。ノード単体およびグラフレベルの両方でよい表現を学ぶ能力がある。GNNは与えられた初期グラフとノードの状態からのメッセージを伝達してノードの状態を更新する。仮にGNNのノードが正規分布の平均と精度行列であるとすると、GNNの処理はGaussian BPアルゴリズムに非常に近い処理となる。このとき、ニューラルネットワークの持つ近似能力により、GNNはGaussian BPの一般系とみなすことができる。Gausiann BPが保証するように、GNNは周辺分布の収束を保証しないものの、以下の利点がある。

* GNNはバックプロパゲーションで訓練できる
* 正規分布に従わないデータを処理できる（車のヘディング角など）

### Spatially-Aware Graph Neural Networksによる予測

SpAGNNのアルゴリズムはノードの状態初期化(2〜5行目)とノードの状態更新ステップ(8~14行目)で構成される。SpAGNNは各エージェント$$v$$をグラフのノードとして処理する。各ノードは隠れ状態$$h_v^{(k)}$$と出力状態$$o_v^{(k)}$$の2つの状態を持つ。$$(k)$$は伝播回数である。隠れ状態はサイズ512の特徴ベクトルである。出力状態$$o_v^k$$はそのエージェントの予測経路である。予測経路は2次元位置とヘディングで構成される。2次元位置は正規分布のパラメータ$$\mu_{x_v}^{(k)}, \mu_{y_v}^{(k)},\sigma_{x_v}^{(k)},\sigma_{y_v}^{(k)}$$、ヘディングはフォンミーゼス分布のパラメータ$$\eta_v^{k},\kappa_v^{k}$$で表現される。また予測経路の位置およびヘディングは常にそのエージェントの座標系で表される。エージェントの座標系に設定することでグローバル座標系で設定するより予測タスクの学習が簡単になることが理由である。

![algorithm](./algorithm.png)

#### ノードの状態初期化(2〜5行目)

物体検出により検出したエージェントからグラフのノードの状態$$h_v^{(0)},o_v^{(0)}$$を次の手順で初期化する。

* （3行目）J. Maらによって“Arbitrary-oriented scene text detection via rotation proposals”で提案されたRotated Region of Interest Align (RRoI Align)を使う。検出した位置およびヘディングを中心にエージェントの前31m、後ろ10m、左右12.5mの41m×25mに対応する範囲をバックボーンで計算された特徴マップから抽出する。
* （4行目）抽出された特徴マップを4層のCNNとmaxpoolingを使って隠れ状態$$h_v^{(0)}$$に変換する。
* （5行目）隠れ状態から2層のMLPを使い出力状態$$o_v^{(0)}$$を計算する。

#### ノードの状態更新(8~14行目)

ノードの状態更新を次の手順でK回更新する。実装ではK=3で固定する。

* （10行目）グラフのすべてのエッジ$$u \rightarrow v$$のメッセージ$$m_{u \rightarrow v}^{(k)}$$を計算する。$$\mathcal{E}^{(k)}$$は3層MLPである。$$\mathcal{T}_{u,v}$$はエージェント$$u$$から$$v$$への座標変換である。エージェント$$u$$の予測経路$$o_u^{(k-1)}$$をエージェント$$v$$の座標に変換してから$$\mathcal{E}^{(k)}$$に入力する。座標変換なしのモデルが空間的な情報を学習することは非常に厳しい。座標変換することでモデルがエージェント間の空間的な関係を認識することができる。また$$\mathcal{E}^{(k)}$$にバウンディングの情報$$b_u, b_v$$を入力する。バウンディングの情報はメッセージを受信するエージェント$$v$$の座標系で変換してから入力する。
* （12行目）ノードの特徴量$$a_v^{(k)}$$を計算する。隣接しているすべてのノードとのメッセージを集約する。$$\mathcal{A}^{(k)}$$をmax poolingで実装する。
* （13,14行目）ノードの特徴量とk-1回目の隠れ状態からk回目の隠れ状態、出力状態を計算する。$$\mathcal{U}^{(k)}$$はGRU cell、$$\mathcal{O}^{(k)}$$は2層のMLPである。

### 学習

SpAGNNを含めたすべてのモデルをend-to-endで学習する。バックプロパゲーションを使い、物体検出と経路予測のマルチタスク損失を最小化する。検出に関する損失は次の２つの損失で構成される。

* 物体検出の分類ヘッドに対して正しいラベルとのバイナリークロスエントロピー損失

  hard negative mining（[reddit](https://www.reddit.com/r/computervision/comments/2ggc5l/what_is_hard_negative_mining_and_how_is_it/), [qiita](https://qiita.com/mshinoda88/items/9770ee671ea27f2c81a9#%E3%83%8F%E3%83%BC%E3%83%89%E3%83%8D%E3%82%AC%E3%83%86%E3%82%A3%E3%83%96%E3%83%9E%E3%82%A4%E3%83%8B%E3%83%B3%E3%82%B0hard-negative-mining)）を適用して、正負のデータの不均衡を改善する。

* 物体検出の回帰ヘッドに対して正しい物体の状態とのL1損失

経路予測に関する損失は予測経路に対する負の対数尤度を使う。

$$\begin{align}
\mathcal{L}_{nll} &=
\sum_{i=1}^{N} \sum_{t=1}^{T} \frac{1}{2} \log \left| \Sigma_{i,t} \right| +
\frac{1}{2} (x_{i,t} - \mu_{i,t})^{\text{T}} \Sigma_{i,t}^{-1} (x_{i,t} - \mu_{i,t}) \\ &-
\kappa_{i,t} \cos(\theta_{i,t} - \eta_{i,t}) +
\log (2 \pi I_0 (\kappa_{i,t}))
\end{align}$$

第１行目は２次元位置に対する２次元正規分布のNLLである。第２行目はヘディングに対する1次元のフォン・ミーゼス分布のNLLである。$$I_0$$は零次の変形ベッセル関数である。

最適化手法はAdamを使う。また学習初期は検出の精度が良くない事実がある。精度が悪い検出結果を元に予測ネットワークを学習すると、ネットワークのパラメータが悪い方向に導かれる可能性がある。学習初期である10000回までは予測ネットワークの学習に真のアクターを使う。

## どうやって有効だと検証した？

### 予測性能の比較

センサデータから環境中にいるエージェントの検出を行い、検出したエージェントの経路を予測するタスクでSpAGNNの性能を検証した。比較手法であるSocial LSTM、Convolutional Social Pooling、CAR-Netは検出されたアクターから予測を行う方法である。検出器を持たないため、SpaGNNで用いる検出器を使用した。

メトリックとして手法がエージェント間の相互作用を表しているかどうかを示すcummative collision rate over timeおよび経路のセントロイドのL2距離、ヘディング誤差を使用した。これらのメトリックは真の将来の経路と経路を予測する検出した物体が同じ場合にのみ計算できる。つまり検出した物体が正しいかどうか、検出器のリコール率が予測の評価に関わってくる。予測性能を公平に比較するため、比較手法およびSpGNNで用いる検出器で検出された物体に対してコンフィデンススコアの閾値を設定した。閾値以下のコンフィデンススコアを持つ物体を省くことで、異なる検出器が同じリコール値で動作するようにした。

ATG4DおよびnuScenes上での比較結果は次のとおりである。SPAGNNがほとんどのメトリックで最も良い性能を示した。この結果より検出と予測を一緒に行うこと、予測で相互作用を捉える利点を示している。

![result](./result.png)

### Ablation Study

Ablation Studyの結果を示す。

![ablation_study](./ablation_study.png)

##### Study 1 Rotated ROI Alignの有効性

Rotated ROI Alignの有効性を調べた。Rotated ROI Alignの代わりにFeature Indexingによる特徴マップからの抽出方法による性能を検証した。検証する際、抽出方法を比べるため提案モデルからSpAGNNを除いたモデルを評価した。上記の表の１行目がFeature Indexingによる方法（R✗）、２行目がRotated ROI Alignを用いる方法（R✔）による結果である。Rotated ROI Alignを用いた方法のが良いことがわかる。バックボーンが計算した特徴マップから車の位置に対応する１点の特徴ベクトルのみを抽出するFeature Indexingに比べてROIで抽出する利点が示されている。

##### Study 2 SpAGNNの有効性

SpAGNNに使われるspatial awarenessの有効性を調べた。表の３〜６行目がその結果である。

３行目は２行目のモデルに対して空間情報をGNNを加えたモデルの予測結果である。このモデルはメッセージ伝達の伝播式において隠れ状態のみを$$\mathcal{E}^{(k)}$$の入力とする。表より２行目のGNNをもたないモデルの結果と比較して性能の優劣がないことがわかる。単にGNNを追加しても性能が上がらないことを示している。

４行目は３行目のモデルに対してメッセージ伝達の伝播式に検出されたバウンディングの情報を加えた結果である。メッセージ反復にバウンディングボックスという空間の情報を加えることで性能の改善が見られる。

５行目は４行目とほぼ同じである。４行目のモデルと異なる点は、バウンディングの情報がグローバル座標系でなくメッセージを受信するエージェントを中心とした座標系で表現される点である。

６行目は提案しているSpAGNNを用いたモデルの結果である。５行目のモデルに対してメッセージ伝達の伝播式に相対的な経路を加えてたモデルである。

## 課題は？議論はある？

SpAGNNのモデルを

* シーンの複数の将来の結果を生成する
* 画像やレーダーなどの他のセンサーを使用する
* 車だけでなく歩行者や自転車などのエージェントの経路も含めて推論する

Conditioned on the observed input and detection output, we assume the future states can be predicted independently for different future time steps. How to explore temporal dependency is left as future work.

## 次に読むべき論文は？

[Deep Structured Reactive Planning](../Deep Structured Reactive Planning/summary.md)

## 補足

なし

## 個人的メモ

なし
