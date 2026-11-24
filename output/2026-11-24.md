# 具身智能日报｜2026-11-24

## 1. [World Models as Native Latent Action Models](https://arxiv.org/abs/2611.30898v1)

该研究将预训练世界模型直接用作原生潜在动作模型，试图从第一人称人类视频和异构机器人录像中恢复可迁移的动作结构，即使素材没有动作标签、也不共享统一动作空间。相比从头训练逆动态与前向动态模型、并在像素重建和潜变量容量及精度间取舍的传统路线，它强调复用视频模型已学到的动态先验。候选摘要未给出架构细节、数据规模或实验指标，核心价值在于为大规模无动作标注视频服务机器人学习提供路径。

**为什么重要：** 若该思路成立，可降低动作标注与跨机器人数据对齐成本，让世界模型和无标签人类视频更直接地服务操作策略学习。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-24 00:01

## 2. [WeaveVLA: 3D Relational Grounding for Vision-Language-Action Models](https://arxiv.org/abs/2611.31126v1)

WeaveVLA面向指令条件下的机器人控制，将任务相关三维关系及其在操作过程中的变化显式纳入动作生成，弥补VLA主要依赖预训练视觉语言表征、对空间结构多为隐式理解的不足。该工作不以单纯扩大骨干网络为重点，而是让三维关系成为动作生成可直接利用的结构信息，目标是改善复杂操作中的关系理解与动作决策。现有摘要未披露具体表示方式、训练配置和实验结果，因此不能量化其相对提升。

**为什么重要：** 显式三维关系有望提升VLA对空间变化和任务结构的建模能力，也为诊断复杂操作失败提供比隐式表征更清晰的结构入口。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-24 01:59

## 3. [DexLatentWorld: 3D Cross-Embodiment Latent Action World Models for Zero-Shot Robotic Manipulation](https://arxiv.org/abs/2611.30907v1)

DexLatentWorld提出三维跨本体潜在动作世界模型，面向零样本机器人操作，试图同时降低动作监督成本和对训练时机器人形态的依赖。它将动态预测、三维表示与跨本体迁移纳入统一框架，以潜在动作缓解真实交互数据昂贵、难以规模化的问题，并探索世界模型向未见机器人形态迁移。候选材料未说明模型组成、训练数据、零样本设定或操作成功率，能够确认的是研究目标与整体技术路线。

**为什么重要：** 统一三维动态与潜在动作表示，可能减少为新机器人重复采集动作数据的需求，推动世界模型跨硬件复用和零样本操作研究。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-24 00:05

## 4. [Real2Worlds2Real: Scaling Self-Improving Agentic Real2Sim2Real for Robot Manipulation](https://arxiv.org/abs/2611.31098v1)

Real2Worlds2Real提出可持续自我改进的代理式Real2Sim2Real流程，用基于真实观察的仿真支持机器人操作策略学习，重点扩展多任务与复杂物理交互覆盖。针对真实交互采集成本高、既有Real2Sim2Real难以覆盖多样任务和物理交互的问题，该工作不只做单次仿真重建，而是持续完善学习闭环，使流程具备扩展和自我改进能力。现有摘要未给出代理模块、仿真生成方式、任务规模或真实机器人指标。

**为什么重要：** 自我改进的仿真学习闭环若可扩展，将降低多任务真实采集压力，并为复杂物理交互下的策略训练与迭代提供基础设施。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-24 01:39

## 5. [Wrist-Camera Video Diffusion as Generalizable Robot Policies](https://arxiv.org/abs/2611.31079v1)

Wrist Video Policy将腕部相机视频扩散用于通用机器人操作，采用闭环框架先学习预测操作过程，再通过几何估计恢复可执行运动。其核心表示是腕部相机轨迹，用这一接口连接视觉未来预测与机器人动作解码，使视频扩散不止生成未来画面，还能服务实际运动恢复，面向新任务、陌生场景和跨本体迁移。候选摘要未提供轨迹参数化、策略训练细节、实验平台或泛化指标，因此尚不能判断其提升幅度。

**为什么重要：** 腕部轨迹把生成式视频预测接到可执行运动上，为利用视频扩散的泛化能力、同时保留机器人控制所需几何约束提供新接口。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-24 01:29

## 6. [Hugging Face发布RoboTrack真实机器人操作点跟踪基准与训练数据](https://huggingface.co/blog/allenai/robotrack)

Hugging Face发布RoboTrack真实机器人操作点跟踪套件：RoboTrack-Bench汇集来自DROID、Ego-Exo4D、MolmoAct 2和EgoVerse的307段人工标注视频，覆盖不同机器人与人手、遮挡杂乱场景及第一、第三人称视角；RoboTrack-15M则通过MolmoSpaces仿真生成稠密点轨迹。评测显示领先跟踪器在该基准得分明显低于既有机器人基准，加入合成数据可改善真实操作视频表现；同时开放RoboTracker与RoboTracker-Warp，后者在五项基准中的四项达到最佳

**为什么重要：** 该套件用更贴近真实遮挡和视角变化的测试暴露感知短板，并以可复用数据、模型和湿实验验证连接操作学习。

> 来源：Hugging Face Blog｜发布时间：2026-11-24 01:20

## 7. [RoboUniverse-10K: Toward the Scaling Era of Agentic Robotics via Real-to-Sim Environments](https://arxiv.org/abs/2611.31002v1)

RoboUniverse-10K以Real-to-Sim环境推动代理式机器人规模化，面向基础模型作为编码代理、生成可执行程序来控制机器人的训练与评估。它针对该方向缺少类似软件工程的大规模可执行环境和后训练生态、评测又常局限于小型人工基准及分布内任务的问题，试图扩充环境数量、任务覆盖和泛化测试基础。现有材料未列出环境实际构成、任务数量、生成流程或基准结果，除名称外不宜推断“10K”的具体统计口径。

**为什么重要：** 规模化可执行环境与分布外评测是编码代理机器人后训练的基础，该方向有助于让不同系统的比较更接近真实任务泛化。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-24 00:53

## 8. [EmboEagle: An Efficient Agentic Embodied Framework for Long-horizon Robotic Manipulation](https://arxiv.org/abs/2611.31173v1)

EmboEagle提出面向长时程机器人操作的高效代理式具身框架，将子任务条件下的World-Action Model控制与监督机制组成闭环。它针对独立WAM连续执行时累积物理误差，以及无状态VLM监督造成分块延迟、缺乏三维空间持续性的问题，重点协调误差修正、空间记忆和跨子任务执行。其设计强调不同模型与控制环节的闭环协同，而非单独扩大某个策略模型；候选摘要未提供效率数据、任务时长或成功率。

**为什么重要：** 闭环监督与空间持续性直接针对长任务误差累积和执行停顿，对提升多阶段操作的可靠性及代理框架效率具有研究价值。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-24 02:31

## 9. [Boltz-Flow: Generating High-Quality Robot Action from Boltzmann Machine](https://arxiv.org/abs/2611.31038v1)

Boltz-Flow将玻尔兹曼机引入流匹配机器人动作策略，重点改变从固定、与观测无关的高斯源积分速度场的做法。针对单模态源可能限制多任务表达规模，以及时间步和控制维度独立分解损失协调信息的问题，它让动作生成的源分布突破固定高斯假设，以更好表达多模态结构与动作耦合关系。该思路面向任务多样性增长后的策略扩展，但现有摘要未披露训练方式、采样成本、基准任务或性能对比。

**为什么重要：** 更具表达力的源分布可能改善多任务动作的多模态与关节协调建模，但其产业价值仍取决于采样效率及真实控制验证。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-24 01:10

## 10. [Foresight Forcing: Learning Spatial Foresight for Robotic Manipulation](https://arxiv.org/abs/2611.30963v1)

Foresight Forcing面向World Action Model训练引入空间预见学习，使模型在预测未来视觉之外，还显式学习物体运动、三维几何转移和空间关系变化。它针对未来画面预测目标通常不直接约束三维几何学习的问题，试图弥合视觉预测与物理空间结构之间的断层，让预见信息能够支撑更可靠的操作动作生成与规划。候选摘要未说明空间监督形式、模型结构、训练数据或实验指标，因此只能确认其训练目标与问题设定。

**为什么重要：** 把三维几何变化纳入未来预测，可推动世界动作模型从画面相似走向空间一致，为接触操作和长期规划提供更可靠的预见信息。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-24 00:32

## 11. [WorldLeague: Benchmarking Physical Agency](https://arxiv.org/abs/2611.30989v1)

WorldLeague围绕“Physical Agency”提出评测问题，将Blender操作、复杂视频游戏中的指令执行和机械臂物体操控放在同一视野，追问当今AI系统能够自主完成哪些物理目标。现有材料只说明回答该问题需要开展系统测试，未提供任务集合、参评模型、评分指标或实验结论，因此不能判断其覆盖规模与结果；可确认的关注点，是用更系统的测试界定物理代理的自主能力范围，而非报道某一机器人技能提升。

**为什么重要：** 统一讨论软件、游戏与机械臂中的自主物理目标，有助于界定具身代理能力边界，但需完整任务与指标才能形成可比较结论。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-24 00:44

## 12. [Figure AI申请可穿戴机械臂系统专利，支持动作采集与人形机器人遥操作](https://roboticsandautomationnews.com/2026/11/23/figure-ai-patents-wearable-system-for-teaching-humanoid-robots-through-human-movement/107567)

Figure AI的可穿戴机器人系统专利US 2026/0364774 A1于2026年11月19日公开，方案用背包式框架和两条越肩机械臂跟随人体，肩、肘、腕由编码器与惯性测量单元采集运动，每臂最多七个旋转轴。数据既可训练人形机器人，也可实时遥操作；申请描述端到端延迟低于20毫秒、可中断传输的离合机构及机器人相机视频头显，目标是在工厂、仓库等日常作业中采集示范，但仍属专利布局而非产品部署。

**为什么重要：** 若方案实现，可把工人日常操作转化为训练示范并兼顾低延迟遥操作，为人形机器人缓解真实数据采集成本提供新硬件路径。

> 来源：Robotics & Automation News｜发布时间：2026-11-24 06:43

## 13. [消息称英伟达董事会一致同意恢复黄仁勋首席执行官职务](http://www.bing.com/news/apiclick.aspx?ref=FexRss&tid=6b0570d6ca9840a0b463ad4a7d26f201&url=https%3A%2F%2Fapnews.com%2Fvideo%2Fwhy-did-nvidia-reinstate-jensen-huang-5a7f94f8fb5f4437a842e5420c0a1941&c=17575256088637658657&mkt=en-us)

现有消息称，英伟达董事会在最初拒绝黄仁勋回归提议后，又一致同意恢复其首席执行官职务，美国总统特朗普也支持其回归。材料同时提到黄仁勋仍面临国会相关事项，但原文截断，未交代董事会决定的时间线、离任与复职原因、国会事项具体内容或公司正式公告。该条目因此只能作为领导层变动消息概述，不能延伸推断其对产品、股价或机器人业务的实际影响。

**为什么重要：** 若消息属实，核心领导层变化可能影响英伟达AI计算与机器人生态的战略连续性，但当前信息不足以评估具体产业后果。

> 来源：Bing News EN｜Global Major Media｜发布时间：2026-11-23 20:43

## 14. [英伟达发布假日技术指南，涵盖RTX创作游戏与Jetson机器人入门](https://blogs.nvidia.com/blog/nvidia-technologies-holidays-2026)

英伟达假日技术指南汇总游戏、内容创作和机器人入门方案：GeForce RTX 50系列基于Blackwell，配备第五代Tensor Core与第四代RT Core，并介绍DLSS 5、Reflex、G-SYNC及拥有逾4500款游戏的GeForce NOW。创作部分提及RTX Spark和NVIDIA Studio；机器人部分以摄像头识别糖果手杖、姜饼人为例，建议通过反复测试探索视觉感知，并引出Jetson边缘AI平台，但截断正文未给出套件配置或性能数据。

**为什么重要：** 该指南虽非机器人研究发布，但把Jetson与低门槛视觉实验结合，有助于降低边缘AI和具身感知原型的入门门槛。

> 来源：NVIDIA Blog｜发布时间：2026-11-24 01:00

## 15. [ASRock Industrial发布RBK-100集成式物理AI机器人开发平台](https://roboticsandautomationnews.com/2026/11/24/asrock-industrial-launches-robotics-in-a-box-for-physical-ai-development/107570)

ASRock Industrial推出RBK-100 Robotics-in-a-Box，以NUC BOX-358H和英特尔Core Ultra X7 358H提供本地计算，集成RGB-D相机、六自由度主从机械臂及AiRoboStarter软件。平台标配32GB DDR5、512GB PCIe Gen4 SSD，64GB高级版增加语音、大模型、视觉和技能串联的代理式AI流程；软件覆盖演示录制、数据检查、训练与执行，支持ACT、Pi0.5，SmolVLA列为后续计划。

**为什么重要：** 一体化主从臂、视觉、计算与训练执行软件可减少系统集成工作，为教学、模仿学习实验及物理AI原型提供较低门槛入口。

> 来源：Robotics & Automation News｜发布时间：2026-11-24 14:26

---

生成时间：2026-11-24T19:11:17+08:00

本日报由自动化系统辅助整理，重要信息请以原始来源为准。
