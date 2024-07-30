param (
    [string]$FolderName
)

if (-not $FolderName) {
    Write-Error "You must provide a folder name."
    exit 1
}

$jsonFile = "$FolderName/tests.json"
$cppFolder = "$FolderName/cpp-files"
$dockerComposeFile = "docker-compose.yml"

if (-not (Test-Path $jsonFile)) {
    Write-Error "tests.json not found in $FolderName"
    exit 1
}

if (-not (Test-Path $cppFolder)) {
    Write-Error "cpp-files folder not found in $FolderName"
    exit 1
}

$testCases = Get-Content $jsonFile | ConvertFrom-Json

foreach ($testCase in $testCases) {
    $id = $testCase.id
    $cppFile = "$id.cpp"
    $input = $testCase.input
    $expectedOutput = $testCase.expected_output
    $punctaj = [int]$testCase.punctaj

    Write-Output "Testare $cppFile"

    Write-Output "Construire docker image pentru $cppFile"
    docker-compose build --build-arg "CPP_FILE=$cppFile" | Tee-Object -FilePath "$FolderName/build-$id.log"

    $score = 0

    Write-Output "Test input $input"
    
    $actualOutput = (echo $input | docker-compose run --rm cpp-app) -replace "`r`n", "`n"

    Write-Output "Output asteptat: $expectedOutput"
    Write-Output "Output actual: $actualOutput"

    if ($actualOutput.Trim() -eq $expectedOutput.Trim()) {
        Write-Output "Ok!"
        $score += $punctaj
    } else {
        Write-Output "Nu e ok!"
    }
    Write-Output ""

    Write-Output "${cppFile}: Punctaj = $score"
    Write-Output ""
}
