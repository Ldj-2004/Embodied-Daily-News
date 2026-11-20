# 具身智能日报｜2026-11-20

## 1. [Awaken-HI: Scaling Humanoid Intelligence with Whole-Body Human Experience](https://arxiv.org/abs/2611.26420v1)

Awaken-HI 面向家庭与工作场所的人形机器人学习，构建核心数据资产 Awaken-Human，将约5万小时第一人称双目视频与同步的人体全身运动数据配对，为模型提供超越单项操作的人类经验。该工作针对第一人称视频活动覆盖广、却缺乏全身动作监督的缺口，尝试以规模化数据支持日常工作和全身移动操作学习，让视觉经历与可执行的身体运动建立对应，而非只覆盖孤立的操作技能。

**为什么重要：** 大规模配对人体运动与第一人称视频，有望补足人形机器人全身移动操作的数据监督，推动人类经验向可执行技能转化。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 01:03

## 2. [PGX: Physically Grounded Execution for Long-Horizon Humanoid Loco-Manipulation](https://arxiv.org/abs/2611.26596v1)

PGX 研究人形机器人的长时程移动操作，指出单体 VLA 虽能执行多种独立技能，却难以同时兼顾时间结构、技能组织与精度控制的紧耦合，长任务中的执行可靠性因此受限。其 Physically Grounded Execution 将时间与精度控制交由两个经典、免训练组件处理，让学习模型无需独自承担全部执行细节，目标是在长时程任务中保持技能组织、技能衔接与物理执行的可靠性。

**为什么重要：** 把长任务中的时间与精度控制从端到端学习中拆解出来，为提升人形机器人移动操作的稳定性和失败诊断能力提供思路。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 02:52

## 3. [波士顿动力第二代Stretch卸货机器人以部署数据升级可靠性，换件维护大幅提速](https://roboticsandautomationnews.com/2026/11/19/boston-dynamics-launches-next-generation-stretch-robot-with-major-reliability-upgrades/107354)

波士顿动力发布第二代 Stretch 自主移动拖车卸货机器人，依据超过10万运行小时和数千万个箱子的部署数据，针对非计划停机改造硬件与结构。新机减少81%、约半英里内部线缆，采用车规级连接器、升级夹爪和可连续旋转关节，模块化设计支持即插即用换件，完整转向驱动更换由一天缩至约一小时；其最高卸货速度为每小时1000箱，电池可覆盖两个班次。

**为什么重要：** 以真实车队故障数据指导线缆、关节和维护设计，表明物流机器人竞争正从峰值演示转向全生命周期正常运行时间与运维成本。

> 来源：Robotics & Automation News｜发布时间：2026-11-20 01:41

## 4. [One Prior, Two Dynamics: Repurposing Video Diffusion Transformers for Self-Supervised Latent Action Learning](https://arxiv.org/abs/2611.26617v1)

O²LaF 面向无动作标注视频中的自监督潜在动作学习，针对视频能够呈现世界变化、却不直接给出导致变化的动作这一问题，探索从观察中恢复可用于控制的潜在动作表示。该方法复用预训练视频扩散 Transformer，让同一生成先验同时服务逆向动力学与前向动力学，避免主要从零学习底层动态，并为自监督潜在动作学习和后续机器人控制提供统一的表示路径。

**为什么重要：** 复用视频生成先验可降低从无标注视频学习动作表征的成本，并为机器人控制衔接大规模视觉经验提供统一路径。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 02:58

## 5. [英伟达与微软扩展全栈合作，Azure运行Vera Rubin并强化开放模型定制](https://blogs.nvidia.com/blog/microsoft-ignite-accelerated-computing-azure-windows-pcs)

NVIDIA 与微软扩展全栈合作，Vera Rubin NVL72 系统已在 Azure 数据中心运行，面向高要求推理、智能体应用及大规模模型训练与推理，双方还推进机架级机密计算和能效优化。Microsoft Foundry 将增加 NVIDIA 开放模型及定制、部署能力；EY 以 Nemotron 适配采购记录分类后，评估准确率提高55%，成本较专有前沿模型降低15倍。

**为什么重要：** 云端训练推理、开放模型定制与边缘运行能力的贯通，为具身智能模型开发、企业数据适配和机器人端侧部署提供基础设施支撑。

> 来源：NVIDIA Blog｜发布时间：2026-11-20 04:00

## 6. [PhyDEX: A Benchmark for Physical Reasoning in Vision-Language-Action Models via Dynamic Extrinsic Dexterity](https://arxiv.org/abs/2611.26565v1)

PhyDEX 是评估 VLA 物理推理能力的操作基准，以动态外在灵巧性考察物体如何借助环境完成交互，而非仅关注夹爪与物体的直接接触。测试把重力、摩擦、惯性和质量分布等因素纳入操作过程，用于区分策略是在插值训练经验，还是确实掌握会影响结果的物理关系，从而为比较不同 VLA 的物理理解提供更细致的诊断维度，并补充既有操作评价的观察角度。

**为什么重要：** 该基准把评价从接触成功扩展到环境物理关系，有助于识别VLA的泛化假象，推动操作策略形成可迁移的物理理解。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 02:33

## 7. [Risk-Controlled Test-Time Adaptation for Vision-Language-Action Models](https://arxiv.org/abs/2611.26438v1)

该工作研究检索增强 VLA 的测试时适配：系统把专家示范作为额外上下文，无需更新模型参数即可利用既有经验，但检索到相关示范并不代表策略一定能有效使用，执行仍可能失败。论文提出风险控制的测试时适配方法，将“检索内容相关”与“适配执行可靠”明确区分，目标是在保留免参数更新优势的同时约束适配失败风险，避免把检索命中直接等同于控制性能提升。

**为什么重要：** 将检索相关性转化为受约束的执行可靠性，可减少免训练适配的盲目性，为VLA在现场利用示范经验提供更安全的评估框架。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 01:12

## 8. [TacInno: Teaching Vision-Language-Action Models the Contact Dynamics Beyond Vision and Action](https://arxiv.org/abs/2611.26405v1)

TacInno 聚焦触觉增强 VLA 在富接触操作中的收益不稳定问题。论文指出，部分视触觉策略很少利用触觉，因为夹爪闭合时的凝胶形变等信号可由视觉观察预测，简单增加触觉输入并不必然带来新信息；为此，该方法尝试让模型学习视觉与动作之外的接触动态，使触觉更直接服务于细微接触事件感知和操作决策，而非成为重复的视觉补充。

**为什么重要：** 明确触觉何时提供视觉之外的增量信息，可避免多模态堆叠造成的虚假收益，推动富接触操作更有效地利用接触动态。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 00:53

## 9. [ZeroVLN: Learning to Navigate without Supervised Fine-Tuning of the VLM Brain](https://arxiv.org/abs/2611.26414v1)

ZeroVLN 针对视觉语言导航中常见的“VLM 大脑加可学习动作头”范式，质疑在导航数据上监督微调 VLM 的必要性，因为这种做法可能显著改变基础权重并损害通用视觉能力。论文提出慢—快导航框架，目标是在不对 VLM 大脑进行监督微调的情况下实现有效导航，同时保留基础模型的通用能力，为导航专用适应与通用能力保留提供另一种分工，避免专用训练全面改写基础模型。

**为什么重要：** 冻结通用VLM大脑并重新划分导航适应职责，有助于缓解专用训练造成的能力遗忘，降低通用模型部署到机器人的代价。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 01:01

## 10. [Plan4D: Generative Plannable 4D Worlds](https://arxiv.org/abs/2611.26516v1)

Plan4D 面向可规划的生成式4D世界模型，回应许多未来预测模型重视频观感、却物理依据较弱且长期几何一致性有限的问题。它在生成未来 RGB 视频的同时预测稠密4D几何，把显式4D建模引入世界预测，使画面变化与空间结构能够在同一时间轴上表达。该方法试图让生成结果不仅可观看，还能为后续规划提供更一致的空间与时间结构，而非单纯提高生成画面的美观度。

**为什么重要：** 把视频预测与稠密几何共同纳入世界模型，可提升长期场景表达的一致性，为基于生成预测的机器人规划提供更可用依据。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 01:59

## 11. [Saturn Dynamics开发交互式物理世界模型Arc，提升仿真速度与轨迹精度](https://roboticsandautomationnews.com/2026/11/19/saturn-dynamics-develops-physics-based-world-model-to-improve-robot-training/107351)

伦敦初创公司 Saturn Dynamics 正开发物理世界模型 Arc，将数学对称性与物理原理纳入架构，让开发者先在交互式仿真中测试开启抽屉、处理滑移物体等动作及后果。公司称，Arc 轨迹准确率较 NVIDIA Cosmos 高73%；在 Jetson Thor 上生成1秒仿真数据仅需0.6秒，Cosmos Nano 与 Edge 分别需23秒和9秒，旨在减少训练计算并缩小仿真到现实的差距。

**为什么重要：** 更快且更具物理依据的交互仿真可扩大动作后果测试规模，为机器人训练降低算力门槛，并直面仿真到现实的可靠性缺口。

> 来源：Robotics & Automation News｜发布时间：2026-11-20 01:23

## 12. [Mind2Act World: A Diagnostic Benchmark for Embodied Mind, Physical Action, and Mind-Action Composition in Robotic Manipulation](https://arxiv.org/abs/2611.26444v1)

Mind2Act World 将机器人操作能力拆为三类互补要素：基于历史的认知推理、精确且及时的物理执行，以及通过环境反馈把推理与执行组合起来的能力。该诊断基准针对既有评测常把推理和执行混在同一评价中的问题，分别审视具身心智、物理动作与二者组合，便于定位复杂任务失败究竟来自认知、动作还是协同，而不是仅以整体结果概括系统能力。

**为什么重要：** 拆分认知、执行与反馈协同可让失败归因更精确，避免总分掩盖短板，为操作模型的针对性改进和公平比较提供依据。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 01:15

## 13. [AgentRoboCritic: Understanding the Capability of Frontier Agents on Direct Robot Control](https://arxiv.org/abs/2611.26613v1)

AgentRoboCritic 系统分析前沿多模态语言智能体直接控制机器人的能力，这类智能体可不依赖高层原语，直接输出低层数值动作。论文认为，只报告回合级成功率无法说明智能体如何成功、在何处失败，因此引入动作级分析，对控制过程进行更细粒度诊断，为比较直接机器人控制策略提供超越单一成功率的观察视角，并帮助区分任务结果与具体控制行为。

**为什么重要：** 动作级诊断能够揭示成功率背后的控制质量与失败位置，为评估通用智能体能否承担低层机器人控制提供更可靠依据。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 02:57

## 14. [Serve Robotics开放三项物理AI服务，向外部机器人车队输出连接与数据能力](https://roboticsandautomationnews.com/2026/11/19/serve-robotics-opens-its-physical-ai-technology-to-other-robot-companies/107358)

Serve Robotics 推出 Physical AI Services，开放三项能力：Serve Link 连接机器人与端外智能，Data Curator 筛选车队高价值训练事件，真实世界数据目录提供人行道地形与基础设施数据。Serve 已在40多座城市和27家医院部署逾2000台机器人，服务覆盖十余个行业的数千台车辆；首批客户 Bedrock Robotics 通过 Wi-Fi、LTE、5G 和卫星网络连接工程机械。

**为什么重要：** 把车队连接、数据筛选与真实环境数据产品化，有助于中小机器人团队复用规模化运营基础设施，加快车队学习闭环。

> 来源：Robotics & Automation News｜发布时间：2026-11-20 01:50

## 15. [Realbotix推出Series 1教育陪伴人形机器人，2027年下半年开始交付](https://roboticsandautomationnews.com/2026/11/19/realbotix-launches-echo-humanoid-robots-for-education-wellness-and-companionship/107339)

Realbotix 将 Echo 平台更名并发布 Series 1 教育、健康与陪伴人形机器人，首批计划2027年下半年交付。桌面版与全身版分别售价11950和59950美元，具备17和39个自由度，支持100多种语言及多类AI平台，首批各限225台和25台；可选 Vinci 视觉系统在本地处理人脸识别、视线追踪等信息，预订押金199美元，软件订阅每月19.99美元起。

**为什么重要：** 低价桌面机型与本地视觉、会话能力结合，为教育陪伴场景提供具身交互载体，但实际交互价值与可靠性仍待交付后验证。

> 来源：Robotics & Automation News｜发布时间：2026-11-19 22:51

---

生成时间：2026-11-20T16:43:30+08:00

本日报由自动化系统辅助整理，重要信息请以原始来源为准。
