# 具身智能日报｜2026-11-18

## 1. [PAIR: Bringing Household Robots in](https://arxiv.org/abs/2611.23070v1)

家庭机器人经常需要操作家电，而智能家电同时提供实体控制面板和设备API；现有具身智能仿真环境却往往只把家电建模为物理对象。研究提出PAIR，面向这一建模缺口引入智能家电仿真，使电器使用研究能够同时考虑面板操作与API控制两类交互路径，而非仅处理物理对象，为家庭场景中的机器人电器操作提供更贴近现实的实验基础。截断摘要尚未列出环境规模、支持任务和实验结果。

**为什么重要：** 把家电物理界面与数字接口纳入同一研究框架，有助于缩小家庭机器人仿真训练与真实电器操作之间的差距，并拓展可评测的任务类型。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-18 00:58

## 2. [Outcome-Balanced PPO and Policy-In](https://arxiv.org/abs/2611.22878v1)

该研究围绕利用强化学习后训练基于流的视觉—语言—动作策略展开：策略通过与环境交互，优化预期任务回报，而不是只依赖既有模型训练。作者指出，这一优化过程带来两项挑战，摘要可见部分明确提到策略更新可能产生问题；从标题看，工作涉及结果均衡PPO及另一项策略机制，但截断材料没有给出其具体结构、损失设计、实验任务或量化改进。

**为什么重要：** 将流式VLA的后训练问题具体化，有助于研究者审视环境交互、回报优化与策略更新之间的关系，并为后续稳定性研究明确问题背景。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-17 22:52

## 3. [VSpark: Speculative Decoding for A](https://arxiv.org/abs/2611.22666v1)

该研究旨在加速自回归视觉—语言—动作模型，这类模型逐个token生成机器人动作，逐token的生成方式构成其效率背景。VSpark引入投机解码思路：由轻量级草稿模型一次提出多个token，再交由VLA处理后续流程，以减少完全依赖主模型顺序生成的限制。现有摘要未展开草稿模型与主模型的具体协作细节，也未给出速度提升、任务成功率或机器人实验数据。

**为什么重要：** 把投机解码引入动作token生成，为缓解自回归VLA的推理延迟提供明确方向，关系到机器人策略能否更高频地响应环境。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-17 20:22

## 4. [InteractVLA: Turning VLAs into Int](https://arxiv.org/abs/2611.22584v1)

现有智能体操作系统通常将预训练视觉—语言—动作策略视为不透明、仅通过语言调用的基础组件。面对陌生指令或场景扰动，一旦策略调用失败，上层智能体便无法进一步引导其行为。InteractVLA针对这一可交互性缺口展开，题目指向将VLA转变为可交互组件，使研究重点从单次调用延伸到失败后的行为引导；截断摘要尚未给出具体接口、训练方式、评测任务或性能数据。

**为什么重要：** 让上层智能体在失败后继续引导VLA，而非停留于一次性语言调用，是提升开放场景操作系统纠错与恢复能力的重要研究问题。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-17 19:07

## 5. [CoBoVLA: Decoupling Language from](https://arxiv.org/abs/2611.22395v1)

CoBoVLA关注视觉—语言—动作模型对指令改写的敏感性。现有模型虽在LIBERO基准上取得较高成功率，但从0.6B到7.5B参数的多类VLA，在LIBERO-Para上均出现22至52个百分点的性能下滑，说明扩大参数规模并未自然消除释义变化带来的问题。研究以解耦语言为题，指向降低动作策略对语言表述形式的依赖；摘要截断处未提供方法细节与最终实验结果。

**为什么重要：** 跨规模模型与明确降幅揭示释义鲁棒性短板，提醒评测不能只看原始指令成功率，也关系到真实语音和文本指令的可靠执行。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-17 16:43

## 6. [Fly as Instructed: Refining World-](https://arxiv.org/abs/2611.22883v1)

该研究面向自然语言引导的无人机导航，这类交互可带来直观的人机协作，并支持复杂环境中的灵活自主飞行。作者强调，可靠导航不仅需要准确遵循指令，还需要持续跟踪任务进展；研究以“按指令飞行”为题，核心是让导航过程同时服务于指令符合度与任务进度管理。可见摘要未说明具体模型、训练数据或仿真到实机设置，也没有给出飞行环境、对比基线和成功率等量化结果。

**为什么重要：** 持续进度跟踪把指令理解延伸到长程任务执行，有助于减少无人机偏航后仍盲目飞行的问题，是语言导航走向实用部署的关键能力。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-17 22:54

## 7. [Learning Agent-Centric Vision-Lang](https://arxiv.org/abs/2611.22880v1)

研究回顾了视觉—语言—动作模型与世界建模结合对端到端自动驾驶的推动：系统不再只对当前观测作出反应，还可围绕想象的未来进行推理。该工作以学习智能体中心的视觉—语言相关方法为题，延续这一研究语境，关注未来预测与驾驶决策的联系。由于摘要在此截断，尚不能确认其模型结构、智能体中心表示的具体形式、训练数据以及闭环或开环评测表现。

**为什么重要：** 把世界模型的未来想象与VLA驾驶决策结合，有助于研究从被动反应走向前瞻推理，但安全收益仍需闭环与真实道路验证。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-17 22:53

## 8. [RefCloth: Transferable Adversarial](https://arxiv.org/abs/2611.22736v1)

RefCloth研究闭环视觉—语言—动作策略面临的视觉攻击风险。此类策略持续依赖多视角相机，而已有攻击通常以二维贴片劫持传感器输入，或修改目标物体的网格；当操作对象发生变化时，后者还需要重新训练。工作题目指向可迁移的对抗性方案，意在讨论跨对象或场景的攻击问题，但截断摘要尚未给出RefCloth的实现方式、扰动约束、受害模型及攻击成功率等结果。

**为什么重要：** 揭示多视角闭环策略的视觉攻击面，可推动VLA安全评测从单帧扰动转向持续感知与对象变化条件，并补足部署前风险检查。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-17 21:06

## 9. [Inertial Video World Models](https://arxiv.org/abs/2611.22314v1)

该研究从物理世界的惯性出发，指出现实状态是在既有基础上连续演化，而非每个瞬间被重新生成。作者认为，许多现有视频世界模型缺少显式的惯性状态演化机制，因此难以在模型层面保证运动等过程的连续性。工作以“惯性视频世界模型”为题，核心问题是把既有状态及其延续纳入视频预测；可见摘要未介绍具体网络设计、训练目标、数据规模或与基线的定量比较。

**为什么重要：** 将惯性作为显式建模原则，直指视频世界模型的状态连续性，为机器人预测动态、规划动作和评估长期一致性提供研究切入点。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-17 15:09

## 10. [Body Schema Policy: Body as the Vi](https://arxiv.org/abs/2611.22713v1)

Body Schema Policy反思依靠规模学习全身移动操作的路径：当前最强策略拥有数十亿参数，仍需要针对具体任务微调。相比之下，人类处理能力有限，却能高效学习与行动，作者由此引出身体图式这一思路，尝试从身体本身寻找视觉与行动组织的依据。题目中的后续文字尚未完整显示，因此不能进一步确认其输入形式、模型规模、任务设置或是否减少对微调的依赖。

**为什么重要：** 若身体图式能替代部分规模堆叠与逐任务微调，将影响全身移动操作的数据和计算成本，也为跨任务学习提供不同归纳偏置。

> 来源：arXiv Robotics｜VLA WM VLN Manipulation UAV｜发布时间：2026-11-17 20:52

## 11. [Hyundai Motor Group Secures 100% S](https://news.google.com/rss/articles/CBMiWEFVX3lxTE9WVWZSQmh0Z2dTOU1aRzJIMDBmN25PXzI4MkhlaXZXN3BPYzVQRzY0ZFJLMFZob1d4U3liRkVKWjhIRXFwS3BxejBic04zMGtJY3JSZmdnTkc?oc=5)

据《金融新闻》标题所示，现代汽车集团已取得波士顿动力100%股权，并将此与加快机器人量产联系起来。现有材料仅明确股权比例和量产方向，未披露交易对价、交割时间、融资安排或此前持股结构，也没有说明波士顿动力哪些产品会扩产、产能目标及落地工厂。因此，该消息可确定的重点是现代汽车集团实现全资控制，以及机器人业务被置于更明确的规模化生产议程中。

**为什么重要：** 全资控制有助于整车集团统一机器人研发、制造与商业化决策，但实际产业影响仍取决于量产产品、持续投资和产能安排。

> 来源：파이낸셜뉴스｜发布时间：2026-11-17 07:05

## 12. [Nearing AI Robotics Breakthrough W](https://news.google.com/rss/articles/CBMizAFBVV95cUxNX19KTUdXRTNybDVWUlRnamNtaHpOYVNCb0Q4VEhXU0REaVhmMVJBMVY2Q1dCM3R2Y0dnckpiLVNBeVBYT09DYXpXZ21jbkFSZWxwbFN5eWFMdFJTYjRJaWFxdjdpQzVqa1QxOTNmUllUemtZWTJvQzhqdGxOaGFxUHk1ZklrV1NVT0NtMWdENWdjX0JjNjdZQ0E4U1lUU2FXakxWSkd4UVZVUDlXX1hnQ1hxYUllc2VSTFV6akhXalBXV0FwRXRtTUlpY0w?oc=5)

财新全球报道标题显示，宇树科技创始人表示，若AI机器人领域接近突破，现有生产能力将面临压力。这一表态把技术进展与制造供给直接联系起来，但现有摘要未说明其所指突破的具体技术门槛、时间判断或适用产品，也未披露宇树当前产能、订单规模、扩产计划及供应链瓶颈。因而可确认的信息是创始人对潜在产能紧张作出预警，不能据此推断企业已经缺货或确定了增产数字。

**为什么重要：** 这一判断提示行业竞争不只在模型与本体性能，也在制造和交付能力；不过具体产能缺口及扩产必要性仍需企业数据佐证。

> 来源：Caixin Global｜发布时间：2026-11-17 14:56

## 13. [Microsoft Ignite 2026 | Explore Mo](https://news.google.com/rss/articles/CBMiWkFVX3lxTE9wSWtxNmQxNDB1V1lMSUdubGdyM1ZyTjlVYzMzRFNTeEs3RVM0WkZlT1luUVNSSFlQeE0yc3pGNUhCT3l3eXFjc2Zfbk9uNzlYbGpjOFlBTldSUQ?oc=5)

现有材料仅显示该页面属于Microsoft Source，标题为“Microsoft Ignite 2026 | Explore More”，未提供任何与具身智能、机器人产品或研究进展相关的正文。页面标题只能确认其指向微软Ignite 2026的更多内容入口，无法判断其中是否包含AI基础设施、机器人开发工具或现场演示，也不能提取具体发布事项、技术参数、客户案例和可用时间。因此，本条不具备进一步概述技术进展的事实基础。

**为什么重要：** 该条目暂无可核实的机器人技术信息，日报应避免把大会导航页误作产品发布；明确证据边界可防止向读者引入无依据的具身智能叙事。

> 来源：Microsoft Source｜发布时间：2026-11-17 07:19

## 14. [Boston Dynamics’ Atlas humanoid la](https://news.google.com/rss/articles/CBMimwFBVV95cUxPOTRNdjY3dzFkQlVNeXdNSXpjMTM4UGRxYUJWaHN5dng2Qkk1ZHkwZWNVMmhWSlFBVi1HMzdkQ3RYdzlOVVRKRkpqdlZuU1VTWGxVNmlCSHdrWWtHcnRBYVdsTzItYUpSQWQxTGtUTkMweFdUZEJzQUM4LUtXTU1Zd1pXV1RWRXRJMWtRY0wzWlJOQUJaNktKempERQ?oc=5)

The Robot Report标题显示，波士顿动力Atlas人形机器人获得首个非汽车领域试用。现有摘要没有说明试用客户、所在行业、具体任务、部署地点与持续时间，也未给出机器人自主程度、负载、班次表现或安全数据。因此，可以确认的是Atlas的试验场景开始超出汽车领域，不能进一步将其表述为正式商业部署、规模交付或已经通过生产验收；该事件目前更适合作为应用边界扩展的早期信号。

**为什么重要：** 从汽车场景走向其他行业试用，可检验人形机器人的任务泛化和现场适配能力，但商业价值仍取决于持续运行与客户验收数据。

> 来源：The Robot Report｜发布时间：2026-11-17 23:32

## 15. [Can AI help build a healthier futu](https://www.microsoft.com/en-us/research/podcast/can-ai-help-build-a-healthier-future)

微软研究院播客《The Shape of Things to Come》中，Doug Burger与Ava Amini、Eric Horvitz及Scripps Research的Eric Topol讨论AI如何改变医学。议题涵盖AI辅助诊断、医学影像、全患者模型、虚拟细胞、生物基础模型，以及AI指导实验和药物发现；嘉宾同时强调，有前景的研究走向患者可能缓慢，更好的生物数据与真实世界验证仍是必要条件。正文还介绍Amini参与AI与精准医学交叉研究，并共同领导Project Ex Vivo。

**为什么重要：** 虽然主题并非机器人，这些讨论为医疗具身智能提供上游视角：诊断与实验模型要进入临床，同样离不开高质量数据和真实世界验证。

> 来源：Microsoft Research｜发布时间：2026-11-18 00:52

---

生成时间：2026-11-18T17:36:41+08:00

本日报由自动化系统辅助整理，重要信息请以原始来源为准。
