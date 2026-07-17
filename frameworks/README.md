# frameworks

The human-readable framework renderings. Each document here is a view of the same underlying control set, rendered into the language one framework's audience needs. The machine-readable mappings and the tools that check these against live upstream sources sit in [`06-evidence-and-audit/data/`](../06-evidence-and-audit/data/).

| Document | Rendering |
|---|---|
| [`nist-800-171-rev2-workbook.md`](nist-800-171-rev2-workbook.md) | All 110 NIST 800-171 Rev 2 requirements with their SPRS weights, the scoring arithmetic, and where each requirement lands in the control set |
| [`fedramp-20x-ksi-map.md`](fedramp-20x-ksi-map.md) | The 46 FedRAMP 20x Key Security Indicators mapped to the control set, reconciled against FedRAMP's live ruleset by the [drift check](../06-evidence-and-audit/upstream-conformance-receipt.md) |
| [`brilliant-basics-map.md`](brilliant-basics-map.md) | The DoW CIO's [Top 10 IT practices](https://dowcio.war.gov/BrilliantBasics/) mapped through 800-171 Rev 2, including the one practice the enforced baseline cannot see |

No rendering ranks above another. Framework choice is a rendering of one control set, never a bet on one framework.
