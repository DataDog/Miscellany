# Variable definitions
# This is an example, typically you'd have a *.tfvars file per a workspace
# and would invoke terraform using the "-var-file=<filename>.tfvars" to provide
# the correct variables
# In this case we are using terraform's ability to automatically pickup a
# var file by including "*.auto.tfvars" in the name.
# See: https://www.terraform.io/docs/configuration/variables.html#variable-files

aws_region = "ca-central-1"
aws_instance_type = "t2.nano"
# replace with your own public key material
aws_public_key_material = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC0pxtVc4fGDU7Z0+ErXEHpiCf8udZSuHToX+pT73+Enu0zl5vEJQt9piM/OQLJIqVFnE8OOMUJ5wEtqyxLC+FU4Ef8INc6m+/jWq+QdnnWXbMdA5sUNCwt439sWBsaHGXGcK03hUy5NhdENER3C9JyCkKytTSYvBjqU57QiqaglMsLgJyBfFmyhazyBo86pyulhIDBpt/bgWYhu5cpEf0aE3FYw3mxFFxqv+1Ydu6J59i0Llu8L4SPiaiWKQv6tR/g222Jo8jRi9ZbZfhKNreJbNmz4LmNJZk7sDw18OCWsEddbvdWX0387+ryOIiaTwRL+rGXlz9DYZLHdFvzQocqB25gwQ7Ciy0BPCp0uwK9MIW/D4KeSl2FgzfQ6MYwWDC6EC2QWaaKmQWDit8zUpOrSonhfQOOjogrsGH0BFtdPW8nmI4lzpEzrO+qs8HFn1Z1fEH8N8DST6YWSi7qAYOl8TetFwmd1uwkEb8ox9DWxR0DNoXMURVit5ZESJnUvjmSLAgJ1lsGr5CL3GENRnCSOvpNoKUQsWyP6VdN9iN23y8SVn7PQ2KG/fEXH8YjdavTMYFzzmqRcp1lk5Y7Z8KG+yi7ayZJRsK9mE0YZmqAptmY7QlN6svo5N0XSJxQUx6eAFlk07iangfjMrsYiCXzMuQl1wsoWNRBABakaEyTHQ== chriskelner@ckelner"
