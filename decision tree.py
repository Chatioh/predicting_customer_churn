from main import *
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler

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

# Step 6: Split between train and test
train_set, test_set = split_by_time_period(data_set)

# Step 7: Obtain target and features
Target, Features = obtain_target_and_features("churn", train_set)

# Step 9: Normalize scale
scaler = StandardScaler()
x_resampled, y_resampled = handle_class_imbalance(train_set, "churn")

# Step 10: Oversampling to balance the classes
x_resampled_scaled = scaler.fit_transform(x_resampled)

# Step 11: Train Decision Tree Classifier
decision_tree = DecisionTreeClassifier(random_state=42)
decision_tree.fit(x_resampled_scaled, y_resampled)

# Step 12: Evaluate Decision Tree on Test Set
test_features_scaled = scaler.transform(test_set.drop(columns=["churn"]))  # Scale test features
test_target = test_set["churn"]

# Predictions
y_pred_tree = decision_tree.predict(test_features_scaled)
y_pred_proba_tree = decision_tree.predict_proba(test_features_scaled)[:, 1]

# Performance Metrics
# print("Decision Tree Classification Report:")
# print(classification_report(test_target, y_pred_tree))

roc_auc_tree = roc_auc_score(test_target, y_pred_proba_tree)
print(f'ROC AUC Score for Decision Tree: {roc_auc_tree:.4f}')

# Step 13: Evaluate on Year 2 Data
year2_data = data_set.iloc[:4000]  # Next 4000 rows
year2_features = year2_data.drop(columns=["churn"])
year2_target = year2_data["churn"]

# Scale features
year2_features_scaled = scaler.transform(year2_features)

# Predictions for Year 2
y_pred_year2 = decision_tree.predict(year2_features_scaled)
y_pred_proba_year2 = decision_tree.predict_proba(year2_features_scaled)[:, 1]

# Performance Metrics for Year 2
print("Year 2 Classification Report:")
print(classification_report(year2_target, y_pred_year2))

roc_auc_year2 = roc_auc_score(year2_target, y_pred_proba_year2)
print(f'ROC AUC Score for Year 2: {roc_auc_year2:.4f}')

# Step 14: Evaluate on Year 3 Data
year3_data = data_set.iloc[-1000:]  # Last 1000 entries
year3_features = year3_data.drop(columns=["churn"])
year3_target = year3_data["churn"]

# Scale features
year3_features_scaled = scaler.transform(year3_features)

# Predictions for Year 3
y_pred_year3 = decision_tree.predict(year3_features_scaled)
y_pred_proba_year3 = decision_tree.predict_proba(year3_features_scaled)[:, 1]

# Performance Metrics for Year 3
print("Year 3 Classification Report:")
print(classification_report(year3_target, y_pred_year3))

roc_auc_year3 = roc_auc_score(year3_target, y_pred_proba_year3)
print(f'ROC AUC Score for Year 3: {roc_auc_year3:.4f}')

# Step 15: Investigate Changes Over Time
# You can compare the ROC AUC scores and classification reports for Year 2 and Year 3
print(f"Comparison of ROC AUC Scores: Year 2: {roc_auc_year2:.4f}, Year 3: {roc_auc_year3:.4f}")

# Additional analysis for concept drift or data shift
if roc_auc_year3 < roc_auc_year2:
    print("Warning: Potential concept drift detected. Model performance has deteriorated from Year 2 to Year 3.")
else:
    print("Model performance is consistent or improved from Year 2 to Year 3.")
