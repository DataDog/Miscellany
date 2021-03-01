# Bootstrapping the Datadog Agent using Packer, Terraform and AWS Secrets Manager

The Datadog Agent is pretty flexible in the fact that it allows you to perform an "install only" type of installation, that doesn't actually start the Agent, or send any data into Datadog for processing. This is useful when creating images that are pre-loaded with apps that your company needs. In this example, I'll show you how to;

1. Create an AMI in AWS that has the latest updates and the latest Datadog Agent pre-installed by using Packer.
1. Deploy and instance into AWS that uses your newly created AMI, and also takes advantage of AWS Secrets Manager to pull in your Datadog API key at deployment time automatically.

## Why is this Useful?
The really cool thing about this deployment method is that it allows the end-user to deploy instances to AWS without the need for managing secrets locally. Because we're using IAM Instance Profiles to configure instance-level access to AWS Secrets Manager, the instance just by being launched with the correct profile associated with it, will automatically have access to the secrets it needs (in this case the Datadog API key) to configure itself. 

## Assumptions
* To use the example Terraform code, you will need AWS access, and permissions to create an EC2 instance, VPC, Security Groups, IAM Roles and Profiles, an SSH keypair and AWS Secrets in Secrets Manager.
* You have a local development environment (Mac, Windows, Linux), with the latest [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) (`v0.14.7` as of this writing) and [Packer](https://learn.hashicorp.com/tutorials/packer/getting-started-install) (`1.7.0` as of this writing) installed.
* This code uses completely [AWS Free Tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc) eligable resources, however you should always double-check potential usage costs before deploying.
* You have a [Datadog account](https://app.datadoghq.com/signup) and the ability to create/access an API key.
* You have an understanding of Packer and Terraform, if you haven't used Packer or Terraform before, here are some excellent resources on what they are and how to use them.
    * [Learn Terraform](https://learn.hashicorp.com/terraform)
    * [Learn Packer](https://learn.hashicorp.com/packer)
* You have an SSH keypair setup locally and have an understanding of how to SSH into a Linux server.
* It's a good idea to have the AWS CLI tool installed locally for quick testing

## Step 1 - Setup

1. Locally, create a workspace directory to work from.
1. Clone this repo into that directory.
1. Copy just this directory and subdirectories/files (from root `./agent_bootstrapping/packer_terraform_aws`) into it's own directory outside of the repo, this is because you will be modifying the file contents.
1. Change directory into the newly copied directory, all work will be done in here.
1. First, edit the `./packer/ubuntu-xenial-16.04-amd64-server.pkr.hcl` file and change the `locals` variables:
    ```
    locals { 
      ami_name_prefix = "ddog-ubuntu-xenial"
      region = "us-east-2"
      instance_type = "t2.micro"
      ddog_url = "datadoghq.com" # Change to datadoghq.eu for EU
      ddog_major_version = "7"
      timestamp = regex_replace(timestamp(), "[- TZ:]", "")
      # Uncomment if you want to use a custom subnet
      # subnet_id = "CHANGEME"
    }
    ```
    The default values should be fine, however tweak them to  your needs. If you uncomment `subnet_id`, be sure to also uncomment the corresponding usage of it on `line 17`.
1. Next, CD into the `./terraform` directory, and copy the `terraform.tfvars.example` to `terraform.tfvars`.
1. All of these variables are customizable, but there are some that are required to be changed (marked with comment), specifically;
    * *ami_name_prefix* - this should match the `ami_name_prefix` that was set in the Packer template in step 5. This is a regex, so the format is `name-prefix-*`, if you haven't changed the Packer template, then you don't need to change this.
    * *iam, sg_info, instance_info* - the defaults are fine for a quick test, however you may want to customize these a bit more.
    * *ssh_key* - this is important, make sure to at least set the `file` to the correct path of your Public SSH key.
    * *ddog_api_key* - **Required** - youre Datadog API key, data won't show up without this.
    * *owner_id* - **Required** - when pulling AMIs, Terraform will search based on the Owner ID (your AWS Account ID).
    * *networking* - you can leave this as-is, or you can modify it to your liking, I typically use a separate VPC than default for most of my testing.
    * *allowed_cidrs* - **Required** - this code will spin up an Admin Security Group that allows for connectivity into the instance from whatever IP subnet is defined, default is `0.0.0.0/0` for "Allow All", however I highly recommend setting this to your own public IP, for example in Google type "what is my ip", then enter what you see as `12.12.12.12/32`, replacing the `12`'s with your actual IP info.

## Step 2 - Build an AMI
The Packer template that is in this example does a few things:
  * It runs updates on the Ubuntu system
  * It installs the AWS CLI tool on the instance for easy retrieval of secrets from the instance
  * It installs the Datadog agent in "Install Only" mode, and sets the API key to `PREINSTALL` as a value
  * It deploys the newly created AMI to your account, ready for use

1. First, be sure you have your AWS credentials configured properly on your local system, I recommend following this guide to make sure you have them set as either [environment variables](https://www.packer.io/docs/builders/amazon#environment-variables), or in a [shared credentials file](https://www.packer.io/docs/builders/amazon#shared-credentials-file). The good news is that you just need to do this once, as Terraform uses the same method for authentication.
1. Next, CD into the `./packer` directory, and then run; 
    ```
    packer build ubuntu-xenial-16.04-amd64-server.pkr.hcl
    ```
1. This will build the AMI and deploy it to your account, a successful build will look something like this:
    ```
    ==> amazon-ebs.ubuntu-xenial: Waiting for the instance to stop...
    ==> amazon-ebs.ubuntu-xenial: Creating AMI ddog-ubuntu-xenial-0063234234234c87e82a6 from instance i-0a150a29b32b4c589
        amazon-ebs.ubuntu-xenial: AMI: ami-0063234234234c87e82a6
    ==> amazon-ebs.ubuntu-xenial: Waiting for AMI to become ready...
    ==> amazon-ebs.ubuntu-xenial: Terminating the source AWS instance...
    ==> amazon-ebs.ubuntu-xenial: Cleaning up any extra volumes...
    ==> amazon-ebs.ubuntu-xenial: No volumes to clean up, skipping
    ==> amazon-ebs.ubuntu-xenial: Deleting temporary security group...
    ==> amazon-ebs.ubuntu-xenial: Deleting temporary keypair...
    Build 'amazon-ebs.ubuntu-xenial' finished after 8 minutes 17 seconds.

    ==> Wait completed after 8 minutes 17 seconds

    ==> Builds finished. The artifacts of successful builds are:
    --> amazon-ebs.ubuntu-xenial: AMIs were created:
    us-east-2: ami-0063234234234c87e82a6
    ```
1. That's really it, at this point you should see the AMI you've created in your account, you can run `aws ec2 describe-images --region us-east-2 --owners self --output json | grep ddog` to take a look at your images (replace `ddog` with whatever string identifies your AMI).

## Step 3 - Deploy using Terraform
The Terraform code included is meant to be fully self-contained, that means it creates an AWS Secret, SSH KeyPair, Instance, IAM Role, Instance Profile, and everything else needed to bootstrap an instance that is ready to read 1 specific secret out of the box. This example doesn't take into account many best practices from Hashicorp due to the fact that it's just meant to show off the process. **So if you use any of this code, please be sure to fully understand what it is doing, and follow [Terraform Recommended Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html) when deploying.**

1. CD into the `./terraform` directory.
1. Run `terraform init` to initialize the AWS and Template plugins.
1. Run `terraform plan` to see what is about to be deployed, be sure to fix any errors you see in syntax.
1. After you have verified everything, run `terraform apply`, you will then be prompted to answer `yes` to continue, do so if everything looks ok.
1. Unless you've skipped ahead, you'll notice that everything deployed _except for_ and actual instance, this is because by default, this code has the instance `count` set to `0`, so go into the `ubuntu-xenial.tf` file and change `count = 0` to `count = 1` on `line 27`.
1. Go through the `terraform plan`, then `terraform apply` process again.
1. Once done, you should now have an Ubuntu instance in AWS that is based on the AMI that you built previously in Step 2.
1. You can now ssh into the instance to verify that it's up and running, and run `sudo datadog-agent status` to verify the agent is working properly. After a few minutes, you will start to see data for the instance show up in Datadog.


Now if you use that AMI combined with the proper IAM Instance Profile for all future deployments, your instances will automatically have Datadog Agent installed and reporting.