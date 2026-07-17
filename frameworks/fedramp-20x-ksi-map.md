# FedRAMP 20x Key Security Indicator map

Every KSI in the current official set (FedRAMP 20x Key Security Indicators (CR26 2026-06-24), 46 indicators), mapped to the Living Control Set. The CR26 release is the authority in force since 24 June 2026 and supersedes the older 20x phase counts quoted in vendor material; each mapping is computed first from the SP 800-53 references CR26 itself publishes per KSI, then curated, and the basis column says which.

**Coverage: 39 covered, 7 partial, 0 unaddressed.** Partial never hides: each names its modernization delta in the note, because those deltas are the actual work of a 20x-shaped program. Coverage describes the engine's control set, never any company's implementation state.

**Why this matters for this role:** FedRAMP's stated direction is continuous, machine-validated evidence over point-in-time narrative, which is the thesis the engine is built on. Mattermost reaches federal buyers today through a partner's package; if the strategy question ever resolves toward its own listing, this map is the gap analysis, pre-built.

## Cybersecurity Education

| KSI | Indicator | Coverage | Living Control Set | Basis | Delta / note |
|---|---|---|---|---|---|
| KSI-CED-RAT | Reviewing All Training | ✅ covered | SAT-02, HRS-01 | computed |  |

## Change Management

| KSI | Indicator | Coverage | Living Control Set | Basis | Delta / note |
|---|---|---|---|---|---|
| KSI-CMT-LMC | Logging Changes | ✅ covered | CHG-02, MON-01 | computed |  |
| KSI-CMT-RMV | Redeploying vs Modifying | ✅ covered | CHG-02-BASELINE, CHG-02 | computed | the engine's GitHub-native operating model is exactly this: version-controlled redeploy over direct modification |
| KSI-CMT-RVP | Reviewing Change Procedures | ✅ covered | CHG-02 | computed |  |
| KSI-CMT-VTD | Validating Throughout Deployment | ✅ covered | CHG-02, VPM-01, SDLC-01 | mixed |  |

## Cloud Native Architecture

| KSI | Indicator | Coverage | Living Control Set | Basis | Delta / note |
|---|---|---|---|---|---|
| KSI-CNA-DFP | Defining Functionality and Privileges | ✅ covered | CHG-02-BASELINE, IAM-03 | mixed |  |
| KSI-CNA-EIS | Enforcing Intended State | ✅ covered | MON-01, CHG-02-BASELINE, GOV-04 | mixed | the drift-opens-a-ticket loop is this KSI's exact mechanism |
| KSI-CNA-IBP | Implementing Best Practices | ✅ covered | CHG-02-BASELINE, NET-02 | computed |  |
| KSI-CNA-MAT | Minimizing Attack Surface | ✅ covered | NET-01, CRY-01 | computed |  |
| KSI-CNA-OFA | Optimizing for Availability | ◐ partial | BCD-01, NET-01 | judgment | delta: the control set is confidentiality-weighted; availability engineering (autoscaling, load-shedding review) is a named extension |
| KSI-CNA-RNT | Restricting Network Traffic | ✅ covered | NET-01 | computed |  |
| KSI-CNA-RVP | Reviewing Protections | ◐ partial | NET-01, MON-01 | judgment | delta: DoS-protection effectiveness review (SC-5) has no dedicated engine control; boundary + monitoring carry it today |
| KSI-CNA-ULN | Using Logical Networking | ✅ covered | NET-01 | computed |  |

## Identity and Access Management

| KSI | Indicator | Coverage | Living Control Set | Basis | Delta / note |
|---|---|---|---|---|---|
| KSI-IAM-AAM | Automating Account Management | ✅ covered | IAM-01, IAC-17, IAM-05 | computed |  |
| KSI-IAM-APM | Adopting Passwordless Methods | ◐ partial | IAM-04 | computed | delta: MFA and phishing-resistant factors are in; a passwordless-first posture is the modernization step |
| KSI-IAM-ELP | Ensuring Least Privilege | ✅ covered | IAM-03 | computed |  |
| KSI-IAM-JIT | Authorizing Just-in-Time | ◐ partial | IAM-03 | judgment | delta: least privilege and PAM exist; a just-in-time, attribute-based authorization model is the named build (CR26 publishes no 800-53 refs for this KSI - it is genuinely new) |
| KSI-IAM-SNU | Securing Non-User Authentication | ✅ covered | IAM-05, SDLC-03 | computed | the engine carries a dedicated non-human-identity control; most programs bolt this on later |
| KSI-IAM-SUS | Responding to Suspicious Activity | ✅ covered | IAC-17, MON-01, IAM-01 | mixed |  |

## Incident Response

| KSI | Indicator | Coverage | Living Control Set | Basis | Delta / note |
|---|---|---|---|---|---|
| KSI-INR-AAR | Generating After Action Reports | ✅ covered | IRO-01 | computed |  |
| KSI-INR-RIR | Reviewing Incident Response Procedures | ✅ covered | IRO-01, IRO-02 | computed |  |
| KSI-INR-RPI | Reviewing Past Incidents | ✅ covered | IRO-01, RSK-02 | mixed |  |

## Monitoring, Logging, and Auditing

| KSI | Indicator | Coverage | Living Control Set | Basis | Delta / note |
|---|---|---|---|---|---|
| KSI-MLA-ALA | Authorizing Log Access | ✅ covered | MON-02, IAM-03 | judgment | CR26 anchors this to SI-11; the engine carries the same function through AU-9 (protect audit information, privileged-subset management) |
| KSI-MLA-EVC | Evaluating Configurations | ✅ covered | CHG-02-BASELINE, GOV-04 | computed |  |
| KSI-MLA-LET | Logging Event Types | ✅ covered | MON-01 | computed |  |
| KSI-MLA-OSM | Operating SIEM Capability | ✅ covered | MON-01, MON-02 | computed |  |
| KSI-MLA-RVL | Reviewing Logs | ✅ covered | MON-01 | computed |  |

## Policy and Inventory

| KSI | Indicator | Coverage | Living Control Set | Basis | Delta / note |
|---|---|---|---|---|---|
| KSI-PIY-GIV | Generating Inventories | ✅ covered | AST-01 | computed |  |
| KSI-PIY-RES | Reviewing Executive Support | ✅ covered | GOV-01, GOV-04 | judgment |  |
| KSI-PIY-RIS | Reviewing Investments in Security | ✅ covered | GOV-01, GOV-04, RSK-01 | judgment |  |
| KSI-PIY-RSD | Reviewing Security in the SDLC | ✅ covered | SDLC-01 | computed |  |
| KSI-PIY-RVD | Reviewing Vulnerability Disclosures | ✅ covered | VPM-01 | computed | Mattermost's published Product Vulnerability Process is a working example of this KSI; the engine adopts it as the model |

## Recovery Planning

| KSI | Indicator | Coverage | Living Control Set | Basis | Delta / note |
|---|---|---|---|---|---|
| KSI-RPL-ABO | Aligning Backups with Objectives | ✅ covered | BCD-02 | computed |  |
| KSI-RPL-ARP | Aligning Recovery Plan | ✅ covered | BCD-01, BCD-02 | computed |  |
| KSI-RPL-RRO | Reviewing Recovery Objectives | ✅ covered | BCD-01 | computed |  |
| KSI-RPL-TRC | Testing Recovery Capabilities | ✅ covered | BCD-01, BCD-02 | computed |  |

## Supply Chain Risk

| KSI | Indicator | Coverage | Living Control Set | Basis | Delta / note |
|---|---|---|---|---|---|
| KSI-SCR-MIT | Mitigating Supply Chain Risk | ✅ covered | TPM-01, TPM-02, SDLC-02 | mixed |  |
| KSI-SCR-MON | Monitoring Supply Chain Risk | ✅ covered | TPM-01, TPM-02, VPM-01 | computed |  |

## Service Configuration

| KSI | Indicator | Coverage | Living Control Set | Basis | Delta / note |
|---|---|---|---|---|---|
| KSI-SVC-ACM | Automating Configuration Management | ✅ covered | CHG-02-BASELINE, END-02 | computed |  |
| KSI-SVC-ASM | Automating Secret Management | ✅ covered | SDLC-03, CRY-02 | computed | dedicated secrets-management control already in the set |
| KSI-SVC-EIS | Evaluating and Improving Security | ✅ covered | VPM-01, VPM-02, MON-01 | computed |  |
| KSI-SVC-PRR | Preventing Residual Risk | ◐ partial | CHG-02, AST-03 | judgment | delta: post-change residual-element review (SC-4 flavor) is carried indirectly by change review and disposal; a persistent automated sweep is the named build. Optional at Class B |
| KSI-SVC-RUD | Removing Unwanted Data | ✅ covered | DCH-02 | computed |  |
| KSI-SVC-SIN | Securing Information | ✅ covered | CRY-01, DCH-01 | computed |  |
| KSI-SVC-VCM | Validating Communications | ◐ partial | CRY-01 | judgment | delta: session authenticity is protected (SC-23 family); persistent AUTOMATED validation of inter-resource communications integrity is the modernization step. Optional at Class B |
| KSI-SVC-VRI | Validating Resource Integrity | ◐ partial | SDLC-02, CRY-01, CHG-02-BASELINE | mixed | delta: dependency and artifact integrity are in; persistent runtime integrity validation of deployed resources is the named extension |

---

*Generated by `06-evidence-and-audit/data/render.py` from `fedramp-20x-ksi-mapping.yaml`. Edit the data, never this file.*
