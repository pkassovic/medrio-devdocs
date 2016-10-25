Param(
[Parameter(Mandatory=$True)][string]$studyAPIKey,
[Parameter(Mandatory=$True)][string]$instance,
[Parameter(Mandatory=$True)][string]$dataExportOptionsFile,
[Parameter(Mandatory=$True)][string]$outputFolder,
[int] $jobDelayInSecs = 20
)

#force TLS version just in case
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12


$SendDataExportRequest= "https://$instance.api.medrio.com/v1/MedrioServiceV1.svc/Studies/$studyAPIKey/Jobs/ExportFileConfig"
$GetDataExportStatus= "https://$instance.api.medrio.com/v1/MedrioServiceV1.svc/Studies/$studyAPIKey/Jobs/"
$jobId = 0
$jobFile = ""


Function Send-DataExportRequest{
Param($optionsFile)

$request = [System.Net.WebRequest]::Create("$SendDataExportRequest")
$request.Method="POST"
$request.ContentType = "application/xml"

$requestStream = $request.GetRequestStream()

$fileStream = [System.IO.File]::OpenRead("$optionsFile")
$fileStream.CopyTo($requestStream)


$response = $request.GetResponse()

$fileStream.Close()
$fileStream.Dispose()

$requestStream = $response.GetResponseStream()
$readStream = New-Object System.IO.StreamReader $requestStream

$data=$readStream.ReadToEnd()

$results = [xml]$data

Return $results.MedrioResponse

}

Function Get-DataExportStatus{
Param($tjobId)

$request = [System.Net.WebRequest]::Create("$GetDataExportStatus$tjobId")
$request.Method="GET"

$response = $request.GetResponse()
$requestStream = $response.GetResponseStream()
$readStream = New-Object System.IO.StreamReader $requestStream

$data=$readStream.ReadToEnd()

$results = [xml]$data

Return $results.MedrioResponse.Records.Job
}


Function Get-DataExportResult{
Param($jobFile, $outputFolder)

$request = [System.Net.WebRequest]::Create($jobFile)
$request.Method="GET"

$response = $request.GetResponse()
$requestStream = $response.GetResponseStream()

$fileStream = [System.IO.File]::OpenWrite("$outputFolder\\MedrioDataExport.zip")

$requestStream.CopyTo($fileStream)

$fileStream.Close()
$fileStream.Dispose()

$requestStream.Close()
$requestStream.Dispose()

}


# sending request for get data export
Write-Host "Sending request to Medrio for Data Export"

$result = Send-DataExportRequest -optionsFile $dataExportOptionsFile

Write-Host "Request sent with result $($result.Code)"

$jobId = $result.Records.Job.JobID

Write-Host "Getting status of job id: $jobId"

#get status of job and wait while it completes
do {

Write-Host "Waiting $jobDelayInSecs for job to complete"

[System.Threading.Thread]::Sleep($jobDelayInSecs)

$result = Get-DataExportStatus -tjobId $jobId

} while ($result.Status -ne "Successful")



Write-Host "Downloading job file from location: $($result.File)"

Get-DataExportResult -jobFile $result.File -outputFolder $outputFolder


