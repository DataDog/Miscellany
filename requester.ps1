<# 
This script will establish a UDP client, connect it to 127.0.0.1:8125, 
invoke a request to our supplied endpoint, parse the json returned from that,
and send the key-value pairs from that json to dogstatsd which will then send
them through to datadog as custom metrics.
#>

$dogstatsdAddress = '127.0.0.1'
$dogstatsdPort = '8125'

$restEndpoint = 'http://127.0.0.1:5000/'

# udp client
$udpClient = New-Object System.Net.Sockets.UdpClient 
$udpClient.Connect($dogstatsdAddress, $dogstatsdPort)
# invoke request to get json data from endpoint, and parse response
$ipinfo = Invoke-WebRequest $restEndpoint -UseBasicParsing | ConvertFrom-Json
foreach ($info in $ipinfo.PSObject.Properties) {
    # get name and value of current json element
    $metricName = $info.Name
    $metricValue = $info.Value
    Write-Host "Metric Name: $metricName | Metric Value: $metricValue "
    # encode data s.t. dogstatsd accepts it
    $encodedData=[System.Text.Encoding]::ASCII.GetBytes("${metricName}:${metricValue}|g") # curly brackets these otherwise it'll interpret it as a property value
    Write-Host "data to be sent to DogstatsD: $encodedData"
    # send it through to our udp client (pointed to dogstatsd)
    $bytesSent=$udpClient.Send($encodedData,$encodedData.Length)
    Write-Host "bytesSent: $bytesSent"