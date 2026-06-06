# 百科全书检索指南

画任何动植物之前，先阅读相关百科条目。AI 没见过猫——但百科告诉你猫长什么样。

## 检索优先级

### 第一优先：百科/图鉴

```
"<对象> anatomy diagram labeled"       → 解剖结构图
"<对象> morphology description"         → 形态学描述
"<对象> 身体结构 比例"                   → 中文百科
"<对象> species description size"       → 物种特征（尺寸/颜色/比例）
```

### 第二优先：博物学插画

```
"<对象> natural history illustration"   → 博物学插画（精准比例）
"<对象> field guide drawing"            → 野外图鉴插画
"<对象> biological illustration"        → 生物学图示
```

### 第三优先：照片

```
"<对象> photo profile" → 等百科建立认知后，用照片验证
```

## 阅读百科时需要提取的关键信息

对于像素画设计，百科中最重要的不是文字描述，而是**量化比例数据**：

| 提取项 | 示例（猫） | 用于像素画 |
|--------|----------|-----------|
| 头身比 | 头约占体长 1/5 | 32px 网格中头占 6px |
| 耳位 | 耳在头顶两侧，间距约 1 耳宽 | 耳坐标 |
| 眼位 | 眼间距约 1 眼宽，位于面部中线 | 眼坐标 |
| 尾长 | 尾长约等于体长 | 尾巴像素数 |
| 四肢比例 | 前腿直，后腿弯曲，掌垫形状 | 腿的像素走向 |
| 颜色分布 | 白胸、深背、条纹走向 | 配色方案 |

## 常见误区（AI 容易犯的）

- **眼睛太大**：AI 常把眼睛画成占脸 1/2，实际约 1/5~1/4
- **耳朵位置**：AI 常把耳朵画在头顶正上方，实际在两侧偏上
- **身体太直**：坐姿猫背是弧形，不是直线
- **腿太粗/太短**：猫腿细长，AI 容易画成柱子

## 检索示例

画猫时：
```
1. "cat anatomy proportions head body ratio" → 了解头身比
2. "cat skeletal structure side view" → 了解骨骼曲线
3. "cat sitting posture reference" → 坐姿的脊椎弧度
→ 然后才搜索像素参考
```

画蚊子时：
```
1. "mosquito anatomy diagram body parts" → 口器/胸/腹/翅
2. "mosquito leg structure femur tibia" → 腿的关节位置
→ 然后才搜索像素参考
```
