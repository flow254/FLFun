import syft as sy

data_site = sy.orchestra.launch(name="cancer-research-centre")

client = data_site.login(email="rachel@datascience.inst", password="syftrocks")

print(client.requests)

bc_dataset = client.datasets["Breast Cancer Biomarker"]
features, labels = bc_dataset.assets

result = client.code.ml_experiment_on_breast_cancer_data(features_data=features, labels=labels).get()

print(result)



