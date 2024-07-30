param (
    [string]$FolderName
)

if (-not $FolderName) {
    Write-Error "You must provide a folder name."
    exit 1
}

# Define paths based on the provided folder name
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

# Read each test case from the JSON file
$testCases = Get-Content $jsonFile | ConvertFrom-Json

foreach ($testCase in $testCases) {
    $id = $testCase.id
    $cppFile = "$id.cpp"
    $input = $testCase.input
    $expectedOutput = $testCase.expected_output
    $punctaj = [int]$testCase.punctaj

    Write-Output "Testing $cppFile"

    # Build Docker image for the current C++ file
    Write-Output "Building Docker image for $cppFile"
    docker-compose build --build-arg "CPP_FILE=$cppFile" | Tee-Object -FilePath "$FolderName/build-$id.log"

    # Initialize score
    $score = 0

    Write-Output "Testing input: $input"

    # Run the Docker container with the input using docker-compose
    $actualOutput = (echo $input | docker-compose run --rm cpp-app) -replace "`r`n", "`n"

    Write-Output "Expected output: $expectedOutput"
    Write-Output "Actual output: $actualOutput"

    if ($actualOutput.Trim() -eq $expectedOutput.Trim()) {
        Write-Output "Test passed!"
        $score += $punctaj
    } else {
        Write-Output "Test failed!"
    }
    Write-Output ""

    Write-Output "${cppFile}: Final score = $score"
    Write-Output ""
}
