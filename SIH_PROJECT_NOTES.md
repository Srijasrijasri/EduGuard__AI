# Smart India Hackathon (SIH) & Final-Year Viva Presentation Notes

**Project Title**: AI-Based Student Risk Prediction & Early Support System  
**Domain**: Smart Education / AI for Academic Excellence  
**Tech Stack**: Python, Flask, Scikit-Learn, Random Forest, SQLite, HTML5, CSS3, JavaScript, Chart.js  

---

## 1. Problem Statement
In higher educational institutions, academic failure, course backlogs, and student dropouts often occur because struggling students are identified **too late**—typically after semester exam results are published. Existing approaches rely on manual, end-of-term evaluations without automated risk monitoring.

---

## 2. Proposed Solution & Innovation
**EduGuard AI** is a proactive, data-driven academic early-warning system. By analyzing continuous student indicators—attendance, internal test scores, assignment completion, daily study hours, previous semester percentages, and active backlogs—the system uses a trained **Random Forest Classifier** to evaluate risk levels (**LOW**, **MEDIUM**, **HIGH**) in real-time with confidence scores.

### Key Innovation:
* **Pre-emptive Classification**: Detects risk weeks before final exams.
* **Dual Engine Architecture**: Combines Machine Learning for risk classification with a Rule-Based Recommendation Engine for tailored, actionable study plans.
* **Privacy-First Design**: Operates on synthetic or anonymized datasets without storing sensitive personal credentials.

---

## 3. Technical Architecture
```text
[Student Metrics] -> [Form Validation] -> [Scikit-Learn Preprocessor] -> [Random Forest ML Model] -> [Risk & Confidence %] -> [Recommendation Engine] -> [SQLite DB & Chart.js Dashboard]
```

---

## 4. Machine Learning Methodology
* **Algorithm**: Random Forest Classifier (`n_estimators=120`, `max_depth=10`).
* **Preprocessing**: `ColumnTransformer` applying `StandardScaler` on numerical features and `OneHotEncoder` on categorical features.
* **Train/Test Split**: 80/20 Stratified Split (`random_state=42`).
* **Accuracy**: **85.00%**
* **Weighted F1-Score**: **85.08%**

---

## 5. 2-Minute Elevator Pitch Script
> "Good morning judges/examiners. In many colleges, students who are struggling academically are only noticed after they fail their final exams. 
> 
> Our project, **AI-Based Student Risk Prediction & Early Support System**, solves this by giving faculty a real-time early warning tool. We input key student indicators like attendance, internal marks, study hours, and backlogs into a trained Random Forest machine learning model. The system predicts if a student is at Low, Medium, or High risk with a confidence percentage, and immediately generates customized recommendations—such as meeting faculty mentors, attending remedial classes, or increasing daily study hours.
> 
> It also provides an interactive analytics dashboard using Chart.js so department heads can track overall class risk distributions and attendance patterns. This ensures early intervention, reduces backlog counts, and improves overall graduation rates."

---

## 6. 5-Minute Detailed Presentation Pitch Script
> **Slide 1: Introduction**  
> "Hello everyone. Today we present our AI-Based Student Risk Prediction & Early Support System built using Python, Flask, Scikit-learn, and SQLite."
> 
> **Slide 2: Problem & Existing System**  
> "Currently, most institutions track student performance reactively. Faculty mentors only review results after exams. By then, it is too late to prevent backlogs or dropouts."
> 
> **Slide 3: Our AI Solution**  
> "Our solution continuously monitors multiple academic factors: attendance, internal marks, assignment scores, study hours, previous semester grades, and backlogs. Our ML pipeline normalizes numerical data with StandardScaler, encodes categorical variables, and feeds them into a Random Forest Classifier trained on 1,200 student records."
> 
> **Slide 4: Results & Demonstration**  
> "Our model achieves an 85% accuracy rate on test data. When a student is evaluated, the system displays their predicted risk level alongside a confidence score, contributing deficit factors, and an automated step-by-step academic action plan."
> 
> **Slide 5: Dashboard & Impact**  
> "The platform includes a real-time institutional dashboard with Chart.js charts showing risk distribution, attendance vs risk level, and internal marks comparison, along with a searchable database log."
> 
> **Slide 6: Conclusion & Future Scope**  
> "In the future, this system can be integrated directly with Canvas or Moodle LMS via REST APIs and send automated WhatsApp/SMS alerts to faculty. Thank you!"

---

## 7. Common Viva / Judge Questions & Answers

### Q1: Why did you choose Random Forest instead of Decision Trees or Logistic Regression?
**Answer**: Decision Trees tend to overfit on single academic attributes, while Logistic Regression assumes linear decision boundaries. Random Forest builds an ensemble of multiple decision trees, providing higher accuracy (85%), robustness against noisy data, and better generalization across varied student profiles.

### Q2: Why is the recommendation system rule-based instead of ML-based?
**Answer**: The ML model excels at statistical pattern classification (`Low`, `Medium`, `High` risk). However, actionable advice (e.g., 'Increase attendance above 75%') must follow strict academic compliance rules set by university policies. Combining ML prediction with rule-based recommendations gives us the best of both worlds: data-driven prediction with deterministic, compliant guidance.

### Q3: How do you prevent Data Leakage during model training?
**Answer**: We fit all transformers (`StandardScaler`, `OneHotEncoder`) strictly inside a Scikit-Learn `Pipeline` on the training dataset split only, and apply standard `train_test_split(..., stratify=y, random_state=42)` to ensure identical target distributions across splits without test set leakage.

### Q4: Does the system replace faculty mentors?
**Answer**: No. The system serves as a decision-support tool. It empowers faculty mentors with early insights and clear data so they can intervene effectively before exams.

### Q5: How would this scale to a real university with 10,000 students?
**Answer**: The Flask application can be deployed using Gunicorn behind an Nginx reverse proxy. The SQLite database can be migrated to PostgreSQL without changing application logic, and batch predictions can be processed asynchronously using Celery task queues.
