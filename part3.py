import syft as sy
import sklearn

data_site = sy.orchestra.launch(name="cancer-research-centre")

client = data_site.login(email="rachel@datascience.inst", password="syftrocks")

print(client.datasets)

bc_dataset = client.datasets["Breast Cancer Biomarker"]

bc_dataset

features, targets = bc_dataset.assets  # using Python tuple unpacking

#Explore features and targets mock data, accessible to data scientist
print(features.mock.head(n=3))  # pandas.DataFrame
print(targets.mock.head(n=3))

#explore and see we cannot access these with data scientist role
##print(features.data) ##we get a denied error from the API for both of these requests
##print(targets.data)

X, y = features.mock, targets.mock

##Experiment Data Modelling

def ml_experiment_on_breast_cancer_data(features_data, labels, seed: int = 12345) -> tuple[float, float]:
    # include the necessary imports in the main body of the function
    # to prepare for what PySyft would expect for submitted code.
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    
    X, y = features_data, labels.values.ravel()
    # 1. Data Partition
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=seed, stratify=y)
    # 2. Data normalisation
    scaler = StandardScaler()
    scaler.fit(X_train, y_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    # 3. Model training
    model = LogisticRegression().fit(X_train, y_train)
    # 4. Metrics Calculation
    acc_train = accuracy_score(y_train, model.predict(X_train))
    acc_test = accuracy_score(y_test, model.predict(X_test))
    
    return acc_train, acc_test

##call the function on the mock data
print(ml_experiment_on_breast_cancer_data(features_data=features.mock, labels=targets.mock))

remote_user_code = sy.syft_function_single_use(features_data=features, labels=targets)(ml_experiment_on_breast_cancer_data)

description = """
    The purpose of this study will be to run a machine learning
    experimental pipeline on breast cancer data. 
    As first attempt, the pipelines includes a normalisation steps for 
    features and labels using a StandardScaler and a LabelEncoder. 
    The selected ML model is Logistic regression, with the intent
    to gather the accuracy scores on both training, and testing 
    data partitions, randomly generated.
"""

# Create a project
research_project = client.create_project(
    name="Breast Cancer ML Project",
    description=description,
    user_email_address="rachel@datascience.inst"
)

print(client.projects)
code_request = research_project.create_code_request(remote_user_code, client)
print(code_request)
print(client.code)
print(client.requests)

#this should fail before the request has been approved
client.code.ml_experiment_on_breast_cancer_data(features_data=features, labels=targets)
