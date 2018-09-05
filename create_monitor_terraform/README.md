# Terraform Datadog
Infrastructure and Monitoring as Code w/ Terraform &amp; Datadog example. This
repo will create infrastructure and monitoring resources using Terraform as
defined within the same configuration.

Be sure to watch this video of Atlassian presenting on their usage of Terraform
and Datadog: https://vimeo.com/237934245.

All terraform configuration can be found under the [`/terraform`](/terraform)
directory. Their is no hierarchy for this example, but typically you might
organize your terraform configuration in such a way that it gets broken into
re-usable modules (and potentially modules of modules) for common patterns
within your infrastructure.

In this example, modules and raw configuration are colocated into "groups"
respective of their function, e.g. `infrastructure.tf` will contain the
configuration to create AWS resources, while `monitoring.tf` will contain the
configuration to create Datadog resources, and so on.

__*This repo is only for example purposes.*__

# Noteworthy
- This repo does not use [Terraform
workspaces](https://www.terraform.io/docs/state/workspaces.html); it is a best
practice to use workspaces, this repo is only for example purposes.
- This repo does not use [Terraform remote
state](https://www.terraform.io/docs/state/remote.html); it is a best
practice to use remote state, this repo is only for example purposes.
- For infrastructure definitions, see
[`./terraform/infrastructure.tf`](./terraform/infrastructure.tf)
- For monitoring definitions, see
[`./terraform/monitoring.tf`](./terraform/monitoring.tf)
- The repo will provision an AWS VPC, Subnets, NAT, security groups & rules,
EIP, and route tables. Should you not want those items to be created you
should delete or comment out the
[`./terraform/infrastructure.tf`](./terraform/infrastructure.tf) file. This was
included for example purposes only.

# Use
## Setup
- Checkout this repository using git
- Change into the [`/terraform`](/terraform) directory on the command line
- Update variable values in [`/terraform/variables.tf`](/terraform/variables.tf)
to meet those required by your environment
- Define AWS authentication via Environment, Shared Creds file, etc as
documented in the [Terraform AWS Provider
docs](https://www.terraform.io/docs/providers/aws/index.html#environment-variables)
- Define `DATADOG_API_KEY` and `DATADOG_APP_KEY` in environment variables per
the [Terraform
documentation](https://www.terraform.io/docs/providers/datadog/index.html)
- Set `TF_VAR_datadog_api_key` in your environment. e.g. `export
TF_VAR_datadog_api_key="<your-api-key>"` (note the quotes `""` around the value)
; this is used to install the agent on an EC2 host via userdata script

## Init
Run `terraform init` - this will pull down all modules and setup your
local environment to get started with terraform. Output will look similar to the
example below (truncated in places):
```
Initializing modules...
- module.vpc
  Found version 1.17.0 of terraform-aws-modules/vpc/aws on registry.terraform.io
  Getting source "terraform-aws-modules/vpc/aws"

Initializing provider plugins...
- Checking for available provider plugins on https://releases.hashicorp.com...
- Downloading plugin for provider "datadog" (1.0.3)...
- Downloading plugin for provider "aws" (1.8.0)...

The following providers do not have any version constraints in configuration,
so the latest version was installed.

* provider.aws: version = "~> 1.8"
* provider.datadog: version = "~> 1.0"

Terraform has been successfully initialized!

...
```

# Plan
Run `terraform plan -out=plan.out` - this will provide you with a plan of what
terraform will change (commonly known as a "dry run"). The `-out` flag allows us
to save this plan to a file and use it when making the actual changes later. In
this way we can ensure that any local or remote changes that have occurred
between the time we ran `plan` and `apply` are not accepted.

An example of plan output (truncated in places):
```
Refreshing Terraform state in-memory prior to plan...
The refreshed state will be used to calculate this plan, but will not be
persisted to local or remote state storage.

aws_vpc.this: Refreshing state... (ID: vpc-f215b19a)
data.aws_availability_zones.available: Refreshing state...
aws_eip.nat[2]: Refreshing state... (ID: eipalloc-7b1a3055)
...
aws_route.private_nat_gateway[2]: Refreshing state... (ID: r-rtb-e949df811080289494)

------------------------------------------------------------------------

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  + aws_instance.web
      id:                           <computed>
      ami:                          "ami-15e9c770"
      ...

  + aws_key_pair.aws_ssh_key
      id:                           <computed>
      fingerprint:                  <computed>
      key_name:                     "datadog-demo-default"
      ...

  + aws_security_group.web_sg
      id:                           <computed>
      description:                  "Security Group for web node SSH"
      ...
      vpc_id:                       "vpc-f215b19a"

  ...
  + module.http_security_group.aws_security_group_rule.outbound_internet_to_anywhere
      id:                           <computed>
      cidr_blocks.#:                "1"
      cidr_blocks.0:                "0.0.0.0/0"
      from_port:                    "0"
      protocol:                     "-1"
      security_group_id:            "${aws_security_group.sg.id}"
      self:                         "false"
      source_security_group_id:     <computed>
      to_port:                      "0"
      type:                         "egress"


Plan: 9 to add, 0 to change, 0 to destroy.

------------------------------------------------------------------------

This plan was saved to: plan.out

To perform exactly these actions, run the following command to apply:
    terraform apply "plan.out"
```

# Apply
Run `terraform apply "plan.out"` to create or update your infrastructure. By
passing `"plan.out"` this will ensure that what you saw in your dry run is what
gets applied to real infrastructure ignoring any local or remote changes (which
can result in failure if there is a mismatch, this can help you prevent
mistakes or collisions). Example output below w/ truncations:
```
module.vpc.aws_eip.nat[1]: Creating...
  allocation_id:     "" => "<computed>"
  ...
  tags.Name:         "" => "vpc-example-ca-central-1b"
  tags.Terraform:    "" => "true"
  vpc:               "" => "true"
module.vpc.aws_vpc.this: Creating...
  assign_generated_ipv6_cidr_block: "" => "false"
  cidr_block:                       "" => "10.0.0.0/16"
  default_network_acl_id:           "" => "<computed>"
...
module.vpc.aws_route.private_nat_gateway[2]: Creation complete after 0s (ID: r-rtb-c121dda91080289494)

Apply complete! Resources: 36 added, 0 changed, 0 destroyed.

Outputs:

instance_id = i-0df63b920403b43c4
instance_ip = 35.183.32.231
subnet_ids = [
    subnet-91fe18f9,
    subnet-76cbf60d,
    subnet-b1f117d9
]
vpc_id = vpc-b64455df
```

# Destroy
Run `terraform destroy` to delete all your resources. Ideally you should, in a
best practices scenario, run a `plan -destroy -out=<file.out>` as described in
the [Terraform
docs](https://www.terraform.io/docs/commands/plan.html#destroy) to ensure you
do not destroy anything you intended to keep and then `apply` that plan.

Example output (truncated in places):
```
aws_key_pair.aws_ssh_key: Refreshing state... (ID: datadog-demo-default)
aws_vpc.this: Refreshing state... (ID: vpc-f215b19a)
data.aws_availability_zones.available: Refreshing state...
aws_eip.nat[1]: Refreshing state... (ID: eipalloc-571b3179)
...
aws_route.private_nat_gateway[2]: Refreshing state... (ID: r-rtb-e949df811080289494)

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  - aws_key_pair.aws_ssh_key
  ...
  - module.vpc.aws_vpn_gateway.this

Plan: 0 to add, 0 to change, 37 to destroy.

Do you really want to destroy?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

random_shuffle.subnet: Destroying... (ID: -)
random_shuffle.subnet: Destruction complete after 0s
module.vpc.aws_route.private_nat_gateway[1]: Destroying... (ID: r-rtb-eb4adc831080289494)
aws_security_group_rule.inbound_ssh_from_anywhere: Destroying... (ID: sgrule-3703888604)
...
module.vpc.aws_vpc.this: Destroying... (ID: vpc-f215b19a)
module.vpc.aws_vpc.this: Destruction complete after 0s

Destroy complete! Resources: 37 destroyed.
```
