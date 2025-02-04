from main import *
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Step 1: Import and Clean Data
data_set = import_and_clean_data("data.csv", ['customer_id'])
print(data_set.head())
print(data_set.info())

# Step 2: Convert relevant columns to numeric
data_set = convert_row_to_numeric(['age','income', 'monthly_minutes', 'monthly_data_gb', 'support_tickets', 'monthly_bill', 'outstanding_balance', 'churn'], data_set)
print(data_set.info())

# Step 3: Remove outliers based on normal distribution for specified columns
data_set, normal_outliers = remove_outliers_normal_distribution_data(data_set, ['age', 'monthly_minutes', 'outstanding_balance'])

# Step 4: Remove outliers for skewed distributions
data_set, skewed_outliers = remove_outliers_skewed_distributions(data_set, ['income', 'monthly_data_gb', 'support_tickets', 'monthly_bill'])
print(data_set.head())
print(data_set.info())

# Step 5: One-Hot Encode categorical variables (e.g., 'region')
data_set = pd.get_dummies(data_set, columns=['region'], drop_first=True)

# Step 6: splits the data according to year
year1_data, year2_data, year3_data = divide_into_years(data_set)
print(year1_data.info())
print(year2_data.info())
print(year3_data.info())
year1_2_data = data_set[:4000]

# obtain target and features for each year
year1_target, year1_features = obtain_target_and_features("churn", year1_data)
year2_target, year2_features = obtain_target_and_features("churn", year2_data)
year3_target, year3_features = obtain_target_and_features("churn", year3_data)
year1_2_target, year1_2_features = obtain_target_and_features("churn", year1_2_data)

year1_features = normalise_scale(year1_features)
year2_features = normalise_scale(year2_features)
year3_features = normalise_scale(year3_features)
year1_2_features = normalise_scale(year1_2_features)

# Step 9 plot their graph
correlation_matrix = explore_correlations(year1_features)
correlation_matrix2 = explore_correlations(year2_features)
correlation_matrix3 = explore_correlations(year3_features)
correlation_matrix4 = explore_correlations(year1_2_features)

# Step 10: Over sampling every year's data and normalise it. x are features and y target
x_1, y_1 = handle_class_imbalance(year1_data, "churn")
x_2, y_2 = handle_class_imbalance(year2_data, "churn")
x_3, y_3 = handle_class_imbalance(year3_data, "churn")
x1_2, y1_2 = handle_class_imbalance(year1_2_data, "churn")

# step 11: Train Logistic Regression for year 1
log_reg = LogisticRegression(max_iter=2000, solver='liblinear')
log_reg.fit(x_1, y_1)

# Predict on year 2
y2_pred_log_reg = log_reg.predict(x_2)

# Evaluate Model Performance on Year 2
# Logistic Regression Performance on Year 2
log_reg_accuracy = accuracy_score(y_2, y2_pred_log_reg)
log_reg_precision = precision_score(y_2, y2_pred_log_reg)
log_reg_recall = recall_score(y_2, y2_pred_log_reg)
log_reg_f1 = f1_score(y_2, y2_pred_log_reg)

# Step 12: Train on Year 2 Data and Test on Year 3
# Train Logistic Regression on Year 2
log_reg.fit(x_2, y_2)

# Predict on Year 3
y3_pred_log_reg = log_reg.predict(x_3)

# Evaluate Model Performance on Year 3
# Logistic Regression Performance on Year 3
log_reg_accuracy_y3 = accuracy_score(y_3, y3_pred_log_reg)
log_reg_precision_y3 = precision_score(y_3, y3_pred_log_reg)
log_reg_recall_y3 = recall_score(y_3, y3_pred_log_reg)
log_reg_f1_y3 = f1_score(y_3, y3_pred_log_reg)

# Step 13: Train on year 1 and 2 and test on year 3
# Train Logistic Regression on Year 2
log_reg.fit(x1_2, y1_2)

# Predict on Year 3
y32_pred_log_reg = log_reg.predict(x_3)

# Evaluate Model Performance on Year 3
# Logistic Regression Performance on Year 3
log_reg_accuracy_y32 = accuracy_score(y_3, y32_pred_log_reg)
log_reg_precision_y32 = precision_score(y_3, y32_pred_log_reg)
log_reg_recall_y32 = recall_score(y_3, y32_pred_log_reg)
log_reg_f1_y32 = f1_score(y_3, y32_pred_log_reg)

# Step 14: Compare Performance Over Time
# Logistic Regression Performance across Years
log_reg_metrics_year2 = {
    "accuracy": log_reg_accuracy,
    "precision": log_reg_precision,
    "recall": log_reg_recall,
    "f1_score": log_reg_f1
}

log_reg_metrics_year3 = {
    "accuracy": log_reg_accuracy_y3,
    "precision": log_reg_precision_y3,
    "recall": log_reg_recall_y3,
    "f1_score": log_reg_f1_y3
}

log_reg_metrics_year3_by_12 = {
    "accuracy": log_reg_accuracy_y32,
    "precision": log_reg_precision_y32,
    "recall": log_reg_recall_y32,
    "f1_score": log_reg_f1_y32
}

# Print the performance across years for comparison
print("Logistic Regression Performance Comparison:")
print(f"Year 2: {log_reg_metrics_year2}")
print(f"Year 3: {log_reg_metrics_year3}")
print(f"Year 3 base on year 1 and 2:\n {log_reg_metrics_year3_by_12}")

