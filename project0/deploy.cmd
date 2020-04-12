@echo off
echo Deploying to Azure...
az storage blob sync -c app1 -s app1/build
echo Done.