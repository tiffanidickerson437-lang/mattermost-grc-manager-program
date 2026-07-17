# Questionnaire answer-bank lint

Source: [https://handbook.mattermost.com/operations/operations/company-policies/security-policies.md](https://handbook.mattermost.com/operations/operations/company-policies/security-policies.md)  
Checked: 2026-07-17 15:04:00 UTC · 80 questions · 96% answered Yes

## 2 question(s) need a human

### POLARITY — Governance Q8  `NEG-PII-EXPOSURE`

> For all IT systems including but not limited to servers, routers, switches, firewalls, and databases, do privileged accounts (e.g., system or security administrator) that communicate directly with the internet, contain any personally identifiable information (PII) such as: social security numbers, credit card numbers, patient health record information, or other confidential records?

**Published answer:** `Yes`

Answering Yes asserts that sensitive data sits somewhere it should not.

### CONTRADICTION — Governance Q8  `XOR-PII-EXPOSED-VS-PII-PROTECTED`

> Q8: For all IT systems including but not limited to servers, routers, switches, firewalls, and databases, do privileged accounts (e.g., system or security administrator) that communicate directly with the internet, contain any personally identifiable information (PII) such as: social security numbers, credit card numbers, patient health record information, or other confidential records?

**Published answer:** `'Yes'`

One answer says sensitive data sits on internet-facing privileged accounts; the other says all such data is protected by industry-standard encryption. Both may be literally reconcilable, but a customer's security reviewer will not reconcile them — they will ask, and the deal slows while someone finds out which is true.

**Paired with:** Q9: Is all sensitive, protected health information (PHI) and personally identifiable information (PII) protected using an industry standard encryption algorithm where technically feasible? -> 'Yes'

**None of the above is a verdict.** Each is a question where the published answer would be read by a customer's security reviewer as a disclosure. The answer may be correct and deliberate — but if it is not, this is where a deal slows down and nobody traces it back to the file.

## Coverage

| | |
|---|---:|
| Questions parsed | 80 |
| Negative polarity (Yes = admission) | 1 |
| Positive polarity (Yes = good) | 18 |
| Polarity unknown — not classified, not cleared | 61 |
| Answered Yes | 77 |
| Answered No | 0 |
| Prose / other | 0 |

**61 questions could not be classified** and are reported here rather than counted as clean. A linter that treats *unclassified* as *fine* is the fail-open defect it exists to catch. Curating those into `polarity-rules.yaml` is the work; the rules file is committed so the person who owns the answers can argue with it.

<details><summary>Unclassified questions</summary>

- Governance Q5: For all IT systems including but not limited to servers, routers, switches, firewalls, databases, and external → `yes`
- Governance Q9: Is all sensitive, protected health information (PHI) and personally identifiable information (PII) protected u → `yes`
- Governance Q12: Is a background screening performed prior to allowing personnel access to Scoped Systems and Data? → `yes`
- Governance Q14: Is there a disciplinary process for non-compliance with information security policies? → `yes`
- Governance Q15: Is there a personnel termination or change of status process? → `yes`
- Access control Q2: Is access to and maintenance of applications, systems, network components (including routers, databases, firew → `yes`
- Access control Q5: Are there written network password policies and/or procedures? → `yes`
- Access control Q6: Is password administration employed for critical systems? → `yes`
- Access control Q7: Are passwords prevented from being displayed in clear text during user authentication or in electronic/printed → `yes`
- Access control Q8: If user accounts are assigned to non-permanent personnel (e.g., contractors, consultants) for troubleshooting  → `yes`
- Operational security Q1: Is there a risk assessment program that has been approved by management, communicated to appropriate personnel → `yes`
- Operational security Q2: Is there an information security policy that has been approved by management, communicated to appropriate pers → `yes`
- Operational security Q3: Is there a vendor management program? → `yes`
- Operational security Q4: Is there a respondent information security function responsible for security initiatives? → `yes`
- Operational security Q5: Is there an asset management policy or program that has been approved by management, communicated to appropria → `yes`
- Operational security Q7: Is there an operational change management/change control policy or program that has been approved by managemen → `yes`
- Operational security Q8: Are system backups performed? → `yes`
- Operational security Q9: Are firewalls in use for both internal and external connections? → `yes`
- Operational security Q10: Are firewalls or IPS(s) secured against unauthorized access from the internet, Extranet, and Intranet users? → `yes`
- Operational security Q11: Are vulnerability assessments, scans, or penetration tests performed on internal or external networks? → `yes`
- Operational security Q12: Are incoming emails scanned for questionable file attachments? → `yes`
- Operational security Q13: Does the company use spam filtering software to reduce the number of unsolicited emails? → `yes`
- Operational security Q14: Are email attachments scanned by anti-virus software? → `yes`
- Business resiliency Q1: Is there an established Business Resiliency program that has been approved by management and communicated to a → `yes`
- Business resiliency Q2: Has a Business Impact Analysis been conducted? → `yes`
- Business resiliency Q3: Is there a formal process focused on identifying and addressing risks of disruptive incidents to the organizat → `yes`
- Business resiliency Q4: Is there an established Business Resiliency program that has been approved by management and communicated to a → `yes`
- Business resiliency Q5: Are specific response and recovery strategies defined for addressing risks of disruptive incidents to the orga → `yes`
- Business resiliency Q7: Has senior management assigned the responsibility for the overall management of the response and recovery effo → `yes`
- Business resiliency Q8: Is there a periodic review of your Business Resiliency Program? → `yes`
- Business resiliency Q9: Is there an Influenza Pandemic/Infectious Disease Outbreak Plan? → `yes`
- Business resiliency Q10: Is there insurance coverage for business interruptions or general services interruption? → `yes`
- Compliance Q1: Is there an internal audit, risk management, or compliance department with responsibility for identifying and  → `yes`
- Compliance Q2: Are there policies and procedures to ensure compliance with applicable legislative, regulatory, and contractua → `yes`
- Compliance Q3: Is there a records retention policy covering paper and electronic records, including email in support of appli → `yes`
- Compliance Q4: Is licensing maintained in all jurisdictions where the business operates or where licensing is required? → `yes`
- Compliance Q5: Is there an internal compliance and ethics program to ensure professional ethics and business practices are im → `yes`
- Compliance Q6: Are policies and procedures maintained for enabling compliance with applicable legal, regulatory, statutory, o → `yes`
- Compliance Q7: Is there a formalized governance process to identify and assess changes that could significantly affect the sy → `yes`
- Software Development Life Cycle (SDLC) Q2: Do the materials above include references to application security best practices and principles being followed → `yes`

</details>

