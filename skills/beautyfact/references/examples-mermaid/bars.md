# Pattern: overview with ▓ bars: decision map, threat table

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

## 3. 🗺️ Decision map

🔗 Source: [Summary L151–L158](design.md#L151)

Five groups of decisions (D9–D23) plus six security threats (S1–S6).

| Group | Count | Entries |
| --- | --- | --- |
| Foundations | ▓▓▓▓ | D9 D10 D11 D21 |
| State and writes | ▓▓▓▓ | D12 D13 D14 D15 |
| Probes and sync | ▓▓▓ | D16 D17 D22 |
| Panel | ▓▓ | D18 D19 |
| Distribution, adapters | ▓▓ | D20 D23 |
| Security | ▓▓▓▓▓▓ | S1 S2 S3 S4 S5 S6 |

## 9. 🔒 Security

🔗 Source: [design.md L115–L136](design.md#L115)

| Threat | Scenarios | Addressed by |
| --- | --- | --- |
| S1 probe runs by itself | ▓▓▓▓ 4 | D16 D17 D22 |
| S2 path escape | ▓▓ 2 | D13 D22 real-path checks |
| S3 markup in names | ▓▓ 2 | D18 CSP nonce `textContent` |
| S4 malformed or huge files | ▓▓▓▓ 4 | D11 limits and shape checks |
| S5 hostile hook text | ▓ 1 | D23 |
| S6 fake or lost state | ▓▓▓ 3 | D14 D15 D21 |

- 📌 Inputs: `progress.json`, `progress.config.json`, CLI arguments, webview messages, harness event payloads. Secrets: none stored.
