# 局部搜索批处理脚本使用说明

本文档说明如何使用批处理脚本自动运行所有城市的局部搜索算法。

## 📁 文件说明

### 1. `test_ls_single.py` - 单例测试脚本
用于快速测试局部搜索算法是否正常工作。

**运行方式：**
```bash
python test_ls_single.py
```

**功能：**
- 对Cincinnati数据集运行1分钟测试
- 验证算法能否正常工作
- 适合调试和快速验证

---

### 2. `run_ls_all.py` - 批处理运行脚本 ⭐
自动对所有数据集运行局部搜索算法。

**运行方式：**
```bash
python run_ls_all.py
```

**配置参数（在脚本顶部修改）：**
```python
CUTOFF_TIME = 600  # 时间限制（秒），默认600秒 = 10分钟
NUM_SEEDS = 10     # 每个数据集使用的随机种子数量，项目要求至少10个
START_SEED = 0     # 起始种子值（默认从0开始）
```

**功能：**
- 自动找到DATA文件夹中的所有.tsp文件
- 对每个数据集运行NUM_SEEDS次（使用不同的随机种子）
- 显示实时进度和预计剩余时间
- 统计成功/失败次数

**输出：**
- 生成的解文件保存在 `output/LS/` 文件夹
- 文件命名格式：`<城市名>_LS_<时间>_<种子>.sol`
- 例如：`Atlanta_LS_600_0.sol`, `Atlanta_LS_600_1.sol`, ...

**预计运行时间：**
- 13个数据集 × 10个种子 × 600秒 ≈ 21小时
- 实际可能更快，因为算法可能提前收敛

---

### 3. `analyze_ls_results.py` - 结果分析脚本
分析所有运行结果，计算统计数据。

**运行方式：**
```bash
python analyze_ls_results.py
```

**功能：**
- 读取所有`output/LS/`文件夹中的解文件
- 计算每个数据集的：
  - 最优解
  - 平均解
  - 最差解
  - 标准差
  - 变异系数
- 显示每个种子的详细结果
- 生成CSV统计文件

**输出：**
- 控制台显示详细统计表格
- 生成 `ls_statistics.csv` 文件（可用于报告）

---

## 🚀 使用流程

### 步骤1：测试算法
```bash
python test_ls_single.py
```
确保算法能正常运行。

### 步骤2：批量运行（需要较长时间）
```bash
python run_ls_all.py
```

**提示：**
- 这个过程会运行很长时间（可能10-20小时）
- 建议在晚上或周末运行
- 可以在运行时做其他事情
- 按 Ctrl+C 可以中途停止（已完成的结果会保留）

### 步骤3：分析结果
```bash
python analyze_ls_results.py
```
查看统计数据并生成CSV文件用于报告。

---

## ⚙️ 自定义配置

### 修改时间限制
编辑 `run_ls_all.py`，修改：
```python
CUTOFF_TIME = 300  # 改为5分钟（更快但可能质量较低）
```

### 修改种子数量
编辑 `run_ls_all.py`，修改：
```python
NUM_SEEDS = 5  # 改为5个种子（更快）
```

### 只运行特定城市
编辑 `run_ls_all.py`，在 `get_tsp_files()` 函数中添加过滤：
```python
def get_tsp_files():
    data_path = Path(DATA_DIR)
    tsp_files = sorted(data_path.glob("*.tsp"))
    # 只运行Atlanta和Boston
    tsp_files = [f for f in tsp_files if f.stem in ['Atlanta', 'Boston']]
    return tsp_files
```

---

## 📊 输出文件说明

### 解文件格式
每个 `.sol` 文件包含两行：
```
670811                          # 第一行：路径总长度
1,2,3,4,5,...,100              # 第二行：访问城市的顺序
```

### 文件命名
```
<城市名>_LS_<时间限制>_<随机种子>.sol
```

例如：
- `Atlanta_LS_600_0.sol` - Atlanta，600秒，种子0
- `Atlanta_LS_600_9.sol` - Atlanta，600秒，种子9
- `Boston_LS_600_0.sol` - Boston，600秒，种子0

---

## 🔧 故障排除

### 问题：找不到DATA文件夹
**解决方案：** 确保在项目根目录运行脚本
```bash
cd C:\Users\Li103\Downloads\CSE6140\CSE6140_Project
python run_ls_all.py
```

### 问题：脚本运行很慢
**解决方案：** 
1. 减少时间限制：`CUTOFF_TIME = 300`
2. 减少种子数量：`NUM_SEEDS = 5`
3. 先测试小数据集（Cincinnati, Philadelphia）

### 问题：中途停止了怎么办
**解决方案：** 
- 已完成的结果会保留在 `output/LS/` 文件夹
- 可以修改 `START_SEED` 从未完成的种子继续运行
- 或者删除部分完成的结果，重新运行

---

## 📝 用于报告的数据

运行 `analyze_ls_results.py` 后，使用生成的 `ls_statistics.csv` 文件：
- 包含每个数据集的平均解质量
- 可以直接导入Excel或用于生成报告表格
- 用于计算相对误差（RelError）

---

## ✅ 检查清单

运行完成后，检查：
- [ ] `output/LS/` 文件夹中有130个文件（13城市 × 10种子）
- [ ] `ls_statistics.csv` 文件已生成
- [ ] 每个数据集都有10个不同种子的结果
- [ ] 解文件格式正确（两行，第一行是数字）

---

## 🎯 快速开始

**如果你想快速测试整个流程（推荐用于首次运行）：**

1. 修改 `run_ls_all.py` 为快速模式：
```python
CUTOFF_TIME = 60   # 1分钟
NUM_SEEDS = 3      # 3个种子
```

2. 运行：
```bash
python run_ls_all.py
```

3. 分析结果：
```bash
python analyze_ls_results.py
```

这样只需要约40分钟就能完成所有运行并看到结果！

---

**祝你运行顺利！** 🎉

