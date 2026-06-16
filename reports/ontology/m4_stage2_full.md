# M4 Stage 2 — LLM 검증 리포트

생성: 2026-05-22T22:24:54.079657
입력: `data/ontology/chunk_enrichment.jsonl.gz`
출력: `data/ontology/chunk_enrichment_validated.jsonl.gz`
검증 범위: tier=theory,implementation, suspect_tags=`proto:nat,proto:rip,feat:power-supply`, min_candidates=2
doc-broadcast: ON

## 요약

- 전체 처리: **515043** records
- 검증 대상 (LLM 호출): **9635**
- skip (passthrough): 504408
- LLM 호출 수: doc-level **646**, chunk-level **12262**
- 평균 chunk-level latency: **3.02s**
- 총 소요: **22814.7s** (380.2분)
- status: validated=5161, broadcast_only=4307, parse_error=167, no_text=0, llm_error=0, skipped=504408

## per-tag

| tag | candidates | validated | rejected | rejection rate |
|---|---|---|---|---|
| `proto:nat` | 2740 | 499 | 2241 | 81.8% |
| `proto:vlan` | 2721 | 1563 | 1158 | 42.6% |
| `proto:igmp` | 1414 | 666 | 748 | 52.9% |
| `proto:stp` | 1230 | 831 | 399 | 32.4% |
| `proto:rip` | 1181 | 375 | 806 | 68.2% |
| `proto:ospf` | 1140 | 703 | 437 | 38.3% |
| `feat:port-mirroring` | 1063 | 658 | 405 | 38.1% |
| `proto:dhcp` | 1018 | 587 | 431 | 42.3% |
| `proto:bgp` | 843 | 426 | 417 | 49.5% |
| `proto:arp` | 780 | 474 | 306 | 39.2% |
| `proto:acl` | 727 | 414 | 313 | 43.1% |
| `feat:power-supply` | 725 | 193 | 532 | 73.4% |
| `proto:rstp` | 592 | 277 | 315 | 53.2% |
| `proto:ipv6` | 572 | 326 | 246 | 43.0% |
| `concept:ospf-area` | 494 | 264 | 230 | 46.6% |
| `proto:tcp` | 488 | 175 | 313 | 64.1% |
| `proto:snmp` | 479 | 313 | 166 | 34.7% |
| `proto:eigrp` | 420 | 201 | 219 | 52.1% |
| `proto:udp` | 372 | 98 | 274 | 73.7% |
| `feat:firmware-upgrade` | 369 | 154 | 215 | 58.3% |
| `proto:mstp` | 338 | 207 | 131 | 38.8% |
| `proto:icmp` | 333 | 111 | 222 | 66.7% |
| `proto:ipv4` | 310 | 157 | 153 | 49.4% |
| `proto:qos` | 300 | 94 | 206 | 68.7% |
| `concept:ospf-lsa` | 285 | 120 | 165 | 57.9% |
| `proto:syslog` | 246 | 104 | 142 | 57.7% |
| `proto:isis` | 220 | 126 | 94 | 42.7% |
| `concept:vlan-trunk` | 160 | 98 | 62 | 38.8% |
| `concept:bgp-as-path` | 155 | 73 | 82 | 52.9% |
| `feat:clock-config` | 145 | 78 | 67 | 46.2% |
| `proto:ntp` | 139 | 81 | 58 | 41.7% |
| `feat:dot1q-tunnel` | 134 | 98 | 36 | 26.9% |
| `feat:mac-address-table` | 133 | 81 | 52 | 39.1% |
| `proto:lacp` | 132 | 68 | 64 | 48.5% |
| `feat:console-access` | 132 | 77 | 55 | 41.7% |
| `proto:ssh` | 130 | 53 | 77 | 59.2% |
| `concept:mac-learning` | 128 | 78 | 50 | 39.1% |
| `proto:mpls` | 122 | 68 | 54 | 44.3% |
| `proto:radius` | 122 | 64 | 58 | 47.5% |
| `proto:vrrp` | 118 | 89 | 29 | 24.6% |
| `feat:port-security` | 105 | 58 | 47 | 44.8% |
| `concept:ospf-neighbor` | 101 | 46 | 55 | 54.5% |
| `proto:dhcpv6` | 95 | 56 | 39 | 41.1% |
| `proto:ospfv3` | 86 | 34 | 52 | 60.5% |
| `proto:ppp` | 78 | 7 | 71 | 91.0% |
| `proto:tls` | 59 | 10 | 49 | 83.1% |
| `feat:storm-control` | 57 | 31 | 26 | 45.6% |
| `proto:ndp` | 55 | 30 | 25 | 45.5% |
| `proto:mld` | 40 | 18 | 22 | 55.0% |
| `proto:gpon` | 40 | 25 | 15 | 37.5% |
| `proto:ripng` | 37 | 23 | 14 | 37.8% |
| `proto:pppoe` | 36 | 13 | 23 | 63.9% |
| `proto:lldp` | 35 | 15 | 20 | 57.1% |
| `concept:stp-root-bridge` | 28 | 14 | 14 | 50.0% |
| `proto:icmpv6` | 11 | 0 | 11 | 100.0% |
| `proto:nat64` | 4 | 1 | 3 | 75.0% |

## reject reason 샘플 (상위 10)

(none collected — use --keep-reasons)

## validated 예시 (앞 10)

- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:ripng']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:eigrp']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:mpls']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:ripng']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:tls']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:eigrp', 'proto:ripng']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:eigrp']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:eigrp', 'proto:isis', 'proto:ospf']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:ripng']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:ripng']

## rejected 예시 (앞 10)

- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:rip']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:nat', 'proto:rip']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:bgp', 'proto:nat', 'proto:rip']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:nat']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:nat']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:nat']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:nat']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:nat', 'proto:rip']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:nat', 'proto:rip', 'proto:udp']
- `/home/ymlee/work/markdown_rag/input_optimized/Cisco_CCIE/CCIE_Vol1/05_part-iii-ip-igp-rout` → ['proto:rip']
