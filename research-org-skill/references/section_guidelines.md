# Research Section Guidelines

This document provides detailed guidance for each section of the company research report. Follow these guidelines to ensure comprehensive, well-structured research that provides strategic value.

## Research Mantras

Strong research combines:
1. **Depth** - Meet word count range of targetWordCount from config.json (each section includes target lengths)
2. **Accuracy** - Verifiable sources and citations throughout. Do not make claims that cannot be verified. Note when information is derived or estimated.
3. **Balance** - Both positive (strengths/opportunities) and negative (weaknesses/risks) perspectives. Do not be biased.
4. **Clarity** - Accessible prose that explains specialized concepts
5. **Strategic Value** - Insights that inform decision-making, not just information collection

## Citation and Reference Best Practices

Reference links are REQUIRED throughout. Every major claim, metric, or fact must be linked to its source inline. See `references/writing_style.md` for detailed citation formatting, link density targets, and examples.

---

# 0. Structure
This structure is the EXACT order that must be followed:

# Company Overview
## Founding Story
## Mission and Vision
## Thesis
## Business Model
# Executive Team
# Investors, Funding Rounds, and Valuation
## Funding Rounds (table)
## Valuation Analysis (narrative below table)
# Products and Services
# Notable Partnerships and Customers
# Market
## Customer
## Market Size and Opportunity
## Market Dynamics and Trends
## Competitive Landscape Overview
## Key Competitors (table)
## Competitive Advantages
## Traction
# Opportunities and Risks
## Key Opportunities
## Key Risks
## SWOT Analysis
### Strengths
### Weaknesses
### Opportunities
### Threats

---

## 1. Company Overview

**Purpose:** Provide a clear, compelling summary of what the company does, who they serve, and their value proposition.

**Guidelines:**
- Open with a 2-3 sentence description of the company's core business
- Clearly articulate the problem they solve and for whom
- Highlight key differentiators or unique approach
- Include founding year and headquarters location
- Mention current scale indicators (employees, customers, geographic presence) if available
- Write 2-4 paragraphs in clear, engaging prose
- Avoid jargon; use language that would be clear to someone unfamiliar with the company
- Focus on what makes them distinctive in their market
- Include reference links to key sources (company website, prominent news articles, analyst reports)

**Expected Length:** 2-4 paragraphs

---

## 1a. Founding Story

**Purpose:** Provide context on how and why the company was started.

**Guidelines:**
- Describe the origin story and founding team's background
- Explain what problem or insight led to the company's creation
- Include founding year and initial focus
- Mention key pivots or evolution in the company's direction if relevant
- Highlight founder credentials, previous experience, or domain expertise that informed the founding
- Write 2-3 paragraphs in narrative form
- Include citations or links to founding announcements and early coverage

**Expected Length:** 2-3 paragraphs

---

## 1b. Mission and Vision

**Purpose:** Articulate the company's stated purpose and long-term ambitions.

**Guidelines:**
- Identify explicit mission and vision statements from official sources (website, investor decks, founder interviews)
- Paraphrase in company's own language if official statements are unclear
- Explain the core philosophy or values driving the company
- Connect mission to founding story and current strategy
- Distinguish between mission (current purpose) and vision (future state)
- Write 2-3 focused paragraphs
- Link to official sources (company manifesto, founder interviews, mission statements)

**Expected Length:** 1-2 paragraphs or a bulleted list

---

## 1c. Thesis

**Purpose:**

Write a compelling Company Thesis section that articulates why this company represents an exceptional investment opportunity. Structure your analysis using these guidelines:

- Market Convergence & Timing: Open by identifying 2-3 major trends or market forces that converged to create the opportunity. Include specific market size data, growth rates, or supply-demand imbalances that quantify the opportunity. Explain why now is the right time for this solution.
- Competitive Differentiation: Articulate the company's unique approach versus competitors. Be specific about what competitors do (name them) and how this company's solution is fundamentally different or more comprehensive. Focus on structural advantages, not just features.
- Technology & Capability Inflection: Identify the technological or market inflection point that makes this solution possible now but wasn't feasible before. Reference specific timeframes, technological breakthroughs, or capability thresholds that enable the business model.
- Economic Disruption: Quantify the improvement in unit economics, speed, cost, or accessibility compared to traditional approaches. Use specific numbers (10x, 100x) and concrete before/after comparisons that demonstrate the magnitude of improvement.
Synthesis: Ensure the thesis flows as a cohesive narrative that connects market opportunity → unique solution → right team → right time → validated traction → massive potential. Each element should reinforce the others to build conviction.

**Expected Length:** 2-4 paragraphs

---

## 1d. Business Model

**⚠️ REMINDER:** Business Model section appears HERE in the report structure (position 1d, after Thesis, before Executive Team). Do NOT place it later in the report.

**Purpose:** Explain how the company makes money and scales.

**Guidelines:**
- Describe revenue model:
  - Pricing approach (per-seat, per-transaction, subscription, hybrid, etc.)
  - Typical deal size or contract terms
  - Customer acquisition cost (CAC) if available
  - Customer lifetime value (LTV) if available
- Explain go-to-market strategy:
  - Sales motion (direct sales, self-serve, marketplace, partnerships)
  - Sales cycle length
  - Channel strategy (if applicable)
- Describe unit economics where possible:
  - Gross margins
  - Customer acquisition cost
  - Net revenue retention / expansion revenue
- Discuss competitive pricing and positioning
- Include links to pricing pages or case studies that reveal business model

**Expected Length:** 4-8 paragraphs

---

## 2. Executive Team

**Purpose:** Showcase leadership depth and relevant expertise.

**Guidelines:**
- List key executives with titles
- For each leader at C-level or SVP level, include:
  - Relevant background and previous companies/roles
  - Notable achievements or domain expertise
  - How long they've been with the company
  - Their specific role in current strategy
- Present in a structured format (can use a table or formatted list)
- Focus on C-suite, SVP-level roles, and specialized expertise areas
- Include educational background when relevant to credibility
- Explain how executive team composition strengthens company positioning
- Include LinkedIn profile links where relevant for verification

**Expected Length:** Varies (typically 1 paragraph per executive)

---

## 3. Investors, Funding Rounds, and Valuation

**Purpose:** Document the company's funding history and financial backing.

### 3a. Funding Rounds Table

Create a comprehensive funding table with columns:
- **Round** (Seed, Series A, Series B, include any M&A activity in the timeline, etc.)
- **Date** (when the round closed)
- **Amount Raised** (dollar amount)
- **Valuation** (post-money valuation; note if estimated)
- **Lead Investors** (primary investors in that round)
- **Notes** (other investors, relevant context or conditions, and relevant metrics)

**Table Guidelines:**
- Include all known funding rounds in chronological order
- For M&A activity: 
  - Note which company was acquired, when, for how much, and strategic rationale as a separate row in the table, e.g.:
    - | M&A: Acquires TechCo | Q3 2023 | Acquisition | $50M | - | Strategic product acquisition for vertical expansion |
- Valuation Estimation: If valuations are missing for some rounds, use the method outlined in references/valuation_guide.md
  - Clearly mark estimated valuations as "~$XX (estimated)"
  - Mark unavailable valuations as "Not available"

**Table Format Example:**

```markdown
<table header-row="true">
<tr>
<td>Round</td>
<td>Date</td>
<td>Amount Raised</td>
<td>Valuation</td>
<td>Lead Investors</td>
<td>Notes</td>
</tr>
<tr>
<td>Seed</td>
<td>Q1 2022</td>
<td>$5M</td>
<td>$25M</td>
<td>Investor A</td>
<td>First institutional funding</td>
</tr>
<tr>
<td>Series A</td>
<td>Q3 2023</td>
<td>$50M</td>
<td>~$200M (estimated)</td>
<td>Investor B (lead), Investor A</td>
<td>Estimated using 4x ratio</td>
</tr>
</table>
```

### 3b. Funding Summary (Below Table)

Include a summary covering:
- **Total Funding:** Total amount raised and number of rounds
- **Lead Investors:** List prominent investors and their significance:
  - First institutional investors and their relevance
  - Strategic investors (customers, partners) and their strategic importance
  - Notable repeat investors across rounds
  - Board observers or board members from investor firms
- **Valuation Trajectory:** Analyze valuation changes:
  - Growth rate between rounds
  - Comparison to industry benchmarks
  - What valuation trends reveal about company progress
  - Investor sentiment and market positioning
- ** Use of Funding**: If available, include how the company plans to deploy the new capital, such as:
  - R&D
  - Sales and marketing
  - Geographic expansion
  - Acquisitions

**Expected Length:** 2-4 paragraphs of narrative analysis BELOW the table

---

## 4. Products and Services

**Purpose:** Detail what the company offers and how their solutions work.

**Guidelines:**
- Describe each major product or service offering
- Explain key features and capabilities
- Detail the technology stack or approach where relevant
- Describe the user experience or customer journey
- Highlight unique or innovative aspects of their offerings
- Include specific examples of use cases
- Note any integrations or platform partnerships
- Organize by product line if they have multiple offerings
- Include links to product pages, demos, or technical documentation

**Expected Length:** 4-8 paragraphs

---

## 5. Notable Partnerships and Customers

**Purpose:** Demonstrate market validation and go-to-market strength.

**Guidelines:**
- List major customers (with permission/if public)
- Describe key partnership relationships
- Highlight notable logos or case studies
- Include customer testimonials or results if available
- Note any channel partnerships or distribution agreements
- Mention customer segments served (e.g., enterprise, mid-market, SMB)
- Provide specific examples of customer success or adoption
- For major customers, note:
  - Industry or vertical they represent
  - Scale or significance
  - Known outcomes or case studies
- Explain what customer composition reveals about go-to-market strategy
- Include press releases or case study links

**Expected Length:** 4-8 paragraphs

---

## 6. Market

**Purpose:** Define the addressable market, customer characteristics, and market dynamics.

---

## 6a. Customer

Describe the ideal customer:
- Company size, industry, geographic focus
- Specific pain points the company solves
- Decision-making process and buying committee
- Budget range or typical deal size (if known)
- Examples of customer types already won

**Expected Length:** 4-6 paragraphs

---

## 6b. Market Size and Opportunity

Provide quantitative market analysis:
- Total addressable market (TAM) with source and date
- Serviceable available market (SAM) if different from TAM
- Market growth rate (CAGR) and projection period
- Key drivers of market growth
- Market segmentation (by vertical, geography, company size, etc.)
- Cited sources and links to market research reports

**Expected Length:** 4-6 paragraphs

---

## 6c. Market Dynamics and Trends

Analyze what's driving adoption:
- Industry tailwinds (regulatory changes, technology shifts, etc.)
- Customer priorities and changing needs
- Competitive intensity
- Consolidation trends
- Link to relevant industry reports and analyses

**Expected Length:** 4-6 paragraphs

---

## 6d. Competitive Landscape Overview 

**Purpose:** Position the company within the competitive landscape.

- Identify categories of competitors:
  - Direct competitors (similar product, similar customer)
  - Indirect competitors (alternative solutions)
  - Potential future competitors (platform players, adjacent vendors)
- Explain competitive dynamics and market maturity

**Expected Length:** 2-4 paragraphs

---

## 6e. Key Competitors (table)

Identify competitors to the target company. Consider product and/or service offerings, categories, and target markets. Carefully evaluate each potential competitor -- are they specifically targeting the same customers, solving the same problems, or offering similar solutions? If they are simply in a similar market or industry, but not directly competing, do not include them.

For each major competitor, include:
- Company name (linked to their website)
- Founded year and funding/valuation
- Company focus and positioning
- Key differentiators vs. the company being researched
- Links to competitor websites and key resources

**Table Format Example:**

```markdown
<table header-row="true">
<tr>
<td>Company</td>
<td>URL</td>
<td>Founded</td>
<td>Focus/Positioning</td>
<td>Key Differentiators</td>
</tr>
<tr>
<td>Competitor A</td>
<td>competitora.com</td>
<td>2019</td>
<td>Enterprise-focused platform</td>
<td>Strong in healthcare vertical, raised $200M</td>
</tr>
</table>
```

---

## 6f. Competitive Advantages

- What defensible advantages does the company have?
- Data moats, brand, switching costs, technical depth, etc.
- How sustainable are these advantages?

**Expected Length:** 2-3 paragraphs

---

## 6g. Traction

**Purpose:** Demonstrate momentum and successful execution.

**Guidelines:**
- Quantify revenue growth with specific numbers and time periods
- Include customer growth metrics (number of customers, customer logos, growth rate)
- Highlight key milestones:
  - Product launches
  - Partnership announcements
  - Award/recognition wins
  - Geographic expansion
  - Team growth
- Provide financial metrics:
  - ARR/MRR if available
  - Net revenue retention (NRR)
  - Growth rate (YoY %)
  - Unit economics improvements
- Date all metrics and note sources
- Include links to press releases and announcements supporting key milestones

**Expected Length:** 3-5 paragraphs

---

## 7. Opportunities and Risks

---

## 7a. Key Opportunities

**Purpose:** Identify 3-5 major growth opportunities and strategic options.

**Guidelines:**
- For each opportunity:
  - Clearly state the opportunity
  - Explain why it's significant (market size, competitive advantage)
  - Describe how the company could pursue it
  - Identify risks or execution challenges
  - Estimate potential impact on the business
- Distinguish between:
  - Product expansion (new features, new verticals)
  - Geographic expansion
  - Business model evolution
  - Strategic partnerships or M&A
  - Data or technology leverage (data moats, IP)
- Write objectively, not as marketing
- Ground opportunities in company strengths and market trends identified in earlier sections

**Expected Length:** 2-4 paragraphs

---

## 7b. Key Risks

**Purpose:** Identify material risks to the company's success.

**Guidelines:**
- For each risk:
  - Clearly state the risk
  - Explain why it's significant
  - Assess probability (high/medium/low)
  - Assess impact (high/medium/low)
  - Identify mitigation strategies if company is pursuing them
  - Note how risk might manifest
- Categories of risks to consider:
  - Market/competitive risks
  - Execution/operational risks
  - Financial/unit economics risks
  - Regulatory/compliance risks
  - Technology/product risks
  - Key person risks
  - Customer concentration risks
- Write objectively and balanced
- Avoid speculation; ground in evidence

**Expected Length:** 2-4 paragraphs

---

## 8. SWOT Analysis

**Purpose:** Synthesize strengths, weaknesses, opportunities, and threats.

**Guidelines:**

### 8a. Strengths: Internal capabilities, assets, competitive advantages
  - Proprietary technology
  - Team depth/expertise
  - Customer relationships/references
  - Data or information advantages
  - Brand or market position

### 8b. Weaknesses: Internal limitations or gaps
  - Execution gaps
  - Resource constraints
  - Limited market presence
  - Product gaps vs. competitors
  - Dependency on key people/technologies

### 8c. Opportunities: External positive factors (from earlier opportunities section)
  - Market growth
  - Adjacency expansion
  - Partnership/ecosystem plays
  - Strategic acquisition targets
  
### 8d. Threats: External negative factors (from earlier risks section)
  - Competitive threats
  - Market downturns
  - Regulatory changes
  - Technology disruption
  - Customer concentration

**Expected Length:** 3-5 bullet points per subsection (Strengths, Weaknesses, Opportunities, Threats) with each bullet including a 1-4 word title (bolded) followed by 1-2 sentences summarizing the key points.

---
