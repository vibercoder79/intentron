# Integration Discovery Questionnaire

> Audience: the customer's IT department
> Language: English — for the German version see [`integration-discovery.md`](./integration-discovery.md)

## Purpose of this document

The INTENTRON framework together with Claude Code runs during development on a dedicated (VPS-based) dev setup. This development and build environment is standardized and fully covered by the framework itself — the customer's IT does not need to contribute anything here.

This questionnaire captures exclusively the **customer-specific part**: everything the customer's IT must answer **up front** so that the solution to be built can subsequently integrate into the customer's **live and existing environment**. In other words, this is about continuous integration and continuous deployment **into your systems** — not about the development itself.

The more complete and precise the following clusters are answered, the more smoothly the later integration will run. Unclear or open points are not a problem: they are flagged as assumptions and clarified together over the course of the project. Please answer the questions as concretely as possible; where standards or existing guidelines exist, feel free to reference them directly.

---

## 1. Target runtime / hosting of the solution

**Why we ask:** Where the solution ultimately runs determines almost every downstream decision — deployment mechanics, networking, secrets, compliance. We need to know early whether we are building against on-prem, a public cloud, or a hybrid model, and which platform and IaC standards are set on your side, so that we do not develop against your existing conventions.

- Should the solution run on-prem, in a public cloud, or hybrid?
- For cloud: which provider is mandated (AWS, Azure, GCP, Hetzner, other)?
- Which region or data location is required (e.g. EU, Switzerland, a specific data center)?
- Which container or runtime platform is standard (Kubernetes, Docker/Compose, plain VMs, serverless)?
- If Kubernetes: managed (EKS/AKS/GKE) or self-operated? Which clusters are available for which environments (dev/test/prod)?
- Which Infrastructure-as-Code standard applies (Terraform, Ansible, Helm, Pulumi, CloudFormation)? Are there existing modules/repos we should hook into?
- Are there requirements regarding operating system, base images, or hardened image sources?

---

## 2. The customer's existing CI/CD systems

**Why we ask:** The solution should slot into your existing build and deploy pipeline rather than spinning up a second, parallel world. We need to know which CI/CD system you use, how artifacts are managed, and what approval process precedes a deployment, so that our delivery follows your established path.

- Which CI/CD system is in use (Jenkins, GitLab CI, GitHub Actions, Azure DevOps, CircleCI, other)?
- Where do the source repositories live, and by what pattern are new repos created/managed?
- Which artifact or container registry is used (e.g. Artifactory, Nexus, GitLab Registry, ACR/ECR/GCR, Harbor)?
- Which branch and release strategy applies (trunk-based, GitFlow, release branches, tagging convention)?
- What does the approval and deploy process look like: automated, manual gates, four-eyes principle?
- Which environments exist (dev/integration/staging/prod), and how is promotion between them handled?
- Are there existing pipeline templates, quality gates, or mandatory checks (tests, linting, security scans) we must adopt?

---

## 3. Interfaces / target systems / data sources

**Why we ask:** The solution delivers its value through the connection to your existing systems. We need to know the concrete target systems, their interface types, and the authentication model in order to plan adapters, data flows, and migrations cleanly — and to recognize early where schema or protocol breakpoints lie.

- Which existing systems should be connected (ERP, CRM, databases, line-of-business applications, third-party services)? Please list each system with version if known.
- Which interface types are present (REST, SOAP, gRPC, event/streaming such as Kafka, message queues, file/batch transfer)?
- Is there an API gateway or integration layer (e.g. Kong, Apigee, Azure API Management, MuleSoft) we should/must route through?
- How does authentication against these systems work (SSO, OIDC, SAML, LDAP/AD, API keys, mTLS, technical service accounts)? Is there a central identity federation?
- Which data schemas/data models are relevant, and is there authoritative documentation for them?
- Are data migrations or initial data takeovers part of the scope? If so, to what extent and from which sources?
- Are there requirements regarding data formats, interface versioning, or backward compatibility?

---

## 4. Network / access

**Why we ask:** Even the best solution only works if it can reach the endpoints it needs and is reachable in return. Network clearances and access paths often have long lead times at customers — so we clarify them as early as possible, so they do not become a blocker at the first deployment.

- Which endpoints must the solution reach (internal systems, external services), and are these reachable from the target runtime?
- Is a VPN or a dedicated connection required, and who provides it?
- Which firewall clearances are required (sources, destinations, ports, protocols)? What is the request process and typical lead time?
- Is there IP whitelisting or allow-listing into which our components must be added?
- Does access go through a bastion / jump host? How is this access provided and logged?
- Which egress rules apply (outbound traffic, mandatory proxy, blocked destinations)?
- Is there network segmentation/zoning (DMZ, internal zones) that influences the solution design?

---

## 5. The customer's secrets management

**Why we ask:** The solution needs credentials, certificates, and keys to talk to your systems. These must never end up in code, pipelines, or configuration files. We need to know your secrets management in order to bring the solution's secrets into the target environment from the start, via the secure path you have designated.

- Which secrets management is in use (HashiCorp Vault, Azure Key Vault, AWS Secrets Manager, GCP Secret Manager, CyberArk, other)?
- How are secrets delivered to applications at runtime (injection, sidecar, mount, environment variables via the platform)?
- Who creates and rotates secrets — and how should the solution's secrets be requested/provided?
- Are there requirements regarding rotation, validity period, and encryption?
- How are TLS/client certificates managed and rolled out?
- How do secrets get into the CI/CD pipeline without appearing there in plaintext?
- Is there a defined process for handling compromised secrets?

---

## 6. The customer's compliance / audit requirements

**Why we ask:** Compliance requirements are not a downstream check but a design constraint. We need to know your industry- and company-specific obligations early so that architecture, data handling, and the delivery process are compliant from the start, and no late, costly rework becomes necessary.

- Which industry- or company-specific obligations apply (e.g. ISO 27001, SOC 2, BAIT/VAIT, KRITIS, HIPAA, PCI-DSS, regulatory requirements of your industry)?
- How is data classified (public, internal, confidential, strictly confidential), and which of the processed data falls into which class?
- Are penetration tests, code audits, or external sign-offs mandatory before go-live? By whom, with what lead time?
- What does the change-approval process look like (Change Advisory Board, mandatory tickets, approval instances)?
- Which audit/logging requirements exist (traceability, retention periods, tamper-proof logs)?
- Are there requirements regarding data residency, data processing agreements, or subprocessors?

> **Cross-reference:** If the solution includes an AI component, additional regulatory requirements apply — in particular the EU AI Act as well as data protection (GDPR/BDSG/nDSG). These are captured and assessed separately via the `dpo` skill (Data Protection Officer); please have any AI components and the personal data processed by them ready.

---

## 7. Responsibilities / go-live

**Why we ask:** A technically clean deploy is worthless if, at go-live, it is unclear who decides, who approves, and who acts in case of failure. Clear responsibilities, an agreed cutover plan, and a defined rollback make the transition into live operation plannable and significantly reduce risk.

- Who are the contacts on the customer IT side (business, technical, operations)? Please include role and availability.
- What is the RACI breakdown for build, operation, and maintenance of the solution?
- What does the escalation path look like (levels, contacts, response times)?
- Which maintenance windows are available for deployments and changes?
- Which SLAs apply to availability, response, and recovery times?
- How should the cutover/go-live proceed (big bang, phased, parallel run)? Is there a fixed date?
- How is the rollback strategy defined (criteria, responsible parties, technical implementation)?
- Who takes over operation and maintenance after go-live — customer, us, shared?

---

## Note

Based on your answers, the **individual integration and CI part of the project setup** is created: the concrete connection of the solution to your pipelines, target systems, network and secrets infrastructure, as well as the agreed go-live and rollback plan. Open points are documented as assumptions and refined together before they feed into implementation.
