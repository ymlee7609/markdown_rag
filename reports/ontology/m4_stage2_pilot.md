# M4 Stage 2 — LLM 검증 리포트

생성: 2026-05-22T16:03:45.004800
입력: `data/ontology/chunk_enrichment.jsonl.gz`
출력: `data/ontology/chunk_enrichment_validated.jsonl.gz`
검증 범위: tier=theory,implementation, suspect_tags=`proto:nat,proto:rip,feat:power-supply`, min_candidates=2
doc-broadcast: ON

## 요약

- 전체 처리: **1000** records
- 검증 대상 (LLM 호출): **630**
- skip (passthrough): 370
- LLM 호출 수: doc-level **23**, chunk-level **837**
- 평균 chunk-level latency: **2.52s**
- 총 소요: **1120.8s** (18.7분)
- status: validated=318, broadcast_only=271, parse_error=41, no_text=0, llm_error=0, skipped=370

## per-tag

| tag | candidates | validated | rejected | rejection rate |
|---|---|---|---|---|
| `proto:nat` | 345 | 79 | 266 | 77.1% |
| `proto:vlan` | 211 | 118 | 93 | 44.1% |
| `proto:stp` | 166 | 75 | 91 | 54.8% |
| `feat:port-mirroring` | 146 | 58 | 88 | 60.3% |
| `concept:vlan-trunk` | 94 | 51 | 43 | 45.7% |
| `feat:power-supply` | 80 | 23 | 57 | 71.2% |
| `proto:ipv6` | 71 | 25 | 46 | 64.8% |
| `proto:rip` | 61 | 15 | 46 | 75.4% |
| `proto:rstp` | 48 | 27 | 21 | 43.8% |
| `proto:ipv4` | 44 | 19 | 25 | 56.8% |
| `proto:dhcp` | 39 | 15 | 24 | 61.5% |
| `proto:arp` | 34 | 12 | 22 | 64.7% |
| `concept:stp-root-bridge` | 32 | 21 | 11 | 34.4% |
| `proto:eigrp` | 24 | 1 | 23 | 95.8% |
| `proto:tcp` | 24 | 13 | 11 | 45.8% |
| `proto:snmp` | 24 | 6 | 18 | 75.0% |
| `proto:ospf` | 23 | 12 | 11 | 47.8% |
| `proto:udp` | 21 | 5 | 16 | 76.2% |
| `proto:ppp` | 20 | 3 | 17 | 85.0% |
| `proto:pppoe` | 17 | 5 | 12 | 70.6% |
| `proto:ntp` | 14 | 4 | 10 | 71.4% |
| `feat:mac-address-table` | 14 | 3 | 11 | 78.6% |
| `proto:qos` | 13 | 4 | 9 | 69.2% |
| `proto:lacp` | 13 | 6 | 7 | 53.8% |
| `feat:dot1q-tunnel` | 12 | 10 | 2 | 16.7% |
| `proto:mstp` | 12 | 3 | 9 | 75.0% |
| `proto:acl` | 12 | 7 | 5 | 41.7% |
| `proto:bgp` | 10 | 3 | 7 | 70.0% |
| `proto:icmp` | 10 | 1 | 9 | 90.0% |
| `proto:tls` | 9 | 0 | 9 | 100.0% |
| `proto:dhcpv6` | 9 | 5 | 4 | 44.4% |
| `proto:vrrp` | 9 | 7 | 2 | 22.2% |
| `proto:syslog` | 8 | 2 | 6 | 75.0% |
| `proto:ndp` | 8 | 4 | 4 | 50.0% |
| `proto:lldp` | 7 | 1 | 6 | 85.7% |
| `proto:ripng` | 6 | 1 | 5 | 83.3% |
| `proto:ssh` | 6 | 0 | 6 | 100.0% |
| `proto:mpls` | 5 | 3 | 2 | 40.0% |
| `feat:clock-config` | 5 | 0 | 5 | 100.0% |
| `proto:isis` | 4 | 3 | 1 | 25.0% |
| `proto:ospfv3` | 4 | 4 | 0 | 0.0% |
| `concept:mac-learning` | 4 | 1 | 3 | 75.0% |
| `concept:ospf-lsa` | 3 | 2 | 1 | 33.3% |
| `concept:ospf-neighbor` | 3 | 2 | 1 | 33.3% |
| `concept:ospf-area` | 2 | 0 | 2 | 100.0% |
| `proto:igmp` | 2 | 0 | 2 | 100.0% |
| `proto:radius` | 2 | 0 | 2 | 100.0% |
| `proto:icmpv6` | 2 | 1 | 1 | 50.0% |
| `proto:mld` | 1 | 0 | 1 | 100.0% |
| `feat:port-security` | 1 | 0 | 1 | 100.0% |

## reject reason 샘플 (상위 10)

(none collected — use --keep-reasons)

## validated 예시 (앞 10)

- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/00_front-matter.md::chu` → ['proto:nat']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['proto:nat']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['proto:bgp', 'proto:mpls', 'proto:qos']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['proto:nat']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['proto:nat']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['concept:vlan-trunk', 'feat:port-mirroring', 'proto:stp', 'proto:vlan']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['concept:vlan-trunk', 'feat:port-mirroring', 'proto:stp', 'proto:vlan']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['proto:isis', 'proto:ospf', 'proto:rip']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['concept:vlan-trunk', 'feat:dot1q-tunnel', 'feat:port-mirroring', 'proto:vlan']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['feat:port-mirroring', 'proto:nat', 'proto:stp', 'proto:vlan']

## rejected 예시 (앞 10)

- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/00_front-matter.md::chu` → ['proto:nat']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['proto:rip']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['feat:power-supply', 'proto:eigrp']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['proto:eigrp', 'proto:ripng']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['proto:nat', 'proto:ppp', 'proto:pppoe', 'proto:stp']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['concept:stp-root-bridge', 'proto:mstp', 'proto:rstp']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['feat:port-mirroring']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['proto:tcp', 'proto:tls']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['proto:arp', 'proto:dhcpv6', 'proto:nat', 'proto:snmp', 'proto:syslog']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/02_fifth-edition.md::ch` → ['proto:eigrp', 'proto:rip', 'proto:ripng']
