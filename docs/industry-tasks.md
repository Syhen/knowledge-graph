[Toc]

<h1>医疗行业知识图谱子任务算法总结</h1>
[一文详解达观数据知识图谱技术与应用](https://www.jiqizhixin.com/articles/2018-09-28-11)

[LinkedData]()  这个数据如何获取？

**无论用哪种方法，都不能保证百分之百的准确率，所以最后也要有人工审核和过滤。**

所有的有监督模型都需要设计完整的迭代闭环。
- 新的标注数据如何来？
- 模型迭代周期多少？
- 测试环境和线上环境如何尽量匹配？如何测试模型在生产环境的效果？

# 实体识别

## 实体融合
现在实体对齐普遍采用的还是一种聚类的方法，关键在于定义合适的相似度的阈值，一般从三个维度来依次来考察的，首先会从字符的相似度的维度，基于的假设是具有相同描述的实体更有可能代表同实体。第二个维度，是从属性的相似度的维度来看的，就是具有相同属性的和以及属性词的这些实体，有可能会代表是相同的对象。第三个维度，是从结构相似度的维度来看，基于的假设是具有相同邻居的实体更有可能指向同对象。

## 结构化数据
### 图映射
链接数据中获取知识

### D2R转换
结构化数据库中获取知识
D2R: Database to RDF


## 半结构化数据
### 表格
### 列表

## 非结构化数据
### 正则表达式
- 需要人工编写大量规则
- 准确率高
- 召回率低

### 深度学习
- 模型：Word Embedding + Bi-LSTM + CRF
- 需要人工标注数据
- 需要大量已 `标注数据`
- 标注的结果直接决定模型的效果

# 实体关系提取
## 基于规则
### 基于模板

### 基于依存句法
比如：主谓宾构成一个关系

## 机器学习
### 有监督
需要定义关系并给 `大量数据` 打上标签
- 深度学习
  Word Embedding & Position Embedding/POS-tag Embedding & 实体标签 Embedding + CNN/RNN + Attention
- 机器学习

### 半监督
难度量模型
- Seed-base Bootstrapping
- Snowball
- 远程监督
有什么样好的处理的方法？用远程监督的一种方法，典型的工具Deepdive，也是斯坦福大学InfoLab实验室开源的知识抽取的系统，通过弱监督学习的方法，从非结构化的文本当中可以抽取出结构化的关系的数据。开发者不需要理解它里面的具体的算法，只要在概念层次进行思考基本的特征就可以了，然后也可以使用已有的领域知识进行推理，也能够对用户的反馈进行处理，可以进行实时反馈的一种机制，这样能够提高整个预测的质量。背后用的是也是一种远程监督的技术，只要少量的运训练的数据就可以了。

### 分布式知识表示
还有是基于分布式的知识语义表示的方法，比如像Trans系列的模型，在这个模型基础上进行语义的推理。TransE这个模型的思想也比较直观，它是将每个词表示成向量，然后向量之间保持一种类比的关系。比如上面这个图里面的北京中国，然后类比巴黎法国，就是北京加上首都的关系就等于中国，然后巴黎加上capital的关系等于France。所以它是无限的接近于伪实体的embed]ding。这个模型的特点是比较简单的，但是它只能处理实体之间一对一的关系，它不能处理多对一与多对多的关系。

### 无监督
难度量模型
关系无法定义，使用的是原文中的词句、精度低
- Open IE

# 事件提取

# 知识融合
## 数据分组

## 属性相似度计算
### 字符串
- 编辑距离
- 余弦相似度

### 集合类型
- Jaccard相似度
现有两集合 $P$ 和 $Q$，Jaccard相似度 $S_{jaccard}$ 为：
    $$S_{jaccard} = \frac{n(P \cap Q)}{n(P \cup Q)}$$

### 文档类型
- 基于关键词的余弦相似度计算
- 基于 `Tf-idf` 或 `TextRank` 计算关键词
- 基于 `Word2Vec` 等文本向量表示计算相似度

## 实体相似度计算
### 回归

### 聚类

# 知识推理
