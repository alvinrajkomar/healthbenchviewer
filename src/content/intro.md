# Introduction to HealthBench

**HealthBench** is an open-source benchmark developed by OpenAI to evaluate the performance and safety of large language models (LLMs) in healthcare contexts.  

---

## What is in the benchmark?

Unlike prior benchmarks that rely on multiple-choice questions or narrowly scoped tasks, HealthBench presents 5,000 realistic multi-turn **conversations** between LLMs and users—including both laypeople and healthcare professionals. Each conversation (also called an example) is classified into one of the following **themes**:

- **Context seeking**  
  Evaluates whether models recognize when information is missing and ask clarifying questions to proceed safely.  
  - A user asks whether they should take a treatment, but the answer depends on missing personal details.  
  - A vague user query like “Should I change my meds?” lacking context.  
  - A moderately detailed conversation where crucial details (like symptoms or duration) are still missing.  
  - An informational question (e.g., "What is the treatment for asthma?") that depends on severity or subtype.

- **Emergency referrals**  
  Measures a model’s ability to recognize medical emergencies and recommend appropriate urgent care.  
  - Emergent: A user describes chest pain and shortness of breath—model should urge immediate emergency care.  
  - Conditionally emergent: A user describes symptoms that might be emergent depending on risk factors (e.g., dizziness and vision changes).  
  - Non-emergent: A user asks about mild symptoms (e.g., seasonal allergies)—model should recommend routine care if necessary, not emergency services.

- **Global health**  
  Evaluates model ability to adapt to diverse healthcare contexts across geographies, resources, and norms.  
  - A user asks about malaria treatment in a region where drug resistance varies—model should consider local context.  
  - A user in a low-resource setting asks about pregnancy complications—model should adapt to resource availability.  
  - A universal question like “What is the normal body temperature?” where local context is irrelevant.

- **Responding under uncertainty**  
  Assesses whether models recognize uncertainty in situations and respond with appropriately cautious language.

- **Expertise-tailored communication**  
  Tests if models can tailor responses based on the user's role (e.g., layperson vs. healthcare professional).

- **Health data tasks**  
  Focuses on structured tasks like documentation or summarization, where factual precision is critical.

- **Response depth**  
  Assesses whether the model provides an appropriate level of detail—neither too brief nor overwhelming for the task.

---

## How are the conversations/examples scored?

Each conversation is evaluated against **detailed, physician-written** rubrics that reflect real-world expectations. There are **48,562 unique criteria** authored by **262 physicians** across **26 specialties** and **60 countries**.

Each example is scored along one or more of five behavior axes:
- Accuracy  
- Completeness  
- Communication quality  
- Context awareness  
- Instruction-following  

HealthBench was created to address critical limitations in existing health AI benchmarks. Specifically, it attempts to ensure evaluations are:
- **Meaningful** (reflecting real-world impact)  
- **Trustworthy** (aligned with expert medical judgment)  
- **Unsaturated** (offering room for model improvement)  

---

## Sub-benchmarks

HealthBench includes two special subsets:

- **HealthBench Consensus**  
  Focuses on 34 physician-validated behavioral criteria shared across examples. These allow consistent tracking of critical behaviors.

- **HealthBench Hard**  
  A challenging subset where even the best models struggle, designed to push boundaries and diagnose failure modes.

---

By enabling robust, physician-grounded assessments of model performance across realistic scenarios, **HealthBench** provides a comprehensive benchmark to guide the development of safer and more capable AI systems in healthcare.
