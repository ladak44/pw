# Security grupa mastera
resource "aws_security_group" "emr_master" {
  name                   = "${var.name} - EMR-master"
  description            = "Security group for EMR master."
  vpc_id                 = aws_vpc.emr_vpc.id
  revoke_rules_on_delete = true
# FW dla SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ingress_cidr_blocks]
  }
# FW dla brokera kafki
  ingress {
    from_port   = 9092
    to_port     = 9092
    protocol    = "tcp"
    cidr_blocks = [var.ingress_cidr_blocks]
  }
# FW dla Jupytera
  ingress {
    from_port   = 9443
    to_port     = 9443
    protocol    = "tcp"
    cidr_blocks = [var.ingress_cidr_blocks]
  }


  ingress {
    from_port   = 4040
    to_port     = 4040
    protocol    = "tcp"
    cidr_blocks = [var.ingress_cidr_blocks]
  }

  ingress {
    from_port   = 8888
    to_port     = 8888
    protocol    = "tcp"
    cidr_blocks = [var.ingress_cidr_blocks]
  }

  ingress {
    from_port   = 20888
    to_port     = 20888
    protocol    = "tcp"
    cidr_blocks = [var.ingress_cidr_blocks]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "EMR_master"
  }
}
# Security grupa dla slava 
resource "aws_security_group" "emr_slave" {
  name                   = "${var.name} - EMR-slave"
  description            = "Security group for EMR slave."
  vpc_id                 = aws_vpc.emr_vpc.id
  revoke_rules_on_delete = true

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ingress_cidr_blocks]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "EMR_slave"
  }
}


