
# Nazwy zasobów drukowane po utworzeniu klastra
# ID identyfikator klastra
output "id" {
  value = "${aws_emr_cluster.cluster.id}"
}
# Nazwa klastra
output "name" {
  value = "${aws_emr_cluster.cluster.name}"
}
# DNS klastra
output "master_public_dns" {
  value = "${aws_emr_cluster.cluster.master_public_dns}"
}
# ID Security Grupy Mastera
output "master_security_group_id" {
  value = "${aws_security_group.emr_master.id}"
}
# ID Securtity Grupy Slava
output "slave_security_group_id" {
  value = "${aws_security_group.emr_slave.id}"
}
