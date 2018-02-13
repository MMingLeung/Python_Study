# MySQL 索引的学习总结

## 简介

&emsp;&emsp;本文是基于 [MySQL索引背后的数据结构及算法原理](http://blog.codinglabs.org/articles/theory-of-mysql-index.html) 的学习总结。

<br>

## 数据结构及算法基础

### 索引是什么？

&emsp;&emsp;索引是帮助 MySQL 高效获取数据的一种**<u>数据结构</u>。**

​	通过某种方式把数据指向某种数据结构中，实现高级查找算法，这就是索引。

<br>

### B-Tree、B+Tree

#### B-Tree

>1、d为大于1的一个正整数，称为B-Tree的度。
>
>2、h为一个正整数，称为B-Tree的高度。
>
>3、每个非叶子节点由n-1个key和n个指针组成，其中d<=n<=2d。
>
>4、每个叶子节点最少包含一个key和两个指针，最多包含2d-1个key和2d个指针，叶节点的指针均为null 。
>
>5、所有叶节点具有相同的深度，等于树高h。
>
>6、key和指针互相间隔，节点两端是指针。
>
>7、一个节点中的key从左到右非递减排列。
>
>8、所有节点组成树结构。
>
>9、每个指针要么为null，要么指向另外一个节点。
>
>10、如果某个指针在节点node最左边且不为null，则其指向节点的所有key小于v(key1)v(key1)，其中v(key1)v(key1)为node的第一个key的值。
>
>11、如果某个指针在节点node最右边且不为null，则其指向节点的所有key大于v(keym)v(keym)，其中v(keym)v(keym)为node的最后一个key的值。
>
>12、如果某个指针在节点node的左右相邻key分别是keyikeyi和keyi+1keyi+1且不为null，则其指向节点的所有key小于v(keyi+1)v(keyi+1)且大于v(keyi)v(keyi)。

<br>

![](http://blog.codinglabs.org/uploads/pictures/theory-of-mysql-index/2.png)

&emsp;&emsp;检索数据的方式：根节点二分法查找，找到对应节点则返回 data，否则对响应区间的指针指向的节点进行递归查找，指导找到节点或 null 指针。

算法复杂度 ：
$$
O(log_dN)
$$
<br>

#### B+Tree

>与 B-Tree 不同之处：
>
>1、每个节点的指针上限为 2d-1 而不是 2d 。
>
>2、子节点不存 data，只保存 key。叶子结点不保存指针。
>
>3、节点的大小所需空间不同。

![](http://blog.codinglabs.org/uploads/pictures/theory-of-mysql-index/3.png)

<br>

**带顺序访问指针的 B+Tree**

&emsp;&emsp;优化版本，提高区间访问能力。

![](http://blog.codinglabs.org/uploads/pictures/theory-of-mysql-index/4.png)

<br>

------

### 为什么要用 B-Tree(B+Tree)?

&emsp;&emsp;索引所占空间大，一般以文件形式保存在磁盘中。而索引查找过程中产生磁盘 I/O 消耗，相对于内存是非常大的，所以索引的优劣使用查询过程中磁盘 I/O 操作次数的渐进复杂度来评判。索引的组织结构目的在于，减少磁盘 I/O 消耗，提高效率。

&emsp;&emsp;结合主存存取原理与磁盘存取原理分析 B-Tree(B+Tree) 作为索引的效率。

<br>

#### 主存存取原理

&emsp;&emsp;&emsp;主存主要是随机读写的储存器(RAM)，以下是抽象的模型。

![](http://blog.codinglabs.org/uploads/pictures/theory-of-mysql-index/5.png)

>存取过程：
>
>1、读取数据：系统把地址信号放在地址总线传给主存，主存读到地址信号后定位到存储单元，提取数据，放到数据总线上供其他部件使用。
>
>2、写入数据：把单元地址放在地址总线，数据放在数据总线，主存读区两个总线的信号，找到单元并写入数据。

<br>

存取过程不存在机械操作，时间与次数呈线性关系。

<br>

#### 磁盘存取原理

磁盘结构：

![](http://blog.codinglabs.org/uploads/pictures/theory-of-mysql-index/6.png)

> 磁盘由大小相同且同轴的盘片组成，转动同步。一头有固定支架与磁头，磁头可延盘半径方向移动。

<br>

俯视图：

![](http://blog.codinglabs.org/uploads/pictures/theory-of-mysql-index/7.png)

>1、盘面划分成一系列同心圆，称为磁道。
>
>2、所有半径相同的磁盘，称为柱面。
>
>3、沿半径划分的段，称为扇区。是最小的存储单元。

<br>

读取过程：

>1、系统把数据的逻辑地址传给磁盘。
>
>2、磁盘的控制电路按照寻址逻辑把逻辑地址翻译成物理地址。
>
>3、找到磁道与扇区，移动磁头到磁道上。（这个过程叫寻道，所消耗的时间叫寻道时间）
>
>4、磁盘旋转至目标扇区。（这个所消耗的时间叫旋转时间）

<br>

**局部性原理与磁盘预读**

&emsp;&emsp;根据局部性原理—— 当一个数据被使用到，附近的数据也马上会使用到。程序所使用的数据比较集中，为了提高磁盘读取效率，采取<u>预读操作</u>。

&emsp;&emsp;预读操作只需要小量的旋转即可完成，效率很高，总的来说可以提高 I/O 效率。其预读长度为一页的整数倍。

>页：是计算机管理存取器的逻辑块，硬件及操作系统把主存和磁盘分割为大小相等的块，每个存储块成为一页（通常为 4k），主存和磁盘以页为单位交换数据。
>
>主存和磁盘交换数据过程：程序需要读取的数据不在主存中，触发缺页异常，系统向磁盘发出读盘信号，磁盘会根据数据起始位置读取一页或几页，放入内存中，然后异常返回，程序继续运行。

<br>

#### B-Tree(B+Tree)索引的性能分析

&emsp;&emsp;B-Tree 一次检索最多访问 n 个结点，数据库设计者根据磁盘预读特性，将一个节点大小设为一页，每个节点只需一次 I/O 操作载入。

&emsp;&emsp;那么一次检索最多需要 n-1 次 I/O 操作（根结点在内存中），复杂度为
$$
O(n)=O(log_dN)
$$
&emsp;&emsp;又因为 d 很大，通常大于 100，所以 n 很小，通常不超过3，也就是 I/O 极大地减少。

&emsp;&emsp;B+Tree 中，因为子节点无 data，所以使得 d 更加大，拥有更高的效率。
$$
d_{max}=floor(pagesize / (keysize + datasize + pointsize))
$$

------

## MySQL 索引的实现

&emsp;&emsp;索引属于存储引擎级别的概念，不同的存储引擎对索引的实现方式是不同的，主要讨论MyISAM 和 InnoDB 两个存储引擎索引的实现方式。

<br>

### MyISAM索引的实现

&emsp;&emsp;MyISAM 使用 B+Tree作为索引的结构，叶子结点 data 区域存放数据的地址，是一种非聚类索引。

> Col1：主索引
>
> Col2：辅助索引
>
> 检索算法：二分法从根部开始检索，直到找到叶子结点对应的 key 获取其 data ，根据地址读取响应的数据记录。

![](http://blog.codinglabs.org/uploads/pictures/theory-of-mysql-index/8.png)

<br>

![](http://blog.codinglabs.org/uploads/pictures/theory-of-mysql-index/9.png)

<br>

### InnoDB 索引实现

&emsp;&emsp;数据文件就是索引本身，叶子结点记录完成的数据，是一种聚集索引。

> 1、必须有主键
>
> 2、data 区域保存的是主键的值，而不是地址
>
> 索引检索过程：查询根据某个人名的记录，先从辅助索引中获取主键的值，通过主索引根据主键获取记录。
>
> 
>
> 根据上述过程可知：
>
> 1、不建议使用过长的字段作为主键，因为辅助索引依赖主索引，会导致占用空间变大。
>
> 2、不建议使用非自增单调字段（非纯数字），因为数据文件即索引文件，非单调的主键会因为 B+Tree 的分裂调整导致效率低下。建议使用自增字段。

![](http://blog.codinglabs.org/uploads/pictures/theory-of-mysql-index/10.png)

　<br>

![](http://blog.codinglabs.org/uploads/pictures/theory-of-mysql-index/11.png)

<br>