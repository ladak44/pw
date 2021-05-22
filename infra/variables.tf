# Zmienne środowiskowe i tagi 
# Nazwa regionu
variable "region" {
   default = "us-east-1"
}
# Nazwa aplikacji
variable "name" {
  default = "Airly"
}
# Nazwa projektu
variable "project" {
  default = "PW"
}
# Nazwa środowiska w jakim utworzono projekt
variable "environment" {
  default = "Big Data"
}
# Nazwa pary kluczy wykorzystywanej przy połączeniach SSH
variable "key_name" {
  default = "aws_educate"
}
# Adress IP maszyny która będzie miała dostęp do klastra 
variable "ingress_cidr_blocks" {
   default = "5.184.2.217/32"
}
# Nazwa bucketu w którym będą składowane dane
variable "s3_bucket_name" {
  default = "airly-pw"
}
