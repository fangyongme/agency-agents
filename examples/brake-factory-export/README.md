# 中国刹车泵工厂：最小海外获客团队

基于 `fangyongme/agency-agents` 的四人 Codex 项目预设。基线为已合并的
[PR #60](https://github.com/fangyongme/agency-agents/pull/60)，提交
`479193dcce1cf6432ce0f5aa230ab8cc739a8c6b`。用途是帮助真实工厂获得合格询盘。

## 只保留四个 Agent

| 原仓库 Agent | 本项目职责 | 输入 | 输出及下一步 |
| --- | --- | --- | --- |
| Outbound Strategist | 客户研究、ICP、B2B 潜客筛选 | 工厂档案、目录、目标市场、公开商业证据、历史买家 | research.md 给内容负责人；qualification.json 给销售 |
| Social Media Strategist | 内容主线、LinkedIn 成稿、四平台一致性、效果复盘 | 客户问题、已核实产品事实、真实素材 | content-brief.md、linkedin.md、review.md；把母稿交给视频负责人 |
| Video Optimization Specialist | TikTok、Instagram、YouTube 发布素材包 | 已确认母稿、实拍素材、产品术语 | 分平台脚本、字幕稿、镜头表、封面/缩略图、标题、说明、CTA |
| Sales Outreach | 首次外联、回复分流、询价澄清、内部报价交接及跟进 | 合格潜客、已核验联系方式、真实来信、目录及批准报价 | 逐客外联稿、RFQ JSON、澄清/报价回复稿、下一步 |

主 Codex 会话负责调度、审核交接和唯一台账写入，不再安装一个“经理 Agent”。
流程是：研究 → 内容母稿 → 四平台素材 → 潜客筛选 → 首次外联 → RFQ 跟进。
筛选可以在研究后与内容生产同时推进；真实询价可以直接进入 RFQ 流程。

**暂不安装** LinkedIn Content Creator、TikTok Strategist、Instagram Curator：
现阶段平台职责已合并到内容和视频两人，避免同一母稿多人重复改写。
Growth Hacker 暂缓：先获得真实询盘和报价数据，再决定是否需要独立增长实验角色。
这不是断言这些 Agent 缺失，而是有意收窄首期团队。

## 在 Codex 项目使用

需要 Python 3.11+、Bash、Perl 及仓库脚本使用的标准命令；不需要 pip 依赖。
Linux/macOS 可直接运行；Windows 推荐在 WSL 中运行。仅 Linux 在本次验证范围内。

从克隆的仓库根目录执行，建议目标目录是新的独立项目：

```bash
python3 examples/brake-factory-export/setup.py --project ../brake-factory-codex --dry-run
python3 examples/brake-factory-export/setup.py --project ../brake-factory-codex
```

然后在 Codex 中打开 `brake-factory-codex`，新建会话。填写
`knowledge/factory-profile.json`，把目录、素材、客户文件放进 `work/`。
两者已忽略，不应提交到公开 Git 仓库。运行 `RUNBOOK.md` 的启动提示词：

> 读取 AGENTS.md 和工厂档案。建立 pilot-001，先让 Outbound Strategist
> 做客户研究，再由 Social Media Strategist 产出一个内容母稿和 LinkedIn
> 草稿，交给 Video Optimization Specialist 做 TikTok、Instagram、YouTube
> 素材包。整理缺少的证据和素材，完成后给我审核队列。

需要筛选潜客或处理询价时，运行 RUNBOOK 中对应提示词，不必每次从头执行。
无原生子 Agent 能力时，AGENTS.md 提供单会话按角色顺序执行的降级方式。

## 如何复用仓库机制

1. `manifest.json` 锁定四个原始 Agent、原脚本及基线哈希，`agents.txt`
   使用现成的 `--agents-file` 格式。
2. `setup.py` 在临时目录复制原有 `convert.sh`、`install.sh`、`lib.sh`
   和 divisions 清单。仅放入四个角色的工厂裁剪版本。
3. 原版 `convert.sh --tool codex` 生成 TOML，再用原版
   `install.sh --tool codex --agents-file ... --no-convert --path ...` 安装。
   不新造转换器、不扫描安装整个 Agent 库。
4. 最终项目包含 `.codex/agents/` 的四个 TOML、AGENTS.md、业务规则、运行手册、
   模板、空白私有台账和来源清单。生成文件不提交到这个源仓库。

`roles/` 是可维护的业务裁剪正文，保留四个上游角色身份和核心方法；**不是**
把原始全文照搬后追加几句提醒。通用 SaaS 信号、高频外联、增长保证和无关平台
被移除。所有角色共用项目业务规则。未来同步改变已锁定源文件时，安装会停下并
指出文件，要求先审查差异再更新清单，防止无声回退。

这是项目级自定义 Agent 格式；Codex 官方要求 `name`、`description` 和
`developer_instructions`，项目目录为 `.codex/agents/`：
[官方说明](https://developers.openai.com/codex/subagents)。未强制指定模型、修改权限、
修改已有 `.codex/config.toml` 或安装到用户全局目录。

重复运行会保留私有档案、台账和无关文件；已有指令文件不同则在写入前报错。
更新时生成同级新项目审查差异后再合并，避免覆盖本地修改。安装不会删除用户
原有其他 Agent；要获得严格的四人环境，应使用新的项目目录。

## 业务交接要求

- 潜客按五项证据评分；达到 70 分仍需通过产品相关性、市场可承接、联系方式、
  去重和拒收检查。分数是内部试行规则，不是购买概率。
- 一份内容分别输出 LinkedIn、TikTok、Instagram、YouTube 素材；只有脚本时
  明确标注待拍摄/剪辑，不能报告已生成视频或已发布。
- OE 保留原文和原行号，近似、缺位、OCR 不确定的号码进入产品复核，不自动补
  所谓校验位。价格、MOQ、交期、币种、贸易条款只来自批准的内部报价。
- 一个买家跨平台共用 ID。授权、发送成功、收到回复、有效报价、确认订单及收款
  分别记录；台账由主会话统一更新。
- 外联及发布先完成精确内容和目标审核；复用已有有效授权。未连接平台时交付稿件，
  不声称已经发送。此配置本身不包含采集服务、视频渲染、平台账号连接或自动定时器。

启动真实业务前需补充：工厂名称和真实发信身份、目标国家、实际产品目录、可公开
工厂素材、商务条款/报价负责人。档案中的未知项保持空白，不妨碍先做研究和素材规划。

## 验证

```bash
python3 examples/brake-factory-export/test_setup.py
```

测试覆盖真实转换/安装、仅四个 TOML、含空格路径、dry-run、重复运行保留台账、
已有文件冲突和符号链接保护。`acceptance-scenarios.md` 另列 14 项业务行为检查，
供实际 Codex 会话验证；安装测试不等于已完成真实获客或模型行为评测。

本预设沿用已有运营材料确认的“个人代表工厂、日系/韩系/中国品牌适配、内部
报价工具”定位、合格询盘口径与观察窗口；未把旧排期当成已发布业绩，也未把
其他渠道自动加入本次四平台范围。原仓库 MIT 许可随生成项目附带。
