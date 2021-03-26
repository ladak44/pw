resource "aws_vpc" "emr_vpc" {
    cidr_block = "10.0.0.0/16"

    tags = {
        Name = var.name
        Project = var.project
        Env = var.environment
    }
}

resource "aws_subnet" "emr_subnet" {
    vpc_id = aws_vpc.emr_vpc.id
    cidr_block = "10.0.1.0/24"

    tags = {
        Name = var.name
        Project = var.project
        Env = var.environment
    }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.emr_vpc.id

  tags = {
    Name = var.name
    Project = var.project
    Env = var.environment
  }
}

resource "aws_route_table" "emr_route" {
  vpc_id = aws_vpc.emr_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = var.name
    Project = var.project
    Env = var.environment
  }
}

resource "aws_route_table_association" "emr_route_assoc" {
    subnet_id = aws_subnet.emr_subnet.id
    route_table_id = aws_route_table.emr_route.id
}



