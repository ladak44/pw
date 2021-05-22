# nazwa providera i region
provider "aws" {
  region = "us-east-1"
}

# wersja providera 
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "3.39.0"
    }
  }
}