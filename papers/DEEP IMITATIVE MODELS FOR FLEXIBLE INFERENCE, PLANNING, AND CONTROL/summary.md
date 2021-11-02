# [日本語まとめ] Deep Imitative Models for Flexible Inference, Planning, and Control

Nicholas Rhinehart, Rowan McAllister, Sergey Levine

* [Published as a conference paper at ICLR 2020](https://openreview.net/pdf?id=Skl4mRNYDr)
* [Arxiv 1st Oct. 2019](https://arxiv.org/pdf/1810.06544.pdf)
* [github](https://github.com/nrhine1/deep_imitative_models)
* [site](https://sites.google.com/view/imitative-models) [結果](https://sites.google.com/view/imitative-models)を動画で見ることができる

## どんなもの？

模倣学習は行動を模倣するモデルを訓練するフレームワークである。訓練された模倣モデルはテスト時に望ましい最良の推測を行う。しかし、目標を達成するようにモデルに指示することはできない。一方でダイナミクスモデルを使い、目的を達成するように目的関数を最小化するアプローチMBRL (Model Based Reinforcement Learning)は自由に目標を達成できる。しかし目的関数の設計が難しい。特に目標の達成よりも望ましい行動の設計に試行錯誤を必要とする。複雑な行動であればあるほどその設計難易度は高い。

この論文は模倣学習とMBRLの利点を組み合わせた方法Deep Imitative Models(DIM)を提案する。DIMは模倣モデルによる望ましい行動の生成と、目的関数を使用して任意の目標の設定ができる。DIMは模倣モデル $$q(\mathbf{S} \mid \phi)$$ を通常通りエキスパートの軌跡を模倣するように訓練する。そしてMBRLの目的関数内のダイナミクスモデルの代わりに訓練した模倣モデルを使う。DIMの目的関数は探索している行動がどれだけエキスパートに近いかを示す尤度と、目標への近さを示すゴール尤度で構成される。目的関数を最大化することで、実行時にゴールを達成しつつエキスパートらしい行動を求めることができる。

$$\mathbf{s}^{*} \doteq \underset{\mathbf{s}}{\text{argmax}}\ \underbrace{\log q(\mathbf{s} \mid \phi)}_\textrm{imitation prior} + \underbrace{\log p(\mathcal{G} \mid \mathbf{s}, \phi)}_\textrm{goal likelihood}$$

## 先行研究と比べてどこがすごい？何を解決したか？

* 今までの模倣学習による方法は訓練時に目標の設定を必要としていた。そしてその目標の設定は直進、右左折など簡単なものに限られていた。DIMはこの問題を解決した。実行時に新しいゴールの設定を柔軟に行うことができる。

* MBRLで目的関数の設計が複雑となっていた原因である、望ましい行動を行うための目的関数の設計を省くことができる。DIMでは目標を達成するための目的関数の設計だけで良いため、設計の難易度が下がる。
* 目標がノイズを持つ場合でもロバストに機能することができる。

* 自動運転車シミュレーターであるCARLA上で自動運転を行い、性能を検証した。DIMは６つのILとMBRL（モデルベース強化学習）の性能を上回った。またゴール尤度に車両が移動できる領域を設定することでpotholesなどの特定の物体を避けるような計画を行うことができた。

  ![goalsettings](./goalsettings.png)

## 手法は？

連続空間、離散時間、POMDPの仮定をおく。時刻$$t$$におけるエージェントの状態（2次元位置）を$$\mathbf{s}_t \in \mathbb{R}^{D}$$とする。また観測を$$\phi$$とする。変数をボールド、実数値を小文字、確率変数を大文字とする。$$\mathbf{s}=\mathbf{s}_{1:T}$$とする。

DIMは訓練済みのエキスパートの行動を模倣する生成モデル$$q(\mathbf{S} \mid \phi)$$を使い、実行時に目標$$\mathcal{G}$$に到達するエキスパートらしい行動$$\mathbf{s}^{*}$$を次の最適化問題を解くことで求める。

![imitaive_planning_to_goals](./imitaive_planning_to_goals.png)

第１項はエージェントの行動$$\mathbf{s}$$がエキスパートに近いほど高い値となる模倣尤度である。第二項は行動$$\mathbf{s}$$がゴール$$\mathcal{G}$$に近いほど高い値となるゴールの尤度である。この最適化問題はGradient ascentで解くことできる。

![imitative_plan](./imitative_plan.png)

変数$$\mathbf{z}$$は生成モデルの潜在変数である。関数$$f(\cdot)$$は観測$$\phi$$と潜在変数$$\mathbf{z}_t$$から行動$$\mathbf{s}$$に変換する生成モデルの関数である。

$$\mathbf{Z} \sim q_0; \mathbf{S} = f(\mathbf{Z}; \phi)$$

関数$$f(\cdot)$$は可逆かつ微分可能である。アルゴリズムに示すように正規分布からサンプリングした潜在変数を使って経路を生成し、目的関数の値を評価する。そして評価した値から勾配を計算し、潜在変数を更新する。

## 生成モデル

DIMで使うモデルは次の条件を満たしている必要がある。

* 将来の行動を予測する
* エキスパートとの尤度$$q(\mathbf{S} \mid \phi)$$を計算する

例えば次のようなモデルである。

* Danilo Rezende and Shakir Mohamed. Variational inference with normalizing flows. In International
  Conference on Machine Learning (ICML), pp. 1530–1538, 2015.
* Aaron van den Oord, Yazhe Li, Igor Babuschkin, Karen Simonyan, Oriol Vinyals, Koray Kavukcuoglu,
  George van den Driessche, Edward Lockhart, Luis C Cobo, Florian Stimberg, et al. Parallel
  WaveNet: Fast high-fidelity speech synthesis. arXiv preprint arXiv:1711.10433, 2017.

論文内ではR2P2([summary](../R2P2: A reparameterized pushforward policy for diverse, precise generative path forecasting/summary.md))を使う。R2P2はフローベースの生成モデルである。自動運転のためにLIDARの点群を観測としてドライバーの行動$$\mathbf{S}$$を2次元点からなる経路として予測する。R2P2は時刻$$t-1$$から$$t$$への車の位置の遷移確率を正規分布で表現する。R2P2の関数$$f(\cdot)$$はドライバーの１ステップ先の更新式で構成される。

$$\mathbf{S}_{t} = f_{\theta}(\mathbf{Z}_t) = \mu_{\theta}(\mathbf{S}_{1:t-1}, \phi) + \sigma_{\theta}(\mathbf{S}_{1:t-1}, \phi) \cdot \mathbf{Z}_t$$

時刻1からTまで繰り返すことで将来の行動を出力する。関数$$\mu_{\theta}(\cdot)$$および$$\sigma_{\theta}(\cdot)$$は状態$$\mathbf{S}_{t}$$の平均および標準偏差を出力するネットワーク関数である。次の図は$$\mu_{\theta}(\cdot)$$および$$\sigma_{\theta}(\cdot)$$の具体的なアーキテクチャである。

![deep_imitative_model](./deep_imitative_model.png)

具体的な観測$$\phi \doteq \{\mathbf{s}_{-\tau:0}, \chi , \lambda\}$$は次のとおりである。

* $$\mathbf{s}_{-\tau:0}$$は過去から現在までの位置
* $$\chi = \mathbb{R}^{200 \times 200 \times 2}$$はLiDARの情報を俯瞰図で表現したもの(各グリッドの面積は$$0.5 m^2$$であり、地面の上と下にあるポイントの2ビンのヒストグラムである)
* $$\lambda$$は低次元の信号機の情報

モデルは次の手順で動作して計画$$\mathbf{s}_{1:T}$$もしくは$$\mathbf{z}_{1:T}$$を計算する。

1. 現在時刻で得られた観測からRNN(GRU)とCNNを使って特徴量$$\alpha$$と特徴マップ$$\Gamma$$を計算する

2. 時刻1からTまで以下のステップを繰り返す

   1. エージェントの位置$$\mathbf{s}_{t-1}$$に対応した空間特徴量$$\Gamma(\mathbf{s}_{t-1})$$をbilinear補間により特徴マップ$$\Gamma$$から取り出す

   2. 各特徴量$$\alpha$$、$$\mathbf{s}_t$$、$$\Gamma(\mathbf{s}_{t-1})$$および$$\lambda$$はConcatenationして特徴$$p_{t-1}$$を作成する

   3. 特徴$$p_{t-1}$$から予測用のRNN(GRU)を使い、ベレの方法([wiki](https://en.wikipedia.org/wiki/Verlet_integration))のステップ$$m_{\theta}$$と位置の標準偏差$$\sigma_{\theta}$$を計算する

   4. ベレの方法から位置の平均を計算する

      $$\mu_{\theta}(\mathbf{s}_{1:t-1}, \phi) = 2 \mathbf{s}_{t-1} - \mathbf{s}_{t-2} + m_{\theta}(\mathbf{s}_{1:t-1}, \phi)$$

   5. 潜在変数$$\mathbf{z}_t$$から状態$$\mathbf{s}_{t}$$を計算する。もしくは訓練時は状態$$\mathbf{s}_{t}$$から潜在変数$$\mathbf{z}_t$$を計算する。

      $$\mathbf{s}_{t} = \mu_{\theta}(\mathbf{s}_{1:t-1}, \phi) + \sigma_{\theta}(\mathbf{s}_{1:t-1}, \phi) \cdot \mathbf{z}_t$$

      $$ \mathbf{z}_t = \sigma_{\theta}(\mathbf{s}_{1:t-1}, \phi) ^{-1} (\mathbf{s}_{t} - \mu_{\theta}(\mathbf{s}_{1:t-1}, \phi))$$

### ゴール尤度の設計

MBRLのようにゴール尤度は自由に設計できる。例えばエージェントの目標がエージェントが達成するべき最終状態のセット$$\mathbb{G}$$で定義できるとき、ゴール尤度関数はディラックのデルタ分布を使って表現することができる。

$$p(\mathcal{G} \mid \mathbf{s}, \phi) \leftarrow \delta_{\mathbf{s}_T} (\mathbb{G}),\
\delta_{\mathbf{s}_T} = 1 \text{ if } \mathbf{s}_T \in \mathbb{G}, \
\delta_{\mathbf{s}_T} = 0 \text{ if } \mathbf{s}_T \notin \mathbb{G}$$

$$\mathbb{G}$$はエージェントが達成するべき最終状態のセットである。自動運転の場合、目的の道路を示すwaypointsやline segment、もしくは走行可能領域を$$\mathbb{G}$$とすることができる。またディラックのデルタ分布の代わりにガウシアン関数を使うこともできる。この場合、目標は必ず達成しなければならないものから奨励するべきものになる。その他には以下の2つの論文で提案されたエネルギーベースの尤度を使う方法がある。

* Emanuel Todorov. Linearly-solvable Markov decision problems. In Neural Information Processing Systems (NeurIPS), pp. 1369–1376, 2007
* Sergey Levine. Reinforcement learning and control as probabilistic inference: Tutorial and review. arXiv preprint arXiv:1805.00909, 2018.

エネルギーベースの尤度を使う方法は尤度を単純に乗算することにより、様々な尤度を組み合わせることができる。

$$p(\mathcal{G} \mid \mathbf{s}, \phi) \propto \prod_{t=1}^{T} e^{-c(\mathbf{s} \mid \phi)}$$

## どうやって有効だと検証した？

DIMを自動運転システムに適用し、CARLA上で性能を検証した。特に次の点について調べた。

1. 最低限の報酬関数の設計とオフライン学習によって解釈可能なエキスパートのような計画を生成できるか？この手法が有効であるか？
2. 実際の車両の設定のもとでstate-of-the-artの性能を達成できるか？
3. 新しいタスクに対してどれだけ柔軟であるか？
4. ゴール設定へのロバスト性はどれだけあるか？

![PathPlanning](./PathPlanning.png)

### 検証1  性能

様々なゴール尤度の設定のImitative PlanningをCALRA上で実行した。StaticおよびDynamicな環境のいずれも、いくつかの手法の性能を上回った。この結果からの質問1,2に対して肯定的な回答(affirmative answers)を示している。

![start_of_art_result](./start_of_art_result.png)

### 検証2  ゴールノイズに対するロバスト性

ゴールにノイズを混ぜた状況でナビゲーションするテストを行った。

1. waypointsからなるゴールの半分を、大きく変動
2. ゴールを対向車線に設定

以上のいずれの場合も高い確率でナビゲーションを成功させることができた。このことから質問４に対する回答はYesである。

### 検証3  potholeの回避

potholeに対する回避実験を行った。Gaussian Final-State Mixtureおよび) Energy-based likelihoodを組み合わせたゴール尤度を使用することでランダムに設置されたpotholeをセンターラインに近づいたり、時には反対レーンに行くなどして避けることができた。

### 検証4  経路計画の信頼度推定

モデルが陽に計画の尤度を計算することができるのでモデルが計画を安全でない計画を正しく判断できるかの実験を行った。エキスパートが実際に行った良好なwaypointと道路外にある悪いwaypointが含まれる1650のテストケースに対してリコール97.5％、精度90.2%を示した。

またあるウェイポイントが計算した計画の信頼区間に含まれる確率、すなわち信頼度を検証した。信頼区間は、計画の基準の平均値から1標準偏差を引いた値を計画の基準の閾値とした区間である。

1. エキスパートが時間Tに実際に到着したウェイポイントは89.4%
2. 提供されたルートに沿って20m進んだ先のウェイポイントは73.8%
3. 2)のウェイポイントから2.5mずれたウェイポイントは2.5%

この結果から有効なウェイポイントを正しく判定する傾向があることがわかる。

### 検証5(課題) 信号のノイズに対するロバスト性

20％の確率で緑を赤に、赤を緑に変更するノイズを加えた状態で実験を行った。概ね成功しているものの、赤信号に対してより違反を行うという傾向が見られた。また交差点付近で停止と発進を繰り返し行う挙動が見られた。ノイズを加えた状態で訓練することによりよりロバストになる可能性がある。

![traffic_light_noise](./traffic_light_noise.png)

## 課題は？議論はある？

ゴールノイズに対する実験でノイズとして入れたwaypointが交差点内の有効な場所ではあるが、目的地へ向かう方向ではない場所に設定されたときに、プランナが一時的に最適なルートを生成できないことがある。

観測のノイズおよび分布外の観測に対するロバスト性に対していくつかの課題がある。

1. 観測ノイズに関するロバスト性である。提案モデルは現在の観測のみを予測に使っているため、ベイジアンフィルタリングを使うことで観測ノイズを軽減できるかもしれない。しかしながら高次元のフィルタリングは多くの場合手に負えないので、ディープラーニングをつかった近似ベイジアンフィルタリングを行う必要がある。
2. 訓練データ分布外の観測に関するロバスト性である。これに対応するためにはDeep Ensemble Networkを使う方法が考えられる。

> Balaji Lakshminarayanan, Alexander Pritzel, and Charles Blundell. Simple and scalable predictive uncertainty estimation using deep ensembles. In Neural Information Processing Systems (NeurIPS), pp. 6402–6413, 2017.

## 次に読むべき論文は？

[A. Filos, P. Tigas, R. McAllister, N. Rhinehart, S. Levine, and Y. Gal, “Can autonomous vehicles identify, recover from, and adapt to distribution shifts?” arXiv preprint arXiv:2006.14911, 2020.](../Can autonomous vehicles identify, recover from, and adapt to distribution shifts/summary.md)

[N. Rhinehart, R. McAllister, K. Kitani, and S. Levine, “PRECOG: prediction conditioned on goals in visual multi-agent settings,” in Proceedings of the IEEE International Conference on Computer Vision, 2019, pp. 2821–2830.](../PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings/summary.md)

## 個人的メモ

* 論文中にいくつかのゴール尤度関数が提案されている。
* ゴール内の尤度とエキスパートの尤度のバランスはどうしたらいいだろうか？



