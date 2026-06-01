# Pre-onboarding questionnaire: before we set up your project

> **What is this?** We're setting up a modern, AI-assisted development environment for your project (internally the "INTENTRON" framework). Before we start, we hold a short setup call (~15 min). To make it fast and focused, we send you these questions in advance.
>
> **What you need to do:** nothing to install, nothing to prepare — just read these questions and, where possible, have answers ready. It's only about us understanding **what you want to build** and **in which environment**. The clearer your answers, the better the setup fits from day one.
>
> **Unsure about a question?** Totally fine — mark it "don't know yet / let's clarify together". Nobody needs to know everything: some questions are for your IT, others for the business side or management.

## Part 1 — What do you want to build?

**1. What is the project about?**
In 2–3 sentences: what should the software do, and for whom?
- *Why we ask:* We need to understand the purpose to set sensible quality and security rules.
- *Example answer:* "An internal web portal where our field staff log orders and see their status."

**2. Which technology is planned?**
Do you already know what it's built with? Programming language (e.g. Java, .NET, Node.js, Python) — and is there a web interface (e.g. React/Angular)? "Not decided yet" is also a valid answer.
- *Why:* It determines which test and check tools we wire in.
- *Example answer:* "Backend in Java (Spring Boot), web frontend in Angular." — or: "Still open, please advise."

**3. Does the software have a web interface where speed matters?**
E.g. a customer portal that must load fast.
- *Why:* Then we add an automatic performance check that, on every change, verifies load time and usability.
- *Example answer:* "Yes, a public customer portal — load time is business-critical." / "No, internal tool only."

**4. Does your team work with an AI coding assistant?**
E.g. Claude, GitHub Copilot/Codex, Cursor — or none yet?
- *Why:* The framework aligns to the AI tool your developers actually use.
- *Example answer:* "We use Claude; some developers also Cursor."

**5. Project basics.**
What should the project be called? One sentence on what it does. Is there a starting version number (otherwise we use 0.1.0)?
- *Example answer:* "Project 'FieldOrderPortal', order entry for field staff, start 0.1.0."

**6. What do you use to plan tasks and tickets?**
Jira, Azure DevOps, GitHub Issues, Linear — or nothing yet?
- *Why:* We connect the framework to your existing tool so tasks stay visible where you already work.
- *Example answer:* "Jira, project key AP." / "Nothing yet — please suggest."

**7. Any special requirements around data protection, regulation or AI?**
Does any of this apply? (Multiple possible.)
- The software processes **personal / customer data** → topic **data protection (GDPR)**
- The software contains an **AI component that processes (customer) data** → topic **EU AI Act** (AI regulation with documentation duties)
- You're in a **regulated industry** (finance, health, insurance, legal)
- High **cost relevance** (lots of AI/cloud/SaaS spend)
- *Why:* Depending on your answer we automatically switch on matching protection and evidence mechanisms (e.g. data-protection checks, AI documentation). If none applies, it stays lean.
- *Example answer:* "Yes — processes customer data, finance industry, AI component for fraud detection."

**8. How strict do the rules need to be?**
How critical or regulated is the project?
- **light** — internal helper tool, low risk
- **normal** — production software, usual diligence
- **strict** — regulated/critical software with audit duty and four-eyes principle
- *Why:* This determines how many automatic checks and approval steps we build in. More strictness = more evidence (but also a bit more effort) — we match it to your risk.
- *Example answer:* "Strict — subject to financial supervision."

**9. Do multiple people work on the same code at the same time?**
- *Why:* For parallel work we set up separate work areas so changes don't overwrite each other.
- *Example answer:* "Yes, 4 developers in parallel." / "No, one person for now."

**10. Where is development done?**
Where does the team actually work with the environment?
- everyone **locally on their own machine/laptop**
- on a **shared development server** (e.g. a Linux server in the cloud)
- a **larger team on a central server**
- *Why:* It determines whether we set the environment up once centrally or per machine.
- *Example answer:* "Shared Linux server, 5 developers access it."

## Part 2 — What already exists?

**11. Does the project already exist, or are we starting fresh?**
If it exists: where (server/path)? If new: where should it live?

**12. Do you have a code repository?**
E.g. GitHub, GitLab, Azure Repos — with an address (URL)? Or should one be created? Or none?
- *Why:* That's where the code lives, with its version history and the automatic checks.

**13. Where should the project documentation live?**
Do you have a wiki / Confluence / SharePoint / Notion — or should the docs sit next to the code?
- *Why:* So decisions and knowledge stay findable, even months later.
- *Example answer:* "Confluence space 'AP'." / "Next to the code is fine."

**14. What do you manage tickets with — concretely, incl. access?**
(Follows on from question 6.) Which exact tool, and the project/team key, so we can connect it.

**15. Are there already access keys / credentials the software needs?**
E.g. API keys to other systems.
- *Why:* We handle credentials securely and never store them openly in the code.
- *Example answer:* "Yes, already collected." / "None yet."

**16. Should we create an onboarding doc for new team members?**
- *Why:* So new developers — or another tool — can take over the project quickly without having to bother you.

**Extra — do you already have this?**
- **Monitoring** (e.g. Grafana, a logging system): present and reuse, build new, or still open?
- Do you need **research or diagram functions** in the setup (optional)?

## Part 3 — let's clarify together on the call

- **Doc structure:** Who on your side decides on documentation storage and structure (any mandates, an existing wiki, naming conventions)?
- **Optional automations:** Do you want extras like automatic self-checks, doc synchronization or a learning loop? Any operational objections to automations that write into your environment? — we decide together.

## If the software is later integrated into your live environment

If the finished result is to be embedded into your existing systems (hosting, your deployment processes, interfaces to other systems, network, credentials, approval processes), there's a complementary sheet (`integration-discovery.md`) — we'll send that separately once we get there.

> **Only for whoever sets up the environment technically** (your IT): a current Node.js version, Git and an AI coding tool should be available, plus access to the AI tool / repository / ticket tool. We provide the exact steps.
