# AI-Based Student Risk Prediction & Early Support System

An end-to-end Machine Learning web application designed to predict student academic risk levels (**LOW RISK**, **MEDIUM RISK**, **HIGH RISK**) using academic performance, attendance, study habits, and backlog indicators. The system provides real-time predictions, actionable support recommendations, and institutional analytics for early academic intervention.

---

## 1. Project Overview & Objective

In modern higher education, students facing academic difficulties are often identified only after semester exam results are published, leaving little room for remedial support. 

This project addresses the problem by introducing a proactive **AI-Based Early Support System**:
* **Predicts Academic Risk**: Classifies students into `LOW RISK`, `MEDIUM RISK`, or `HIGH RISK` using a trained Scikit-Learn **Random Forest Classifier**.
* **Calculates Confidence Score**: Displays the model's prediction probability percentage (e.g., 87%).
* **Generates Early Intervention Plans**: Offers rule-based actionable recommendations for faculty mentors and students.
* **Institutional Dashboard**: Provides interactive Chart.js analytics for class-wide risk distribution and attendance metrics.

---

## 2. Technology Stack

* **Frontend**: HTML5, CSS3 (Custom Glassmorphism & Modern Palette), JavaScript (ES6+), Bootstrap 5 (CDN), Chart.js (CDN), FontAwesome 6
* **Backend**: Python 3.12, Flask
* **Machine Learning**: Scikit-Learn (`Pipeline`, `ColumnTransformer`, `RandomForestClassifier`, `StandardScaler`, `OneHotEncoder`), Pandas, NumPy, Joblib
* **Database**: SQLite3
* **Testing**: Python `unittest` / `pytest`

---

## 3. System Architecture

```
                                +---------------------------+
                                |    User Input (Web Form)  |
                                +-------------+-------------+
                                              |
                                              v
                                +---------------------------+
                                |  Input Data Validation    |
                                +-------------+-------------+
                                              |
                                              v
                                +---------------------------+
                                | Data Preprocessing Pipeline|
                                | (StandardScaler & OneHot) |
                                +-------------+-------------+
                                              |
                                              v
                                +---------------------------+
                                |  Random Forest ML Model   |
                                +-------------+-------------+
                                              |
                                              v
                                +---------------------------+
                                | Risk & Confidence Score   |
                                +-------------+-------------+
                                              |
                                              v
                                +---------------------------+
                                |  Rule Recommendations     |
                                +-------------+-------------+
                                              |
                                              v
                                +---------------------------+
                                | SQLite Persistence &      |
                                | Analytics Dashboard       |
                                +---------------------------+
```

---

## 4. Machine Learning & Model Evaluation

### Dataset
A realistic synthetic dataset of **1,200 student records** (`data/student_data.csv`) generated with statistical variance across key attributes:
* `attendance_percentage` (35% - 100%)
* `internal_marks` (10 - 100)
* `assignment_score` (15 - 100)
* `previous_semester_percentage` (35% - 100%)
* `study_hours_per_day` (0.5 - 10.0 hrs)
* `backlogs` (0 - 5)
* Categorical attributes: `gender`, `extracurricular_participation`, `family_support`, `internet_access`

### Model Performance
The Random Forest Classifier was trained using a stratified 80/20 train-test split (`random_state=42`):

* **Overall Accuracy**: **85.00%**
* **Weighted Precision**: **85.58%**
* **Weighted Recall**: **85.00%**
* **Weighted F1-Score**: **85.08%**

#### Confusion Matrix:
| Predicted / Actual | Low Risk | Medium Risk | High Risk |
|-------------------|----------|-------------|-----------|
| **Low Risk**      | 78       | 18          | 0         |
| **Medium Risk**   | 7        | 83          | 6         |
| **High Risk**     | 0        | 5           | 43        |

---

## 5. Project Directory Structure

```text
student-risk-prediction/
│
├── app.py                      # Main Flask application & routes
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation
├── SIH_PROJECT_NOTES.md        # SIH presentation & viva guide
├── .gitignore                  # Git exclusion rules
│
├── data/
│   ├── student_data.csv        # Synthetic student dataset (1,200 records)
│   └── generate_dataset.py     # Dataset generator script
│
├── ml/
│   ├── train_model.py          # ML training script (Pipeline + Random Forest)
│   ├── evaluate_model.py       # Performance evaluation metrics
│   └── risk_predictor.py       # Inference wrapper & recommendation engine
│
├── models/
│   └── student_risk_model.pkl  # Serialized ML model pipeline
│
├── database/
│   └── database.db             # SQLite database storage
│
├── templates/
│   ├── base.html               # Base layout template
│   ├── index.html              # Landing page
│   ├── predict.html            # Risk evaluation form
│   ├── result.html             # Assessment result & action plan
│   ├── dashboard.html          # Chart.js analytics dashboard
│   ├── students.html           # Historical records & live search
│   └── about.html              # System overview & problem statement
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom styling & glassmorphism theme
│   └── js/
│       └── script.js           # Chart.js initialization & live table filtering
│
├── tests/
│   └── test_app.py             # Automated test suite (9 test cases)
│
└── screenshots/
    └── .gitkeep
```

---

## 6. How to Run the Project

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate Dataset
```bash
python data/generate_dataset.py
```

### Step 3: Train Machine Learning Model
```bash
python ml/train_model.py
```

### Step 4: Evaluate Model Performance
```bash
python ml/evaluate_model.py
```

### Step 5: Run Automated Tests
```bash
python tests/test_app.py
```

### Step 6: Start Flask Web Server
```bash
python app.py
```

Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 7. Sample Test Data for Demonstration

Try entering the following sample student metrics in the `/predict` page:

| Field | Sample Input |
|-------|--------------|
| **Student Name** | Test Student |
| **Age** | 20 |
| **Gender** | Female |
| **Attendance %** | 55% |
| **Internal Marks** | 45 / 100 |
| **Assignment Score** | 50 / 100 |
| **Previous Sem %** | 52% |
| **Daily Study Hours** | 1.5 hrs/day |
| **Active Backlogs** | 2 |
| **Extracurriculars** | No |
| **Family Support** | Yes |
| **Internet Access** | Yes |

*Expected Output*: The trained ML model will evaluate the input and predict **HIGH RISK** (or **MEDIUM RISK**) with confidence score and tailored support guidelines.

---

## 8. Limitations & Future Scope

### Limitations
1. Uses synthetic data for demo purposes to protect student privacy.
2. Academic risk predictions are indicative and should support, not replace, faculty decision-making.

### Future Scope
* **LMS Integration**: Connect via APIs with Moodle / Canvas LMS to auto-fetch attendance and grades.
* **Automated Alerts**: Send automated SMS/Email notifications to faculty mentors when a student enters High Risk.
* **Deep Learning Expansion**: Train LSTM models on sequential semester progress trends.

---

## 9. SIH Relevance & Resume Summary

### Resume Description
> **AI-Based Student Risk Prediction & Early Support System**  
> *Tech Stack*: Python, Flask, Scikit-learn, Random Forest, SQLite, HTML5, CSS3, JavaScript, Chart.js  
> Developed a web application to predict student academic risk using attendance, internal marks, study habits, and backlog metrics. Implemented a Random Forest Classifier achieving 85.0% accuracy alongside a Flask backend, SQLite persistence, and Chart.js analytics dashboard for early academic intervention.
