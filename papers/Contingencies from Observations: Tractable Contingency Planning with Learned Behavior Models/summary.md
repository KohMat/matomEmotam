# Contingencies from Observations: Tractable Contingency Planning with Learned Behavior Models

[Nicholas Rhinehart](https://arxiv.org/search/cs?searchtype=author&query=Rhinehart%2C+N), [Jeff He](https://arxiv.org/search/cs?searchtype=author&query=He%2C+J), [Charles Packer](https://arxiv.org/search/cs?searchtype=author&query=Packer%2C+C), [Matthew A. Wright](https://arxiv.org/search/cs?searchtype=author&query=Wright%2C+M+A), [Rowan McAllister](https://arxiv.org/search/cs?searchtype=author&query=McAllister%2C+R), [Joseph E. Gonzalez](https://arxiv.org/search/cs?searchtype=author&query=Gonzalez%2C+J+E), [Sergey Levine](https://arxiv.org/search/cs?searchtype=author&query=Levine%2C+S)

* International Conference on Robotics and Automation (ICRA), 2021
* [arxiv](https://arxiv.org/abs/2104.10558)
* [project site](https://sites.google.com/view/contingency-planning/home) まとめ。ここを見たほうが早い。様々な動画がある。
* [github](https://github.com/JeffTheHacker/ContingenciesFromObservations)

## どんなもの？

Contingency Planning(不測の事態に備えた計画)を行う行動モデルを提案する。このモデルは環境内のマルチエージェントの相互作用による行動を表す画像条件付き自己回帰フローモデルである。このモデルは将来の軌道を予測することで訓練される。このモデルを使ったPlanningは過去に見たことのない場所での不測の事態が起きるシナリオで様々なnon-contingentのプランニング方法の性能を凌駕した。

## 先行研究と比べてどこがすごい？何を解決したか？



CARLAを用いて過去に見たことのない場所での不測の事態が起きるシナリオでCfO Plannerは様々なnoncontingentのプランニング方法の性能を凌駕した。

## 手法は？



## どうやって有効だと検証した？

dddd

## 課題は？議論はある？

eeee

## 次に読むべき論文は？

なし

## 補足

### Contingency planningについて (Introductionから作成)

車を運転するには例えば次の３つが求められる。

1. どのように車が動くかの予測ダイナミクスモデル
2. ドライバーの反応の予測モデル
3. 他のドライバーの意図の不確実性を解決し、計画する能力

条件1〜３を満たす自律システムとして

* [Stanley: The robot that won the DARPA Grand Challenge](http://robots.stanford.edu/papers/thrun.stanley05.pdf)
* [Autonomous driving in urban environments: Boss and the urban challenge](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/rob.20255)

がある。これらのシステムは予測と計画を異なるモジュールで行い、マルチエージェント環境で動作する。しかし、このモジュール構成は正確な認識に依存しており、未解決の課題となっている。

生センサの情報からマルチエージェント環境下でナビゲーションを行う学習ベースのEnd-to-Endシステム(例えば[DIM](../DEEP IMITATIVE MODELS FOR FLEXIBLE INFERENCE, PLANNING, AND CONTROL/summary.md))が最近の研究で注目されている。しかしながらこれらの方法はその他のエージェントの行動をモデル化しないため、条件３を満たさない。

可能性があるシステム構成のアプローチとして他のエージェントの行動を予測するモデルをつくり、このモデルをつかった"open-loop"アクションのプランを計画するアプローチがある。しかしこの方法はロボットの行動に対して他のエージェントがどのように反応するか、他のエージェントの行動によってロボットの行動がどう変化するか(共依存性)を無視している。このアプローチは"fronzen robot problem"として知られる自信不足の行動につながる可能性がある。

これらから予測と行動を切り離して考えるのはモデル化の前提として不適切である。この共依存性を考慮する方法として予測した未来の行動や環境に適応するContingency Planningがある。以前のContingency Planningに関する研究は以下のものがある。

1. J. Hardy and M. Campbell, “Contingency Planning Over Probabilistic Obstacle Predictions for Autonomous Road Vehicles,” IEEE Transactions on Robotics, vol. 29, no. 4, pp. 913–929, 2013.
2. W. Zhan, C. Liu, C.-Y. Chan, and M. Tomizuka, “A non-conservatively defensive strategy for urban autonomous driving,” in International Conference on Intelligent Transportation Systems (ITSC). IEEE, 2016, pp. 459–464.
3. E. Galceran, A. G. Cunningham, R. M. Eustice, and E. Olson, “Multipolicy decision-making for autonomous driving via changepoint-based behavior prediction: Theory and experiment,” Autonomous Robots, vol. 41, no. 6, pp. 1367–1382, 2017. 
4. J. F. Fisac, E. Bronstein, E. Stefansson, D. Sadigh, S. S. Sastry, and A. D. Dragan, “Hierarchical Game-Theoretic Planning for Autonomous Vehicles,” in International Conference on Robotics and Automation (ICRA), 2019, pp. 9590–9596.