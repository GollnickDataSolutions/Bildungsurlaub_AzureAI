$grp = "gollnickdatasolutions"

# create the resource group
# az group create --name $grp --location eastus

# create storage account from bicep template inside the resource group grp
az deployment group create --resource-group $grp --template-file .\storage_account2.bicep --parameters storageAccountName=bertstorage20251029


# create a storage account via az cli
# az storage account create --name bicepstorage --resource-group $grp --location eastus --sku Standard_LRS

# list all resources in the resource group grp
az resource list --resource-group $grp