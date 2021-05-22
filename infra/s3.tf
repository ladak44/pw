# Bucket S3 na dane
resource "aws_s3_bucket" "create_bucket" {
  bucket = "${var.s3_bucket_name}"
  acl    = "private"

   tags = {
    role = "rolename"
    env  = "env"
  }
}