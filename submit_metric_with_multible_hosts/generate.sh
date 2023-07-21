cat > send.sh <<EOF
curl -X POST "https://api.datadoghq.com/api/v2/series" \\
-H "Accept: application/json" \\
-H "Content-Type: application/json" \\
-H "DD-API-KEY: YOUR_API_KEY_HERE" \\
-d @- << EOF
{
  "series": [
EOF

i=0
total=$(cat data.csv  | wc -l)
total=$(($total - 2))

while IFS="," read -r hostname value timestamp
do
cat >> send.sh <<EOF
    {
      "metric": "example.metric.1",
      "type": 0,
      "points": [
        {
          "timestamp": "$timestamp",
          "value": "$value"
        }
      ],
      "resources": [
        {
          "name": "$hostname",
          "type": "host"
        }
      ]
    }
EOF
if [ $i -eq $total ]
then
echo "  ]" >> send.sh
else
echo "," >> send.sh
fi
i=$((i+1))
done < <(tail -n +2 data.csv)
echo "}" >> send.sh
echo "EOF" >> send.sh
bash send.sh
