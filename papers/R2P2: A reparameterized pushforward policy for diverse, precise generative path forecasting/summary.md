# (WIP)R2P2: A reparameterized pushforward policy for diverse, precise generative path forecasting

[Nicholas Rhinehart](https://people.eecs.berkeley.edu/~nrhinehart/), Kris M. Kitani, and Paul Vernaza

* [ECCV 2018](https://link.springer.com/chapter/10.1007/978-3-030-01261-8_47)
* [link 1](https://people.eecs.berkeley.edu/~nrhinehart/papers/r2p2_cvf.pdf)
* [site](https://people.eecs.berkeley.edu/~nrhinehart/R2P2.html#:~:text=R2P2%3A%20A%20ReparameteRized%20Pushforward%20Policy%20for%20Diverse%2C%20Precise%20Generative%20Path%20Forecasting,-Nicholas%20Rhinehart%2C%20Kris&text=The%20method%20learns%20a%20policy,paths%20likely%20under%20the%20data)
* [blog post (third-party)](https://medium.com/analytics-vidhya/game-of-modes-diverse-trajectory-forecasting-with-pushforward-distributions-315b1b30d5e6)
* [summarized](http://cvrr.ucsd.edu/ece285sp20/files/r2p2.pdf)

## どんなもの？

LIDARや画像などの情報が埋め込まれた俯瞰図から自車両の運動を時空空間上のパスの分布として予測する方法を提案する。確率的軌道予測において以前から過小評価されていた多様性(データ分布のすべてのモードを含む)と精度(データに有り得そうな)のバランスに関する問題を提起し、その問題を対称化されたクロスエントロピーを最適化することで多様性と精度と確保した予測を行えることを示す。対称化されたクロスエントロピーを計算するために、単純な基本分布の押し出し（pushforward)としてモデル分布をパラメータ化する。この最適化を行うことで既存の模倣学習の性能を強化することを示した。またKITTおよび提案する現実世界のデータセットCaliForecasting上でstate-of-artの手法と比較して提案手法の優位性を示した。

## 先行研究と比べてどこがすごい？何を解決したか？

Write a content that can be read within 30~1 minute.

## 手法は？

### 確率的軌道予測における多様性と精度のバランスの問題



### Pushforward distribution modelingとデータ分布の事前近似



### Policyのモデリング



## どうやって有効だと検証した？



## 課題は？議論はある？

eeee

## 次に読むべき論文は？

[N. Rhinehart, R. McAllister, K. Kitani, and S. Levine, “PRECOG: prediction conditioned on goals in visual multi-agent settings,” in Proceedings of the IEEE International Conference on Computer Vision, 2019, pp. 2821–2830.](../PRECOG: PREdiction Conditioned On Goals in Visual Multi-Agent Settings/summary.md)

[Nicholas Rhinehart, Rowan McAllister, and Sergey Levine. Deep imitative models for flexible inference, planning, and control. arXiv preprint arXiv:1810.06544, 2018. 2, 4, 13](../DEEP IMITATIVE MODELS FOR FLEXIBLE INFERENCE, PLANNING, AND CONTROL/summary.md)