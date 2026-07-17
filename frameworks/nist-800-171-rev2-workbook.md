# NIST SP 800-171 Rev 2 self-assessment workbook

All 110 security requirements, ready to walk on day one. Each row carries its SPRS weight from the DoD Assessment Methodology v1.2.1, the Living Control Set control(s) that address it, and the 800-53 anchor that makes the mapping traceable rather than asserted. The evidence line above each family names where evidence computes from in Mattermost's publicly documented stack.

**What this is not:** an assessment result. No requirement is marked met or unmet here, and no SPRS score is claimed, because implementation state is only knowable inside the boundary, from systems of record. The status column ships empty on purpose; filling it during days 30 to 60 is the work, and this workbook is the instrument.

**Regime note:** under the 2026-07-13 CMMC Phase II suspension the enforced baseline is exactly this document's frame: NIST SP 800-171 Rev 2 by self-assessment, posted to SPRS, with DFARS 252.204-7012 fully in force. A posted score is a signed federal claim, which is why every row below insists on re-derivable evidence.

**Scoring mechanics:** start at 110, subtract each unimplemented requirement's weight. 44 requirements weigh 5 points, 14 weigh 3, 51 weigh 1; two carry partial credit (3.5.3 MFA and 3.13.11 FIPS cryptography); 3.12.4 (the SSP) is unscored because without an SSP the assessment cannot be conducted at all. Floor is -203; a perfect score is 110.

## 3.1 Access Control

**Evidence computes from:** IdP (confirmed in discovery) and AWS IAM for account state; Drata access-review records; VPN/ZTNA configuration for remote access

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.1.1 | Limit system access to authorized users, processes, and devices | 5 | IAM-01, IAC-17 | ☐ assess | anchor: AC-2 |
| 3.1.2 | Limit system access to authorized transaction and function types | 5 | IAM-03 | ☐ assess | anchor: AC-6 (least-privilege implementation of AC-3). judgment-adjacent: 800-171 derives this from AC-2/AC-3; the engine enforces it through least privilege |
| 3.1.3 | Control the flow of CUI per approved authorizations | 1 | DCH-01, NET-01 | ☐ assess | anchor: AC-4 |
| 3.1.4 | Separate duties of individuals to reduce malevolent-activity risk | 1 | GOV-03 | ☐ assess | anchor: AC-5 |
| 3.1.5 | Employ least privilege, including for privileged accounts | 3 | IAM-03 | ☐ assess | anchor: AC-6 |
| 3.1.6 | Use non-privileged accounts for non-security functions | 1 | IAM-03 | ☐ assess | anchor: AC-6(2) |
| 3.1.7 | Prevent non-privileged execution of privileged functions; audit such attempts | 1 | IAM-03, MON-01 | ☐ assess | anchor: AC-6(9)/(10); AU-2 |
| 3.1.8 | Limit unsuccessful logon attempts | 1 | IAM-04 | ☐ assess | anchor: AC-7 |
| 3.1.9 | Provide privacy and security notices for CUI systems | 1 | IAM-04 | ☐ assess | anchor: AC-8. judgment: system-use banners ride the authentication surface |
| 3.1.10 | Use session lock with pattern-hiding displays | 1 | END-02 | ☐ assess | anchor: AC-11 |
| 3.1.11 | Terminate user sessions automatically after a defined condition | 1 | IAM-04 | ☐ assess | anchor: AC-12 |
| 3.1.12 | Monitor and control remote access sessions | 5 | NET-02 | ☐ assess | anchor: AC-17 |
| 3.1.13 | Employ cryptographic mechanisms for remote access confidentiality | 5 | NET-02, CRY-01 | ☐ assess | anchor: AC-17(2); SC-8 |
| 3.1.14 | Route remote access via managed access control points | 1 | NET-02 | ☐ assess | anchor: AC-17(3) |
| 3.1.15 | Authorize remote execution of privileged commands | 1 | NET-02, IAM-03 | ☐ assess | anchor: AC-17(4); AC-6 |
| 3.1.16 | Authorize wireless access before enabling connections | 5 | NET-01 | ☐ assess | anchor: AC-18. corporate-office scope; production is cloud |
| 3.1.17 | Protect wireless access using authentication and encryption | 5 | NET-01, CRY-01 | ☐ assess | anchor: AC-18(1); SC-13 |
| 3.1.18 | Control connection of mobile devices | 5 | END-02 | ☐ assess | anchor: AC-19 |
| 3.1.19 | Encrypt CUI on mobile devices and platforms | 3 | END-02, CRY-01 | ☐ assess | anchor: AC-19(5); SC-28 |
| 3.1.20 | Verify and control connections to external systems | 1 | TPM-01, TPM-02 | ☐ assess | anchor: AC-20 via SA-9 |
| 3.1.21 | Limit use of portable storage devices on external systems | 1 | END-02, DCH-01 | ☐ assess | anchor: AC-20(2) |
| 3.1.22 | Control CUI posted or processed on publicly accessible systems | 1 | DCH-01 | ☐ assess | anchor: AC-22 |

## 3.2 Awareness and Training

**Evidence computes from:** Drata training assignment and completion records; role-based curricula for engineering and incident-response staff

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.2.1 | Ensure personnel are aware of security risks and applicable policies | 5 | SAT-02 | ☐ assess | anchor: AT-2 |
| 3.2.2 | Train personnel to carry out assigned security duties | 5 | SAT-02 | ☐ assess | anchor: AT-3 |
| 3.2.3 | Provide insider-threat awareness training | 1 | SAT-02 | ☐ assess | anchor: AT-2(2) |

## 3.3 Audit and Accountability

**Evidence computes from:** AWS CloudTrail and centralized log platform; Drata monitor results; alert routing lands in Mattermost channels natively

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.3.1 | Create and retain audit logs to enable monitoring and investigation | 5 | MON-01 | ☐ assess | anchor: AU-2 |
| 3.3.2 | Ensure actions of individual users are uniquely traceable | 3 | MON-01, IAM-01 | ☐ assess | anchor: AU-2; AC-2 |
| 3.3.3 | Review and update logged events | 1 | MON-01 | ☐ assess | anchor: AU-2(3) |
| 3.3.4 | Alert on audit logging process failure | 1 | MON-01 | ☐ assess | anchor: AU-5 |
| 3.3.5 | Correlate audit review and reporting for indications of attack | 5 | MON-01 | ☐ assess | anchor: AU-6(3) |
| 3.3.6 | Provide audit record reduction and report generation | 1 | MON-01 | ☐ assess | anchor: AU-7 |
| 3.3.7 | Synchronize system clocks to an authoritative time source | 1 | MON-02 | ☐ assess | anchor: AU-8 |
| 3.3.8 | Protect audit information and tools from unauthorized access or deletion | 1 | MON-02 | ☐ assess | anchor: AU-9 |
| 3.3.9 | Limit audit logging management to a privileged subset of users | 1 | MON-02, IAM-03 | ☐ assess | anchor: AU-9(4); AC-6 |

## 3.4 Configuration Management

**Evidence computes from:** GitHub as the change record (the product monorepo runs 86 CI workflows; the merge record is the approval evidence); IaC baselines; MDM for endpoint configuration

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.4.1 | Establish and maintain baseline configurations and system inventories | 5 | CHG-02-BASELINE, AST-01 | ☐ assess | anchor: CM-2; CM-8 |
| 3.4.2 | Establish and enforce security configuration settings | 5 | CHG-02-BASELINE | ☐ assess | anchor: CM-6 |
| 3.4.3 | Track, review, approve, and log system changes | 1 | CHG-02 | ☐ assess | anchor: CM-3 |
| 3.4.4 | Analyze the security impact of changes before implementation | 1 | CHG-02 | ☐ assess | anchor: CM-4 |
| 3.4.5 | Define and enforce access restrictions for change | 5 | CHG-02 | ☐ assess | anchor: CM-5 |
| 3.4.6 | Employ least functionality; essential capabilities only | 5 | CHG-02-BASELINE | ☐ assess | anchor: CM-7 via CM-6 |
| 3.4.7 | Restrict nonessential programs, functions, ports, protocols, and services | 5 | CHG-02-BASELINE, NET-01 | ☐ assess | anchor: CM-7(1); SC-7 |
| 3.4.8 | Apply deny-by-exception policy for unauthorized software | 5 | END-02 | ☐ assess | anchor: CM-7(4)/(5) via CM-6 |
| 3.4.9 | Control and monitor user-installed software | 1 | END-02 | ☐ assess | anchor: CM-11 via CM-6 |

## 3.5 Identification and Authentication

**Evidence computes from:** IdP configuration exports (MFA policy, password policy, session settings); service-account inventory; Drata identity monitors

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.5.1 | Identify system users, processes, and devices | 5 | IAM-01, IAM-05 | ☐ assess | anchor: IA-2 via AC-2; IA-5(5) |
| 3.5.2 | Authenticate identities as a prerequisite to access | 5 | IAM-04 | ☐ assess | anchor: IA-2 |
| 3.5.3 | Use MFA for privileged accounts and network access to non-privileged accounts | 5 | IAM-04 | ☐ assess | anchor: IA-2(1)/(2). partial credit: 3 of 5 points if general users lack MFA |
| 3.5.4 | Employ replay-resistant authentication | 1 | IAM-04 | ☐ assess | anchor: IA-2(8) |
| 3.5.5 | Prevent reuse of identifiers for a defined period | 1 | IAM-01 | ☐ assess | anchor: IA-4 via AC-2 |
| 3.5.6 | Disable identifiers after a defined period of inactivity | 1 | IAM-01, IAC-17 | ☐ assess | anchor: IA-4 / AC-2(3) |
| 3.5.7 | Enforce minimum password complexity and change of characters | 1 | IAM-04 | ☐ assess | anchor: IA-5(1) |
| 3.5.8 | Prohibit password reuse for a specified number of generations | 1 | IAM-04 | ☐ assess | anchor: IA-5(1) |
| 3.5.9 | Allow temporary passwords only with immediate change to permanent | 1 | IAM-04 | ☐ assess | anchor: IA-5(1) |
| 3.5.10 | Store and transmit only cryptographically protected passwords | 5 | IAM-04, CRY-01 | ☐ assess | anchor: IA-5(1); SC-13 |
| 3.5.11 | Obscure feedback of authentication information | 1 | IAM-04 | ☐ assess | anchor: IA-6 |

## 3.6 Incident Response

**Evidence computes from:** Jira incident tickets and postmortems; IR plan and tabletop records; DIBNet reporting procedure (72-hour clock under DFARS 252.204-7012)

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.6.1 | Establish operational incident-handling capability | 5 | IRO-01 | ☐ assess | anchor: IR-4; IR-8 |
| 3.6.2 | Track, document, and report incidents to officials and authorities | 5 | IRO-01, IRO-02 | ☐ assess | anchor: IR-6. for a DIB contractor this includes the DFARS 7012 72-hour DIBNet report |
| 3.6.3 | Test the incident response capability | 1 | IRO-01 | ☐ assess | anchor: IR-3 via IR-8 |

## 3.7 Maintenance

**Evidence computes from:** MDM maintenance and patch records for corporate endpoints; AWS shared-responsibility documentation for production infrastructure

> Honest engine gap: no dedicated maintenance family exists in the Living Control Set; rows below are nearest-fit. For a cloud-native boundary most physical-system maintenance inherits from the CSP, and the day-one boundary decision determines how much of 3.7 stays in scope. A dedicated MA-01 owned control is the identified engine extension.

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.7.1 | Perform maintenance on organizational systems | 3 | END-02, VPM-01 | ☐ assess | anchor: nearest-fit via CM-6/SI-2. production hardware maintenance inherits from AWS |
| 3.7.2 | Control tools, techniques, and personnel used for maintenance | 5 | END-02 | ☐ assess | anchor: nearest-fit via CM-6. production hardware maintenance inherits from AWS |
| 3.7.3 | Sanitize equipment of CUI before off-site maintenance | 1 | AST-03 | ☐ assess | anchor: MP-6 |
| 3.7.4 | Check diagnostic media for malicious code before use | 3 | END-01 | ☐ assess | anchor: SI-3 |
| 3.7.5 | Require MFA for nonlocal maintenance sessions | 5 | IAM-04, NET-02 | ☐ assess | anchor: IA-2(1); AC-17 |
| 3.7.6 | Supervise maintenance activities of personnel without required access | 1 | HRS-01, PES-01 | ☐ assess | anchor: PS-6; PE-2 |

## 3.8 Media Protection

**Evidence computes from:** MDM removable-media policy enforcement; sanitization certificates; AWS inherits physical media handling for production; backup encryption configuration

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.8.1 | Protect system media containing CUI, paper and digital | 3 | DCH-01, AST-03 | ☐ assess | anchor: MP-6; AC-4. cloud-hosted CUI: physical media largely inherited from AWS |
| 3.8.2 | Limit access to CUI on system media to authorized users | 3 | DCH-01 | ☐ assess | anchor: nearest-fit via AC-4. inherited for production media |
| 3.8.3 | Sanitize or destroy media containing CUI before disposal or reuse | 5 | AST-03 | ☐ assess | anchor: MP-6 |
| 3.8.4 | Mark media with CUI markings and distribution limitations | 1 | AST-02 | ☐ assess | anchor: MP-3 |
| 3.8.5 | Control access to and accountability for media during transport | 1 | DCH-01 | ☐ assess | anchor: nearest-fit. inherited for production; corporate scope is device transport under MDM |
| 3.8.6 | Use cryptography to protect CUI on media during transport | 1 | CRY-01 | ☐ assess | anchor: SC-28 |
| 3.8.7 | Control the use of removable media on system components | 5 | END-02 | ☐ assess | anchor: nearest-fit via CM-6 endpoint policy |
| 3.8.8 | Prohibit portable storage devices with no identifiable owner | 3 | END-02 | ☐ assess | anchor: nearest-fit via CM-6 endpoint policy |
| 3.8.9 | Protect the confidentiality of backup CUI at storage locations | 1 | BCD-02, CRY-01 | ☐ assess | anchor: CP-9; SC-28 |

## 3.9 Personnel Security

**Evidence computes from:** HRIS screening records joined to IdP deprovisioning timestamps (the joiner-mover-leaver record); signed agreements in Drata

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.9.1 | Screen individuals prior to authorizing access to CUI systems | 3 | HRS-01 | ☐ assess | anchor: PS-3 |
| 3.9.2 | Protect CUI systems during and after personnel actions | 5 | HRS-01, IAM-01 | ☐ assess | anchor: PS-4; PS-5 |

## 3.10 Physical Protection

**Evidence computes from:** Office badge and visitor records; AWS SOC 2 / FedRAMP packages inherit production data-center physical security; remote-work standard under MDM

> Production physical protection inherits from AWS. Corporate offices and the remote-first workforce (3.10.6) remain squarely in scope and are where the assessment work actually lands.

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.10.1 | Limit physical access to systems and environments to authorized individuals | 5 | PES-01 | ☐ assess | anchor: PE-2 |
| 3.10.2 | Protect and monitor the physical facility and support infrastructure | 5 | PES-01 | ☐ assess | anchor: PE-3; PE-6 |
| 3.10.3 | Escort visitors and monitor visitor activity | 1 | PES-01 | ☐ assess | anchor: PE-3 |
| 3.10.4 | Maintain audit logs of physical access | 1 | PES-01 | ☐ assess | anchor: PE-6 (access logs) |
| 3.10.5 | Control and manage physical access devices | 1 | PES-01 | ☐ assess | anchor: PE-3 |
| 3.10.6 | Enforce safeguarding measures for CUI at alternate work sites | 1 | PES-01, END-02 | ☐ assess | anchor: PE-17 nearest-fit; CM-6. remote-first workforce makes this a primary, not peripheral, requirement |

## 3.11 Risk Assessment

**Evidence computes from:** Risk register with FAIR quantification; vulnerability scanner output (Dependabot, dependency and container scanning already visible in their public CI)

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.11.1 | Periodically assess risk to operations, assets, and individuals | 3 | RSK-01 | ☐ assess | anchor: RA-3 |
| 3.11.2 | Scan for vulnerabilities periodically and when new ones are identified | 5 | VPM-01, VPM-02 | ☐ assess | anchor: RA-5 |
| 3.11.3 | Remediate vulnerabilities in accordance with risk assessments | 1 | VPM-01 | ☐ assess | anchor: SI-2 via RA-5 |

## 3.12 Security Assessment

**Evidence computes from:** Assessment workpapers; POA&M as the risk-treatment register; continuous-monitoring dashboards; the SSP itself

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.12.1 | Periodically assess security controls for effectiveness | 5 | GOV-04, VPM-02 | ☐ assess | anchor: CA-7 (GOV-04); CA-8 (VPM-02) |
| 3.12.2 | Develop and implement POA&Ms to correct deficiencies | 3 | RSK-02 | ☐ assess | anchor: CA-5 |
| 3.12.3 | Monitor security controls on an ongoing basis | 5 | MON-01, GOV-04 | ☐ assess | anchor: CA-7 |
| 3.12.4 | Develop, document, and periodically update system security plans | n/a | GOV-01, GOV-02 | ☐ assess | anchor: PL-2 via PM-1/PL-1. unscored in SPRS because an absent SSP means the assessment cannot be conducted; this is the precondition artifact |

## 3.13 System and Communications Protection

**Evidence computes from:** AWS network configuration (security groups, VPC boundaries) as computed evidence; TLS and KMS configuration; the product itself ships FIPS-validated cryptography and STIG-hardened images (v11)

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.13.1 | Monitor, control, and protect communications at system boundaries | 5 | NET-01 | ☐ assess | anchor: SC-7 |
| 3.13.2 | Employ architectural designs and engineering principles that promote security | 5 | SDLC-01 | ☐ assess | anchor: SA-8 |
| 3.13.3 | Separate user functionality from system management functionality | 1 | NET-01, IAM-03 | ☐ assess | anchor: SC-2 nearest; AC-6 |
| 3.13.4 | Prevent unauthorized information transfer via shared system resources | 1 | NET-01 | ☐ assess | anchor: SC-4 nearest. hypervisor-level isolation inherits from AWS |
| 3.13.5 | Implement subnetworks for publicly accessible components | 5 | NET-01 | ☐ assess | anchor: SC-7 |
| 3.13.6 | Deny network traffic by default; allow by exception | 5 | NET-01 | ☐ assess | anchor: SC-7(5) |
| 3.13.7 | Prevent split tunneling for remote devices | 1 | NET-02 | ☐ assess | anchor: SC-7(7) via AC-17 |
| 3.13.8 | Use cryptography to prevent unauthorized disclosure of CUI in transit | 3 | CRY-01 | ☐ assess | anchor: SC-8 |
| 3.13.9 | Terminate network connections after sessions end or defined inactivity | 1 | NET-02 | ☐ assess | anchor: SC-10 via AC-17 |
| 3.13.10 | Establish and manage cryptographic keys | 1 | CRY-02 | ☐ assess | anchor: SC-12 |
| 3.13.11 | Employ FIPS-validated cryptography to protect CUI confidentiality | 5 | CRY-01 | ☐ assess | anchor: SC-13. partial credit: 3 of 5 points if cryptography is mostly not FIPS-validated. Mattermost ships a FIPS-mode product offering, which makes the corporate-boundary question precise rather than novel |
| 3.13.12 | Prohibit remote activation of collaborative computing devices | 1 | END-02 | ☐ assess | anchor: SC-15 nearest-fit. product-relevant for a collaboration platform; corporate scope is endpoint camera/mic policy |
| 3.13.13 | Control and monitor the use of mobile code | 1 | END-01 | ☐ assess | anchor: SC-18 via SI-3 |
| 3.13.14 | Control and monitor the use of VoIP technologies | 1 | NET-01 | ☐ assess | anchor: SC-19 nearest-fit. product-relevant: Mattermost Calls is VoIP; corporate boundary treats it as a governed communication service |
| 3.13.15 | Protect the authenticity of communications sessions | 5 | CRY-01 | ☐ assess | anchor: SC-23 via SC-8 |
| 3.13.16 | Protect the confidentiality of CUI at rest | 1 | CRY-01, DCH-01 | ☐ assess | anchor: SC-28 |

## 3.14 System and Information Integrity

**Evidence computes from:** EDR deployment records; advisory-monitoring runbook (their own published Product Vulnerability Process is the model); SIEM detections routed to Mattermost channels

| Req | Requirement | SPRS | Living Control Set | Status | Notes |
|---|---|---|---|---|---|
| 3.14.1 | Identify, report, and correct system flaws in a timely manner | 5 | VPM-01 | ☐ assess | anchor: SI-2 |
| 3.14.2 | Provide protection from malicious code at designated locations | 5 | END-01 | ☐ assess | anchor: SI-3 |
| 3.14.3 | Monitor security alerts and advisories; take action in response | 5 | VPM-01, MON-01 | ☐ assess | anchor: SI-5 via SI-2/AU-6 |
| 3.14.4 | Update malicious code protection mechanisms when new releases are available | 5 | END-01 | ☐ assess | anchor: SI-3 |
| 3.14.5 | Perform periodic and real-time scans of systems and files | 3 | END-01, VPM-01 | ☐ assess | anchor: SI-3; RA-5 |
| 3.14.6 | Monitor communications traffic for attacks and indicators | 5 | MON-01, NET-01 | ☐ assess | anchor: SI-4; SC-7 |
| 3.14.7 | Identify unauthorized use of organizational systems | 3 | MON-01 | ☐ assess | anchor: SI-4 |

---

**Integrity check:** 44 five-point, 14 three-point, 51 one-point requirements plus the unscored SSP requirement (3.12.4) = 110 of 110. Weights parsed from the methodology PDF itself and verified to reproduce its published score range exactly.

*Generated by `06-evidence-and-audit/data/render.py` from `nist-800-171-rev2-mapping.yaml` + `sprs-weights.json`. Edit the data, never this file.*
