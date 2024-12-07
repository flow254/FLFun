import syft as sy

data_site = sy.orchestra.launch(name="cancer-research-centre")

client = data_site.login(email="owen@cancer-research.science", password="cancer_research_syft_admin")

print(client.projects)

request = client.requests[0]
print(request)

print(request.code)

syft_function = request.code

bc_dataset = client.datasets["Breast Cancer Biomarker"]
features, labels = bc_dataset.assets

result_mock_data = syft_function.run(features_data=features.mock, labels=labels.mock)
print(result_mock_data)

result_real_data = syft_function.run(features_data=features.data, labels=labels.data)
print(result_real_data)

request.approve()

print(client.requests)
