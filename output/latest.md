# 具身智能日报｜2026-11-06

## 1. [智元发布GO-3 Preview，登顶三项具身智能基准](https://news.google.com/rss/articles/CBMi0AFBVV95cUxNUTJPaFpWWDQwMmVoVHRLQkNkRmxVN0hQV0s2T29jS2tpckJNX2hUajlYYk5VUDktMGZiNVR5QzA0dmk4VzkzaGVaOGJUQ1Z4WEI5MlZDcjJzV1B3RFRHdmdxdUFLOVFYMndla1NXRWpWM2RvalZFUjJYV1JPN1hUNFNKOC1sRVEyd19qWGd6LV9lLURwa3hLNkYwRGtFcUlSWEpoUHM5YjBoR1luazRTZkItNVNwaXhxRTZPaWdDZGRDMEhZNWVZWlJreWl3Wjh2?oc=5)

智元机器人发布GO-3 Preview，并在三项具身智能基准测试中取得第一，显示其正围绕通用具身模型推进模型能力与公开评测的系统化迭代。此次信息同时涉及模型更新和榜单表现，但尚未披露架构、训练数据、评测任务及实测硬件细节，也缺少真实机器人任务中的成功率与稳定性数据，因此榜单领先能否转化为跨场景泛化和可靠执行，仍需结合原始技术材料验证。

**为什么重要：** 三项基准登顶为通用具身模型提供公开比较参照，但榜单与真实硬件表现之间的差距，提醒产业重视可复现评测和实机验证。

> 来源：Robotics & Automation News｜发布时间：2026-11-05 18:23

## 2. [小米人形机器人在汽车工厂完成8小时班次](https://news.google.com/rss/articles/CBMirAFBVV95cUxORXZhM2h6VnU3REpqZ3VRMnRKRzJlYjR1VnhrWGZydkJpNU1CQTQtSEczRkxvYjhRRXREdWFKNzRjYzFtWUJHWFJnOEdvMVVJMGdLS24yaTMzZlVSQ1p2Y2JkYnFwdWFGbWxSbjdBXzlPbUdXWXFGd05mek85NDJPU0pHYmZ2bnZwMkprZkMtZWVKNDFieGtMWGZFTGFKNEwzRTV6a2xUZ3pGeGJy?oc=5)

小米人形机器人被报道已在电动汽车工厂承担汽车面板分拣任务，可连续工作长达8小时，并支持全天候运行。相比短时演示，覆盖完整班次更接近工业现场对持续作业、生产节拍与可靠性的要求，也体现其在自有制造场景中的真实试用；目前尚未披露任务成功率、人工接管频次、部署数量及是否进入规模化生产，落地成熟度仍待验证。

**为什么重要：** 完整班次试用将人形机器人验证从演示推向连续生产，为评估工业耐久性、节拍适配与规模化部署价值提供了更贴近现场的观察窗口。

> 来源：Moomoo｜发布时间：2026-11-05 16:00

## 3. [校准潜在探测实现VLA运行时失败预测与分类](https://arxiv.org/abs/2611.08425v1)

该论文面向视觉—语言—动作（VLA）模型在分布偏移下的突发失效，研究基于校准潜在空间探测的运行时失败预测与分类。目标是在边缘设备可承担的开销内，提供及时、校准且能说明失败类型的监控信号，从而降低设备损坏和人员安全风险；相比仅在失败后纠错，该方向把可靠性保障前移到执行过程，可为系统触发暂停、人工接管或恢复策略提供依据。

**为什么重要：** 轻量、校准且可分类的运行时监控有望补足VLA安全闭环，让机器人在失效造成后果前及时干预，并为边缘部署和失败恢复研究提供新路径。

> 来源：arXiv Robotics｜发布时间：2026-11-06 02:21

## 4. [SLA以持续预训练扩展空间语言动作模型](https://arxiv.org/abs/2611.08373v1)

SLA提出通过持续预训练扩展空间—语言—动作模型，针对现有VLA多从二维视觉语言预训练继承表征、空间监督往往仅在任务适配阶段加入的问题，将三维空间理解前移为基础模型能力。研究目标是同时服务语义理解与精确控制，使空间知识能够跨任务迁移，并探索可复用的空间预训练路径，避免为每项操作任务分别补充空间监督。

**为什么重要：** 把三维空间能力前移至预训练阶段，有助于减少对单任务空间监督的依赖，为跨任务操作、精确控制及通用机器人表征学习提供可复用基础。

> 来源：arXiv Robotics｜发布时间：2026-11-06 01:52

## 5. [英伟达发布Cosmos 3交互式世界模拟开放模型](https://huggingface.co/blog/nvidia/cosmos-interactive-world-simulation)

英伟达为Cosmos世界模型开发平台新增四个Cosmos 3 Nano开放权重后训练检查点，均有160亿可训练参数，并采用OpenMDW1.1许可。Sim-Bimanual可根据机器人或相机动作预测视频，Sim-Transfer把仿真器控制与文本提示转为逼真视频；面向驾驶的Transfer-Auto支持最多11路相机及RGB—LiDAR联合生成，Sim-Auto则流式输出同步相机和激光雷达观测，用于交互仿真与多传感器驾驶场景。

**为什么重要：** 开放权重与后训练配方为动作条件世界模型和多传感器仿真提供共同起点，有助于机器人数据生成与策略测试，但仍需验证其支持策略学习和评估的保真度。

> 来源：Hugging Face Blog｜发布时间：2026-11-06 03:35

---

生成时间：2026-11-06T16:13:23+08:00

本日报由自动化系统辅助整理，重要信息请以原始来源为准。
