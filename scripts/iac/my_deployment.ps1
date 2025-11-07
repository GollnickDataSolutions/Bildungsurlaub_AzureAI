$grp = "berttest"

az group create --name $grp --location eastus

az storage account create --name bertstorage20251106 --resource-group $grp --location eastus --sku Standard_LRS --template-file .\storage.bicep

