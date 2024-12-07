import syft as sy

##check syft version
## print(sy.__version__)
'''

data_site = sy.orchestra.launch(name="cancer-research-centre", reset=True)

client = data_site.login(email="info@openmined.org", password="changethis")

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
## pip install ucimlrepo to get cancer data
## import data from cancer repo
try:
    from ucimlrepo import fetch_ucirepo
except ImportError:
    install("ucimlrepo")
    from ucimlrepo import fetch_ucirepo


# fetch dataset 
breast_cancer_wisconsin_diagnostic = fetch_ucirepo(id=17) 

# data (as pandas dataframes) 
X = breast_cancer_wisconsin_diagnostic.data.features 
y = breast_cancer_wisconsin_diagnostic.data.targets

# metadata 
metadata = breast_cancer_wisconsin_diagnostic.metadata
# variable information 
variables = breast_cancer_wisconsin_diagnostic.variables

print(X.head(n=5))
print(X.shape)

print(y.sample(n=5, random_state=10))

import numpy as np

# fix seed for reproducibility
SEED = 12345
np.random.seed(SEED)

X_mock = X.apply(lambda s: s + np.mean(s) + np.random.uniform(size=len(s)))
y_mock = y.sample(frac=1, random_state=SEED).reset_index(drop=True)

features_asset = sy.Asset(
    name="Breast Cancer Data: Features",
    data = X,      # real data
    mock = X_mock  # mock data
)

targets_asset = sy.Asset(
    name="Breast Cancer Data: Targets",
    data = y,      # real data
    mock = y_mock  # mock data
)

features_asset.data.head(n=3)
features_asset.mock.head(n=3)

# Metadata
description = f'{metadata["abstract"]}\n{metadata["additional_info"]["summary"]}'

paper = metadata["intro_paper"]
citation = f'{paper["authors"]} - {paper["title"]}, {paper["year"]}'

summary = "The Breast Cancer Wisconsin dataset can be used to predict whether the cancer is benign or malignant."

# Dataset creation
breast_cancer_dataset = sy.Dataset(
    name="Breast Cancer Biomarker",
    description=description,
    summary=summary,
    citation=citation,
    url=metadata["dataset_doi"],
)
breast_cancer_dataset.add_asset(features_asset)
breast_cancer_dataset.add_asset(targets_asset)

print("breast cancer dataset:")
print(breast_cancer_dataset)

client.upload_dataset(dataset=breast_cancer_dataset)
print(client.datasets)

## data_site.land()
'''

##Part 2
data_site = sy.orchestra.launch(name="cancer-research-centre", reset=False)

# logging in as root client with default credentials
client = data_site.login(email="info@openmined.org", password="changethis")

client.datasets

OWEN_EMAIL = "owen@cancer-research.science"
OWEN_PASSWD = "cancer_research_syft_admin"

client.account.set_email(OWEN_EMAIL)

# we can bypass the confirmation by using the confirm=False parameter
client.account.set_password(OWEN_PASSWD, confirm=False)

client.account.update(name="Owen, the Data Owner", 
                 institution="Cancer Research Centre")

client = data_site.login(email=OWEN_EMAIL, password=OWEN_PASSWD)

client.users
print(client.users)

rachel_account_info = client.users.create(
    email="rachel@datascience.inst",
    name="Dr. Rachel Science",
    password="syftrocks",
    password_verify="syftrocks",
    institution="Data Science Institute",
    website="https://datascience_institute.research.data"
)

print(f"New User: {rachel_account_info.name} ({rachel_account_info.email}) registered as {rachel_account_info.role}")

client.users
print(client.users)
