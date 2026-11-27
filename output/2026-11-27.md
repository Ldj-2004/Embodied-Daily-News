# 具身智能日报｜2026-11-27

## 1. [Nav4Manip: From Navigation to Dexterous Mobile Manipulation through Co-Evolution](https://arxiv.org/abs/2611.34655v1)

Nav4Manip 面向复杂、非结构化环境中的灵巧移动操作，研究如何把导航与后续精细操作衔接起来。论文指出现有系统的一项关键问题是导航精度过于粗糙，难以为下游操作提供合适起点，并将协同进化作为从导航走向灵巧移动操作的思路。摘要片段尚未给出第二项挑战的完整表述，也没有实验平台、任务数量和性能数据，因此暂不能判断其相对基线的提升幅度。

**为什么重要：** 该研究把导航终点与灵巧操作需求联系起来，有助于改善移动机器人到达目标区域后仍难以稳定衔接精细操作的问题，并为两类能力的共同优化提供研究方向。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-26 00:29

## 2. [Toward Agentic Robotics: A Large-Scale Study of Harness Design for Robot-Use Agents](https://arxiv.org/abs/2611.34778v1)

这项大规模研究聚焦机器人使用智能体的 harness 设计，即视觉语言模型如何通过策略代码与工具理解多样场景并控制机器人。论文指出，近期模型虽已具备此类代理能力，但即使延长推理过程，对三维夹爪位姿的预测仍然较差，暴露出场景理解与精确操作之间的断层。研究以系统性比较 harness 设计为切入点，不过摘要片段未列出模型规模、基准任务、工具配置和量化结果。

**为什么重要：** 系统比较智能体脚手架有望厘清模型推理、工具接口与三维控制误差的关系，为机器人代理从会生成代码走向可精确执行提供评测依据。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-26 01:39

## 3. [Cairn: Object-Centric 3D Trajectory Priors for Steering Frozen VLAs](https://arxiv.org/abs/2611.34914v1)

Cairn 针对视觉—语言—动作模型在物体位置变化或路径受阻时的目标迁移与碰撞问题，引入以物体为中心的三维轨迹先验来引导冻结的 VLA。论文将此类模型视为有效的低层控制器，但指出其常把物体去向绑定到训练时的场景布局，导致物体被移动到错误位置或发生碰撞。该方法强调无需改动冻结控制器的引导思路，摘要片段未提供具体轨迹生成方式、实验任务和成功率。

**为什么重要：** 若能在不重训底层策略的情况下修正物体去向与避障行为，将降低 VLA 适配新布局的成本，并提升开放场景操作的安全性与可迁移性。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-26 02:57

## 4. [FineDex: Bridging Fine-Grained Human-Object Interaction Generation to Dexterous Humanoid Manipulation](https://arxiv.org/abs/2611.34884v1)

FineDex 试图把细粒度人—物交互生成与灵巧人形机器人操作连接起来，核心是让交互不仅描述做什么，还能指定如何做。论文认为灵巧性的基础是手指级控制，而现有灵巧操作与 HOI 生成方法很少允许用户明确控制交互方式，五指手也常被简化为夹爪式表达。其研究重点因此落在手指动作与交互语义的衔接，但摘要片段未披露模型结构、数据集、机器人平台和实验指标。

**为什么重要：** 把手指级交互意图接入人形机器人操作，可推动技能生成与精细执行之间形成更统一的表达，支持比夹爪式抓取更复杂的任务。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-26 02:40

## 5. [北京亦庄举办E-Bot Day 2026人形机器人开发者大会，集中发布具身智能成果](https://news.google.com/rss/articles/CBMiaEFVX3lxTFA1TWQyeW50dzJCOHluU0lSUzFTMXJobHZvNkFVZV8yRURHLUJzemticzZjbnM4VV9wTXRJRUh3ZFpudWdCTnBTQnBWS291M0hJWnVGZ2xGMFRFNXNYa0Z5U2MxWFA4TDNC?oc=5)

人民网报道，E-Bot Day 2026 人形机器人开发者大会在北京亦庄举办，并在会上发布多项具身智能成果。现有材料能够确认活动名称、举办地点及成果发布这一进展，但未列出具体成果、技术参数、参与机构、开发者规模或应用案例，因此尚无法评估各项成果的成熟度与产业影响。会议以人形机器人开发者和具身智能为核心议题，为相关技术集中展示与交流提供了活动载体，也为后续跟踪成果落地保留了明确线索。

**为什么重要：** 大会集中发布成果有助于观察人形机器人开发者生态与区域产业协同，但在缺少技术细节时，其实际研究价值仍需结合后续资料判断。

> 来源：人民网｜发布时间：2026-11-26 13:59

## 6. [Motion Beyond Pixels: Learning Future Visual Representations for Object-Centric Dynamics](https://arxiv.org/abs/2611.34644v1)

MotionRep 针对具身世界模型未来状态表示与运动生成脱节的问题，提出面向物体中心动态学习的视觉表示。论文指出，许多模型在为 RGB 重建优化的潜空间中预测未来，并未显式强调与运动生成相关的物体级语义和几何信息，因此希望让未来视觉表示超出像素重建目标。现有摘要片段仅交代问题与方法名称，尚未说明表示学习方式、预测任务、评测环境以及对规划或控制的具体增益。

**为什么重要：** 面向物体语义与几何优化未来表示，可减少像素重建目标对运动学习的干扰，为世界模型服务预测、规划和机器人控制提供更合适的状态描述。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-26 00:24

## 7. [RePace: Reasoning about Demonstration Speedup for Faster Vision-Language-Action Policies](https://arxiv.org/abs/2611.34864v1)

RePace 关注 VLA 策略继承人类示范动作缓慢的问题，提出在微调前对示范进行加速，并推理应当采用何种加速方式。与部署时另加速度选择模块不同，该思路把节奏调整前移到训练数据阶段，使微调后的策略有望直接执行得更快。论文因此同时涉及示范速度与策略执行效率，但摘要片段没有给出加速倍率、推理方法、任务类型、成功率变化或对不同机器人平台的验证结果。

**为什么重要：** 把执行节奏前移到示范数据处理阶段，可能以较低部署复杂度改善 VLA 的操作效率，也提醒研究者同时评估提速后的成功率与动作质量。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-26 02:30

## 8. [A Failure-Driven Data Flywheel for Post-Training Vision-Language-Action Models](https://arxiv.org/abs/2611.34698v1)

该研究提出失败驱动的数据飞轮，用于视觉—语言—动作模型的后训练，目标是在新机器人平台上逐项修正预训练模型未满足的行为要求。论文特别关注缺少大规模部署机器人队伍的团队：这类团队难以持续收集足够数据来覆盖部署后暴露的失败，因而需要围绕失败样本组织数据迭代。方法强调以后训练闭环承接真实问题，但摘要片段尚未说明失败如何发现、数据如何采集与筛选，以及每轮迭代的性能改善。

**为什么重要：** 围绕失败组织后训练数据，有助于资源有限的团队把有限采集预算用于真实薄弱行为，推动 VLA 从通用预训练走向特定平台的持续可靠部署。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-26 00:54

## 9. [RoboEvo$^2$: Recursive Robot Self-Improvement via Harness-Policy Co-Evolution](https://arxiv.org/abs/2611.34675v1)

RoboEvo$^2$ 研究通过 harness 与策略协同进化实现递归式机器人自我改进，面向陌生环境适应、交互习得新技能以及练习后高效执行三个阶段。论文肯定 VLA 策略的高效控制能力，同时指出其在获得新能力时往往仍需额外人类示范，限制了持续自主性。该工作试图把外部代理脚手架与底层策略共同纳入改进循环，不过摘要片段未给出循环机制、技能评估方式和真实机器人实验数据。

**为什么重要：** 协同改进代理脚手架与底层策略，为减少新增技能对人类示范的依赖提供了系统视角，也连接了交互学习、技能评估与高效控制三个环节。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-26 00:39

## 10. [Commit2Drive: Perception-Grounded Language Decisions as Commitments for Trajectory Planning in Vision-Language-Action Driving Models](https://arxiv.org/abs/2611.34614v1)

Commit2Drive 将基于感知的语言决策作为轨迹规划承诺，用于改进端到端自动驾驶 VLA 模型。现有方法同时输出语言决策和轨迹，使规划更易解释，但该工作进一步检视二者关系，强调让语言判断真正约束后续轨迹，而非仅作为附加说明。研究场景属于自动驾驶，摘要片段未提供承诺一致性的具体机制、评测数据集，以及安全性、规划精度或语言与轨迹一致程度的量化指标。

**为什么重要：** 让语言决策成为轨迹规划的可检查承诺，有助于提升端到端驾驶模型的决策一致性和可解释性，并为诊断感知、推理与控制偏差提供接口。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-26 00:01

## 11. [DemoFoundry: Toward Scalable Photorealistic Robot Data with Coding Agents and Generative Rendering](https://arxiv.org/abs/2611.34671v1)

DemoFoundry 面向可扩展、照片级真实的机器人数据生成，把编程智能体与生成式渲染结合起来，以同时获得逼真视觉观测和可靠动作监督。论文指出，仿真合成与真实环境存在明显视觉差距，而仅生成视频又难以完整满足机器人学习对动作标注的要求，因此尝试在两条数据路线之间取长补短。该工作聚焦示范数据的规模化生产，但摘要片段未披露智能体如何构建任务、渲染流程、数据规模以及在真实策略训练中的效果。

**为什么重要：** 若生成式渲染能兼顾视觉真实性与动作监督，将缓解真实机器人示范昂贵和仿真视觉失真的双重瓶颈，为规模化策略训练提供更可用的数据来源。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-26 00:37

## 12. [YYForce发布酒店礼宾人形机器人，采用NVIDIA Jetson与Isaac Sim](https://news.google.com/rss/articles/CBMinwJBVV95cUxPdEhuYlpDVjR2ZkRvQnQ2OE01NndQUWpwYUNqclk5ampyQjFsbFozTExYUXFKMm5Zd0NYam5pTEtsSmtBYnhmcVBMMy1fQWdMT201WG9pbnVzVkgzc285d29KZVZ6bUlpclRHbVJ4Rl95N1NBVGlTU1h0cWxvMV9fNVQtZHloN0ZVd0NLZzJsN0szLU12SENkTncxS3V0cFNDQ2ZVaW43NjcxQVZqMklsVFhZN3pIZ2pIQk5BeDB4Vk5pNlBqaFppMnJQYXd5dldWc1ZneG81eHlvYndlMFlkOHlvcS1QRW5fc0s0czB2TnlMb1FnQTVTcF9RcFg1V3Q4R2tPTFpfZjJINzdFX04wVk11S2h2S2ptQlNDR0psTQ?oc=5)

YYForce（NASDAQ: YFOR）发布一款面向酒店礼宾服务、已完成训练的人形机器人。现有摘要显示，该机器人的开发使用 NVIDIA Jetson 计算平台和 Isaac Sim 仿真工具，应用场景已明确指向酒店礼宾，但原始材料未披露机器人型号、硬件参数、试点酒店、训练数据、自主任务范围或商业化时间。此次更新因此主要确认了其目标服务行业与所采用的英伟达技术栈，机器人是否已进入真实酒店运营、能连续完成哪些礼宾流程，仍有待后续信息说明。

**为什么重要：** 酒店礼宾为人形机器人提供了流程相对明确的服务入口，Jetson 与 Isaac Sim 的组合也反映仿真训练和计算平台在商用机器人开发中的支撑作用。

> 来源：Toronto Star｜发布时间：2026-11-26 22:50

## 13. [物理AI模型在机器人操作速度测试中超过人类操作员](https://news.google.com/rss/articles/CBMixAFBVV95cUxOVmxIdUZkQkRyU21naU1IT2ttY3VPLVVpUjBZSzVLMjctbkxRdks5cG5nRkFfV0VfSFFXWFVST19qNFRRWXlZVTRmbzlHWlZmc1c1LUpveUszZ3ViVUxJaFRKcDVtcnQwa2lmZ3RiTnNsa0M1YUc2MXMyVlNiMU51OTloSWM2M3I0bkpaVjJKdW5yOVFham1PYzZRcXp3VWs5alRFODJSRDZIWWdPend4dXFjZE1ObjBVMFpnSTRJZ3R4c2Nw?oc=5)

Positronic Robotics 发布的 PhAIL 测试显示，mimic 的 FLUX-mimic-x 在 Franka FR3 机械臂日常操作中，成功任务中位耗时为11秒，人类遥操作为27秒。该模型可靠率为71.2%，每分钟完成3.08个成功任务；人类可靠率达到94.7%，但每分钟仅完成1.83个，说明其速度领先而可靠性仍有差距。测试包括开抽屉、移动家居物品和将物品放入容器，结果还显示可靠率最高的四个专用机器人模型均采用视频模型路线。

**为什么重要：** 测试把速度与可靠性分开呈现，既展示视频预训练模型提升操作节拍的潜力，也提醒产业部署不能仅以超越人类速度判断系统成熟度。

> 来源：Robotics & Automation News｜发布时间：2026-11-26 18:21

## 14. [mimic物理AI模型操作速度超过人类遥操作，可靠性仍落后](https://roboticsandautomationnews.com/2026/11/26/physical-ai-model-outpaces-human-operator-in-robot-manipulation-tests/107719)

PhAIL 榜单测试中，mimic 的70亿参数视频—动作模型 FLUX-mimic-x 使用 Franka FR3 机械臂完成日常任务，成功任务中位耗时11秒，低于人类遥操作的27秒。其可靠率为71.2%、速度为每分钟3.08个成功任务，人类则分别为94.7%和1.83个；Runway 的 Praxis-1 在物体滑落后有66%的相关片段最终恢复成功。FLUX-mimic-x 基于 FLUX 3 视频模型，可靠率最高的四个专用机器人模型也均采用视频方法。

**为什么重要：** 结果说明视频模型预训练可能同时改善操作速度与动作可靠性，但人类遥操作的可靠率优势表明，物理AI进入实际作业仍需重视失败恢复。

> 来源：Robotics & Automation News｜发布时间：2026-11-26 18:21

## 15. [沃尔沃汽车在根特工厂训练AEON人形机器人，目标2027年年中投入生产](https://roboticsandautomationnews.com/2026/11/26/volvo-cars-begins-training-hexagon-humanoid-robots-for-factory-work/107733)

沃尔沃汽车已在比利时根特工厂开始训练和测试 Hexagon Robotics 的 AEON 人形机器人，计划2027年上半年扩大试点，并力争自2027年年中投入实际生产。机器人通过模仿学习练习把零部件高精度放入两个夹具，后续将处理多部件、在生产区域导航并与既有自动化系统交互。AEON 采用轮式移动，高1.65米、重60公斤、负载最高10公斤、速度最高2.4米每秒，主要承担重复且体力要求高的任务。

**为什么重要：** 该项目以明确工序、量化硬件参数和分阶段试点检验人形机器人价值，为评估其在既有汽车产线中的人机协作与改造成本提供实际参照。

> 来源：Robotics & Automation News｜发布时间：2026-11-26 19:49

---

生成时间：2026-11-27T17:48:04+08:00

本日报由自动化系统辅助整理，重要信息请以原始来源为准。
