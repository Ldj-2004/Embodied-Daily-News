# 具身智能日报｜2026-11-22

## 1. [PGX: Physically Grounded Execution for Long-Horizon Humanoid Loco-Manipulation](https://arxiv.org/abs/2611.26596v1)

PGX聚焦人形机器人的长时程移动操作，指出视觉—语言—动作模型虽已能执行多种单项操作技能，但在移动与操作连续衔接的任务中仍容易受限。此类任务把时间结构、技能组织和执行精度紧密耦合，机器人不仅要完成局部动作，还要在长序列中维持物理上可执行的决策。研究以“物理接地执行”为切入点，将研究对象从孤立技能延伸到持续移动、操作和精度要求共同作用的场景。

**为什么重要：** 该研究把人形VLA的难点从单项技能成功率推进到长序列全身执行，有助于检验模型在真实物理约束下组织移动与操作的能力。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 02:52

## 2. [PhyDEX: A Benchmark for Physical Reasoning in Vision-Language-Action Models via Dynamic Extrinsic Dexterity](https://arxiv.org/abs/2611.26565v1)

PhyDEX面向语言条件下的机器人操作，关注视觉—语言—动作模型的物理推理能力。摘要指出，现有基准主要评估夹爪与物体的接触，却较少考察物体如何通过重力等因素与环境发生交互，因而难以覆盖动态外在灵巧性。该基准将评测重点扩展到物体—环境关系及其动态过程，用于区分模型只会形成抓取接触，还是能够理解并利用操作背后的物理作用，并把语言指令、视觉感知和物理后果放在同一评测语境中。

**为什么重要：** 它补充了以夹爪接触为中心的操作评测，有助于识别VLA是否真正理解物体与环境交互，推动物理推理和灵巧操作能力被分别检验。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 02:33

## 3. [Mind2Act World: A Diagnostic Benchmark for Embodied Mind, Physical Action, and Mind-Action Composition in Robotic Manipulation](https://arxiv.org/abs/2611.26444v1)

Mind2Act World是一项面向机器人操作的诊断基准，把具身智能所需能力拆分为基于历史的认知推理、精确且及时的物理执行，以及认知与动作的组合。研究认为，若机器人要像人一样适应并可靠完成复杂物理任务，这三类能力必须相互补充，不能只观察最终动作是否完成。该基准因此同时检查“心智”、行动及二者协同，为定位模型究竟在理解、执行还是组合环节受阻提供更细的评测视角。

**为什么重要：** 将认知、动作及其组合分开诊断，可避免最终成功率掩盖具体失效原因，为机器人模型选择训练数据、改进执行模块和评估协同能力提供依据。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 01:15

## 4. [Awaken-HI: Scaling Humanoid Intelligence with Whole-Body Human Experience](https://arxiv.org/abs/2611.26420v1)

Awaken-HI面向家庭和工作场所中的日常人形作业，尝试以全身人类经验扩展人形机器人智能。摘要指出，现有第一视角视频数据集虽然覆盖许多相关活动，却缺少可用于学习的同步全身运动数据，仅靠画面难以完整表达人的动作与身体协调。研究由此把规模化经验与全身运动信息放在同一问题中，关注如何将人类日常活动转化为人形机器人可利用的学习资源，而非继续只扩充视频数量。

**为什么重要：** 同步全身经验有望弥补第一视角视频对人体协调表达的不足，为人形机器人学习日常作业提供更贴合全身控制需求的数据方向。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 01:03

## 5. [Risk-Controlled Test-Time Adaptation for Vision-Language-Action Models](https://arxiv.org/abs/2611.26438v1)

该研究面向检索增强视觉—语言—动作模型的测试时适配：系统把专家示范检索为额外上下文，无需更新模型参数即可提高适配效率。摘要同时强调，即使检索到的示范与当前任务相关，也不能自然保证后续执行可靠，因此适配过程需要显式的风险约束。Risk-Controlled Test-Time Adaptation将问题从“能否利用示范”推进到“如何在测试时控制使用示范带来的风险”，兼顾参数不更新的便利性与机器人执行可靠性。

**为什么重要：** 免训练检索适配虽能降低部署成本，却可能引入不可控行为；风险控制思路关系到VLA能否在开放环境中安全使用外部经验。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 01:12

## 6. [TacInno: Teaching Vision-Language-Action Models the Contact Dynamics Beyond Vision and Action](https://arxiv.org/abs/2611.26405v1)

TacInno研究触觉如何真正帮助视觉—语言—动作模型完成接触密集型操作。触觉本可感知视觉上细微的接触事件，但摘要指出，加入触觉输入并不总能带来一致收益，部分视觉—触觉VLA的表现仍不稳定，说明多一种传感信号并不等于掌握接触过程。研究因此把目标表述为让模型学习视觉与动作之外的接触动力学，关注模型是否理解接触如何形成和变化，而不只是是否接入触觉数据。

**为什么重要：** 该工作提醒业界，触觉价值取决于模型能否学习接触动力学，而非简单叠加传感器，这对精细装配等接触密集任务的多模态训练具有参考意义。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 00:53

## 7. [ZeroVLN: Learning to Navigate without Supervised Fine-Tuning of the VLM Brain](https://arxiv.org/abs/2611.26414v1)

ZeroVLN关注视觉语言导航中VLM“大脑”的适配成本。代表性方法通常将视觉语言模型与可学习动作头结合，再在导航领域数据上微调VLM，使其预测几何目标；ZeroVLN则探索不对这一“大脑”进行监督微调的导航学习方式。该设定把研究重点放在如何保留并利用既有视觉语言能力，同时让导航系统获得行动所需的信息，为观察领域微调是否必需、动作学习与通用表征能否更好解耦提供了路径。

**为什么重要：** 若导航学习可少依赖VLM监督微调，就有机会降低领域适配成本并保留通用表征，为视觉语言导航模块的复用和工程部署提供新选择。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 01:01

## 8. [One Prior, Two Dynamics: Repurposing Video Diffusion Transformers for Self-Supervised Latent Action Learning](https://arxiv.org/abs/2611.26617v1)

该研究从视频可观察世界变化、却很少显式给出致变动作这一矛盾出发，讨论自监督潜在动作学习。既有方法可从视觉转移中恢复动作监督，但往往需要较大程度地从头学习底层动态；论文提出复用视频扩散Transformer，把其已有视频生成知识作为先验，而不是完全依赖新的动作数据。题名中的“一个先验、两种动态”概括了这一思路，核心是让视觉变化建模与潜在动作发现共享可迁移的动态基础。

**为什么重要：** 复用视频扩散先验可能减少潜在动作学习从零建模动态的负担，为从无动作标签视频中提取机器人学习信号提供更值得验证的路径。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 02:58

## 9. [AgentRoboCritic: Understanding the Capability of Frontier Agents on Direct Robot Control](https://arxiv.org/abs/2611.26613v1)

AgentRoboCritic考察前沿多模态语言智能体直接控制机器人的能力，包括不依赖高层技能原语、直接输出低层数值动作的方式。摘要指出，现有基准多只报告回合级结果，难以解释智能体究竟在哪些控制环节表现良好或失效，单次成功也不足以呈现执行过程。该工作因此将评价从最终成绩推进到能力诊断，关注前沿智能体面对连续机器人控制时的实际边界，为比较低层动作决策提供更细的分析框架。

**为什么重要：** 细粒度诊断比单回合成功率更能暴露直接控制的短板，可帮助判断通用智能体距离低层机器人控制还有多远，并指导后续评测与改进。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 02:57

## 10. [Alignment Drives Reuse: Learning Generalizable Robot-Use Agents from Heterogeneous Experience](https://arxiv.org/abs/2611.26376v1)

该研究试图从异构经验中学习可泛化的机器人使用智能体。视觉语言模型已能跨任务和领域泛化，但机器人操作仍受到本体差异、任务表述差异和几何约定不一致等因素制约，使多源经验难以直接复用。论文以“对齐推动复用”为核心观点，把不同机器人与任务经验之间的对齐视为学习通用能力的关键，研究重点不是简单汇集更多数据，而是让异构示范形成可迁移、可重复利用的操作知识。

**为什么重要：** 跨本体和任务的数据复用是机器人基础模型规模化的关键障碍，对齐视角有助于减少重复采集，并提升异构经验对通用操作能力的贡献。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-20 00:37

## 11. [Optimus拟18个月内胜任家务，黑芝麻智能在深圳成立具身智能总部](https://news.google.com/rss/articles/CBMiUEFVX3lxTFB6RWZ6bVhoUUhFMmJ3VloyMm12akFMdUtwTXR1NUJBQnlCUzcxWWszdDVMeEpla3hWelZxUEZ1ZjJQd2lTWGc1bjF6dUhzUHVL?oc=5)

盖世汽车“小智一周要闻”汇总两条具身智能产业动态：特斯拉Optimus拟在18个月内具备胜任家务的能力，黑芝麻智能则在深圳成立具身智能总部。前者把人形机器人的应用目标进一步指向家庭劳动，后者体现相关企业围绕具身智能进行区域组织布局。现有材料未披露Optimus的具体家务清单、验证标准，也未给出深圳总部的投资规模、团队配置或研发安排，后续进展仍需结合企业披露判断。

**为什么重要：** 家务目标将检验人形机器人在非结构化环境中的长期可靠性，区域总部则关系到研发与产业协同，但时间表不等于能力已经兑现。

> 来源：盖世汽车｜发布时间：2026-11-22 17:09

## 12. [制造业数据缺口正制约物理AI落地](https://www.therobotreport.com/the-manufacturing-data-gap-holding-back-physical-ai)

文章指出，2026年以来机器人与物理AI公司已融资近480亿美元，但自主机器进入工厂仍受真实数据不足制约。以焊接为例，角度、移动速度和工件位置等参数如何影响成品，往往只存在于技师经验中，且设备记录与质检结果分散在不同系统。受访制造商中，将数据互操作性不足视为智能工厂主要障碍的比例由2025年的22%升至2026年的37%；文章建议优先采集真实生产数据，并把工艺决策与可测量的质量结果关联起来。

**为什么重要：** 物理AI要从演示走向稳定生产，关键不只是模型规模，而是可学习的工艺—质量闭环；数据治理将直接影响机器人自适应与良率改善。

> 来源：The Robot Report｜发布时间：2026-11-22 06:25

## 13. [宇树获得全球首条人形机器人拳击金腰带](https://news.google.com/rss/articles/CBMiWEFVX3lxTE50aVBsTUlxZ1JqV1hpcndka2FHQ2YxVFhOS2F3WnZaLTZYQ2tyTkd4QmxyU2ZTTVRmVkRQYzlDaldaTXFGVVIyaVkzajJjSnkxcjhrRTREZS0?oc=5)

驱动之家报道，宇树获得被称为“全球首条”的人形机器人拳击金腰带，事件将人形机器人拳击从技术展示推向带有竞赛头衔的传播场景。现有材料只确认这一结果，未披露参赛机器人型号、对手、赛制、判罚标准或具体技术表现，因此不能直接把夺冠等同于运动控制、动态平衡和抗冲击能力已经通过系统验证。该进展更适合作为高动态机器人展示及公众关注的案例，仍需技术细节支撑能力判断。

**为什么重要：** 拳击场景可集中呈现人形机器人的快速动作、平衡与接触应对，但金腰带主要是赛事结果，产业评估仍需可复现的控制指标与测试条件。

> 来源：驱动之家｜发布时间：2026-11-22 12:02

## 14. [Anthropic是否正在变成OpenAI？](https://news.google.com/rss/articles/CBMikgFBVV95cUxPdVJWMDdSVXlIT05KX3ZILTRURV84REVnaG9wTFVjaGtvcEJhZ0E0SWx2YUV5ckF3M1BVaTI2Qm5xYXo0RG04Sm9URkZLc1Z1V2RudC1fbXhpck02dFp4dE5oOEFaZzNBOVFNUU14NXpyUTNxajFncjJrTUVyaGtLbUlENnJBUEdMd0s2YXFLclVaQQ?oc=5)

The Verge以“Anthropic是否正在变成OpenAI”为题，讨论前者的发展路径是否开始呈现与后者相似的特征，核心是公司定位与演进方式的比较，而非机器人技术发布。现有输入只有标题，没有正文可核对，也未提供产品、融资、组织治理、模型商业化或安全策略等具体论据，因此不能将设问改写为战略转型的既定事实。对具身智能日报而言，该条目前只能作为前沿AI公司发展方向的媒体观察线索。

**为什么重要：** 前沿模型公司的战略变化可能影响机器人基础模型供给、合作方式与安全边界，但正文缺失时应避免把媒体设问当成确定的产业信号。

> 来源：The Verge｜发布时间：2026-11-21 23:00

## 15. [物理AI进工厂，先补齐制造数据短板](https://news.google.com/rss/articles/CBMiiwFBVV95cUxNMlNaM3pha2IzZVE3b1VReTNIaE52YjdRblM5N212V2FJY3JRUTkxazdzTGlBOTRvX25YWW55OGdrZHJTZFBVaXRKRFE3bVdPenNVczhiaHplejFMcFh4eWZBYWhaeFFMRjZCajI1b3RYVkhYaVdDVW1RRERsM2FkNTRVNGI3bjI5TXhz?oc=5)

物理AI要在制造业实现可靠自主决策，短板不只在机器人本体，也在数据采集、系统互操作和质量反馈。生产现场常把设备参数与检测结果分别保存，技师依据经验作出的调整又缺少结构化记录，使模型难以建立工艺选择与成品质量之间的联系。文章以焊接等流程说明这一问题，并主张部署前明确机器人所需信息、采集反映真实工况的数据，同时与机器人合作方检查既有基础设施，优先补齐影响可靠调整的缺口。

**为什么重要：** 这一分析把机器人落地难点延伸到工厂数据基础，提醒企业同步建设工艺记录、系统连接和质量反馈，才能支撑自主系统持续作出可靠调整。

> 来源：The Robot Report｜发布时间：2026-11-22 06:30

---

生成时间：2026-11-22T21:38:06+08:00

本日报由自动化系统辅助整理，重要信息请以原始来源为准。
