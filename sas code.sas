/* 数据预处理 */
proc stdize data=raw_data method=std missing=em out=std_data;
var q1-q17;
run;

/* 多组验证性因子分析 */
proc calis data=std_data group=景点 multigroup;
measurement
  嵌瓷存在感 = q4 q5 q6,      /* 因子载荷 */
  游客感受 = q7 q8 q9,
  人文发展 = q14 q15,
  经济促进 = q12 q13,
  文化认同 = new_q18 new_q19 new_q20; /* 新增题项 */

structural
  游客感受 = b1*嵌瓷存在感 + b2*人文发展 + b3*文化认同,
  文化认同 = g1*嵌瓷存在感 + g2*游客感受,
  经济促进 = d1*游客感受 + d2*文化认同 + d3*人文发展;

fitindex on;  /* 输出扩展拟合指标 */
modification type=standard;  /* 显示模型修正建议 */
run;

/* 跨组等价性检验 */
proc calis data=std_data group=景点 groupnames=('嵌瓷博物馆' '城隍庙' '从熙公祠' '青龙庙');
model test1:  /* 形态等价 */
  measurement 嵌瓷存在感 = q4 q5 q6;
model test2:  /* 度量等价 */
  measurement 嵌瓷存在感 = (q4-q6) (1-3);
model test3:  /* 结构等价 */
  structural 游客感受 <- 嵌瓷存在感人文发展;
run;
