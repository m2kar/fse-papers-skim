# -*- coding: utf-8 -*-
"""为 papers.csv 重建“分类”与“顺序”字段并按顺序重排（可重复执行，原子写入）

六大类划分准则（互斥、边界清晰）：
  一、代码生成与自动化迁移   —— “写”：从零生成代码/模型/配置，以及遗留代码的自动迁移改造
  二、软件测试与质量保障     —— “测”：主动构造输入并执行被测系统以发现失效（测试与模糊测试技术）
  三、缺陷定位、调试与自动修复 —— “改”：失效后的诊断与治疗（定位、调试、修复）
  四、程序分析与智能运维     —— “析”：支撑上述任务的底层分析技术与运行期监控运维
  五、安全攻防与大模型可信   —— “防”：对抗性场景（漏洞、攻击、逃逸）及大模型自身可信与安全
  六、实证方法、开发者与教育 —— “研”：不解决具体工程问题，而研究方法本身、人与人才培养
"""
import csv, os

BASE = os.path.dirname(os.path.abspath(__file__))

PLAN = [
("一、代码生成与自动化迁移", [
    8,   # Hydra：仓库级生成·结构感知检索（RAG照搬NLP行不通）
    46,  # InlineCoder：同一问题另一解法·调用图内联（与上篇对照）
    45,  # I-BAYGEN：视角从仓库级细化到令牌级·关键令牌重加权
    11,  # EfficientUICoder：多模态UI生成+双向令牌压缩（效率）
    4,   # IaCGen：生成对象扩展到基础设施代码·评测看可部署性
    51,  # APIKG4Syn：低资源鸿蒙·知识图谱合成数据微调
    18,  # Event-B Agent：生成形式化模型·正确性由构造保证（收束“生成”）
    35,  # GraphQLify：转向旧代码现代化·REST→GraphQL确定性迁移
    37,  # GUIMigrator：XML→Compose/SwiftUI转译（与上篇同为迁移，路线对照）
]),
("二、软件测试与质量保障", [
    # A. LLM测试生成与复用
    32,  # TestGeneralizer：单测试泛化为场景全覆盖
    15,  # Cleverest：提交级即时回归测试（2分钟胜fuzzer 24小时）
    41,  # iCoRe：缺陷复现测试·检索质量决定生成质量
    47,  # IntentTester：测试知识跨库跨语言迁移（从生成到复用）
    29,  # TraceDroid：GUI崩溃驱动测试（从接口级上升到界面级）
    # B. 基础软件的模糊测试与变异测试
    49,  # CoupleFuzz：选项感知定向灰盒模糊测试（经典DGF强化）
    12,  # Eidolon：全同态加密库模糊测试·等价变换做预言
    48,  # HornGator：CHC求解器审讯式测试
    5,   # SugBreaker：rustc修复建议·约束违反引导变异
    21,  # P4负测试：类型检查器·悬空覆盖引导变异
    7,   # DiverFPS：浮点SMT多样解采样（为测试供料）
    # C. 智能系统测试
    2,   # DECODE：深度学习算子约束引导测试（引入智能系统）
    13,  # 测试选择度量实证（先立评估标尺）
    22,  # DRL智能体失效驱动测试
    27,  # PtoP：自动驾驶危险场景生成（自主性最高的被测对象）
]),
("三、缺陷定位、调试与自动修复", [
    3,   # 统计故障定位去噪（经典方法打底）
    36,  # GREClue：失效索引·多缺陷并行调试
    34,  # GraphLocator：LLM仓库级issue定位（经典→LLM）
    14,  # ADI：智能体函数级调试接口
    1,   # DeepK：显式调试知识库驱动的修复
    20,  # ExpeRepair：双记忆驱动的仓库级修复（与上篇对照：知识vs记忆）
]),
("四、程序分析与智能运维", [
    33,  # GPA：GPU加速流敏感指针分析（分析基础设施提速）
    50,  # JS自适应堆抽象（与上篇配对·指针分析提速）
    31,  # GAER：图自编码器架构恢复（微观分析→宏观理解）
    42,  # 静态切片+LLM检测ML Notebook数据泄漏（分析技术新应用）
    17,  # EventADL：云服务事件异常检测与根因定位（开发期→运行期运维）
]),
("五、安全攻防与大模型可信", [
    # A. 传统侧：攻击面自底向上
    19,  # Exorcist：硬件层·Spectre运行时检测
    24,  # MATUS：内核层·Linux内核缺陷检测
    30,  # GadgetHunter：运行时层·Java反序列化gadget链
    6,   # SmartComment：应用层·智能合约代码-注释一致性
    26,  # asmFooler：检测器自身·BCSD对抗鲁棒性
    25,  # Flash：攻防·静态恶意代码检测逃逸
    # B. 大模型侧：可信与安全
    38,  # 代码摘要幻觉：揭示/检测/缓解（质量可信）
    9,   # DualCodeDetect：AI生成代码检测（真伪）
    10,  # DuCodeMark：代码数据集水印（确权）
    23,  # 角色扮演公平性（偏见）
    44,  # InDe-LLM：越狱防御（模型安全）
]),
("六、实证方法、开发者研究与软件工程教育", [
    16,  # 配置采样后验风险与置信度（评估方法论）
    43,  # 模糊器评测结果的随机性（评测信度·与上篇呼应）
    40,  # 轻数据挑战（数据需求）
    39,  # 开发者-AI交互行为建模（回到人）
    28,  # AI时代软件工程教育（收尾：育人）
]),
]

order_map, cat_map, seq = {}, {}, 0
for cat, papers in PLAN:
    for n in papers:
        seq += 1
        order_map[n] = seq
        cat_map[n] = cat

src = os.path.join(BASE, "papers.csv")
with open(src, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.reader(f))
header = rows[0]

# 幂等：剥除旧“顺序/分类”列，保留其余原序
drop = [i for i, h in enumerate(header) if h in ("顺序", "分类")]
keep = [i for i in range(len(header)) if i not in drop]
header = [header[i] for i in keep]
rows = [[r[i] for i in keep] for r in rows]

idx_num = header.index("编号")
recs = {}
for r in rows[1:]:
    if r and r[idx_num].strip():
        recs[int(r[idx_num])] = r

assert set(recs) == set(order_map), f"编号不匹配: 缺失{set(order_map)-set(recs)} 多余{set(recs)-set(order_map)}"

new_header = ["顺序", "分类"] + header
out = [new_header]
for n in sorted(order_map, key=lambda x: order_map[x]):
    out.append([str(order_map[n]), cat_map[n]] + recs[n])

tmp = src + ".tmp"
with open(tmp, "w", newline="", encoding="utf-8-sig") as f:
    csv.writer(f).writerows(out)
os.replace(tmp, src)

print(f"完成：{seq} 篇，{len(PLAN)} 类")
for cat, papers in PLAN:
    print(f"  {cat}（{len(papers)}篇）: " + "→".join(map(str, papers)))
