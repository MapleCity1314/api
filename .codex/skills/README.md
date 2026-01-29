# SpoonOS Development Skills

Developer enablement skills for building agents and dApps with the SpoonOS framework.

## Core Skills

| Skill | Description | Use Case |
|-------|-------------|----------|
| [Agent Development](agent-development/SKILL.md) | Build AI agents with SpoonReactMCP | Custom agents, toolchains, prompts |
| [Graph Development](graph-development/SKILL.md) | StateGraph workflow construction | Multi-step workflows, routing, parallelism |
| [Tool Development](tool-development/SKILL.md) | MCP tools and extensions | BaseTool, FastMCP servers |
| [Testing Patterns](testing-patterns/SKILL.md) | Testing strategies | Unit tests, mocking, CI/CD |

## Platform & Deployment

| Skill | Description | Use Case |
|-------|-------------|----------|
| [Platform Integration](platform-integration/SKILL.md) | Deploy to messaging platforms and APIs | Telegram, Discord, REST APIs, webhooks |
| [Deployment Guide](deployment-guide/SKILL.md) | Production deployment patterns | Docker, AWS, GCP, Vercel |
| [Application Templates](application-templates/SKILL.md) | Ready-to-use agent templates | Trading bots, NFT minters, DAO assistants |

## Identity & Security

| Skill | Description | Use Case |
|-------|-------------|----------|
| [ERC-8004 Standard](erc8004-standard/SKILL.md) | Trustless agent identity | On-chain registration, reputation |
| [Identity & Auth](identity-auth/SKILL.md) | Web3 auth and identity | SIWE, ENS, credentials |
| [Security Analysis](security-analysis/SKILL.md) | Web3 security risk analysis | Honeypot/rug checks, transaction simulation |

## Web3 Domains

| Skill | Description | Use Case |
|-------|-------------|----------|
| [DAO Tooling](dao-tooling/SKILL.md) | DAO governance agents | Proposals, voting, delegation |
| [DeFi Protocols](defi-protocols/SKILL.md) | DeFi protocol integrations | Aave, Compound, DEX aggregators |
| [DeFi Interaction](defi/SKILL.md) | DeFi interaction skill | Swaps, lending, yield |
| [NFT Analysis](nft/SKILL.md) | NFT market analysis | OpenSea, Blur, Magic Eden |
| [Onchain Analysis](onchain-analysis/SKILL.md) | On-chain analytics | Etherscan, Dune, explorers |
| [Neo Ecosystem](neo/SKILL.md) | Neo N3 integration | Wallets, contracts, NeoFS |
| [Solana Ecosystem](solana/SKILL.md) | Solana ecosystem integration | DeFi, NFTs, tooling |
| [Bridge](bridge/SKILL.md) | Cross-chain bridges | LayerZero, Wormhole, Stargate |
| [Wallet Operations](wallet/SKILL.md) | Wallet ops | Balance, transfers, portfolio |

## Workflow & UX

| Skill | Description | Use Case |
|-------|-------------|----------|
| [Brainstorming](brainstorming/SKILL.md) | Pre-implementation ideation | Requirements, options, design |
| [Vercel React Best Practices](vercel-react-best-practices/SKILL.md) | React/Next.js performance guide | Component/data fetching optimization |

## Quick Start

### Create an Agent

```python
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager

agent = SpoonReactMCP(
    name="my_agent",
    llm=ChatBot(model_name="gpt-4o"),
    tools=ToolManager([MyTool()]),
    max_steps=15
)

result = await agent.run("Your query")
```

### Build a Workflow

```python
from spoon_ai.graph import StateGraph, END

graph = StateGraph(MyState)
graph.add_node("process", process_node)
graph.set_entry_point("process")
graph.add_edge("process", END)

app = graph.compile()
```

### Create a Tool

```python
from spoon_ai.tools.base import BaseTool

class MyTool(BaseTool):
    name: str = "my_tool"
    description: str = "Tool description"

    async def execute(self, **kwargs) -> str:
        return "Result"
```

## Directory Structure

```
spoonos-skills/
├── agent-development/      # Agent patterns
├── graph-development/      # Workflow graphs
├── erc8004-standard/       # On-chain identity
├── tool-development/       # Tool creation
├── application-templates/  # Ready-to-use templates
├── platform-integration/   # Platform deployment
├── deployment-guide/       # Production deployment
├── testing-patterns/       # Testing strategies
└── README.md
```

## Prerequisites

- Python 3.12+
- SpoonOS Core (`pip install spoon-ai`)

## Related

- [Web3 Skills](../web3-skills/README.md) - Blockchain integrations
