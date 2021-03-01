resource "aws_iam_role" "ddog_api_key" {
  name = var.iam["iam_role_name"]

  assume_role_policy = <<EOF
{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Effect":"Allow",
         "Principal":{
            "Service":"ec2.amazonaws.com"
         },
         "Action":"sts:AssumeRole",
         "Sid": ""
      }
   ]
}
EOF
}

resource "aws_iam_instance_profile" "ddog_api_key" {
  name = var.iam["iam_instance_profile_name"]
  role = aws_iam_role.ddog_api_key.name
}

resource "aws_iam_policy" "ddog_api_key" {
  name = var.iam["iam_policy_name"]
  path = "/"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "secretsmanager:GetSecretValue",
            "Resource": "${aws_secretsmanager_secret.ddog_api_key.id}"
        }
    ]
}
EOF

}

resource "aws_iam_role_policy_attachment" "ddog_attach" {
  role       = aws_iam_role.ddog_api_key.name
  policy_arn = aws_iam_policy.ddog_api_key.arn
}